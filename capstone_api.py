from flask import Flask, request, jsonify, render_template
from flask_cors import CORS 
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import math
from functools import wraps # Helper for decorators

# Load credentials
load_dotenv()

app = Flask(__name__, template_folder='.') 
CORS(app)

# --- CONFIGURATION ---
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'company_db')
}

# hardcoded password for router protection
APP_PASSWORD = "admin" 
# The Secret Token the API expects (In real life, this would be dynamic JWT)
API_SECRET_TOKEN = "secure-token-123"

# --- DATABASE HELPER ---
def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"Database Error: {e}")
        return None

# --- SECURITY DECORATOR  
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check Authorization Header: "Bearer webTrainingToken"
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        
        if not token or token != API_SECRET_TOKEN:
            return jsonify({"error": "Unauthorized. Invalid or missing Token."}), 401
            
        return f(*args, **kwargs)
    return decorated

# --- LOGIC HELPERS ---
def get_or_create_dept_id(dept_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT department_id FROM tbdepartments WHERE name = %s", (dept_name,))
    result = cursor.fetchone()
    
    if result:
        conn.close()
        return result['department_id']
    
    cursor.execute("SELECT MAX(department_id) as max_id FROM tbdepartments")
    new_id = (cursor.fetchone()['max_id'] or 0) + 1
    cursor.execute("INSERT INTO tbdepartments (department_id, name, location) VALUES (%s, %s, 'Unknown')", (new_id, dept_name))
    conn.commit()
    conn.close()
    return new_id

def get_dept_name(dept_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name FROM tbdepartments WHERE department_id = %s", (dept_id,))
    result = cursor.fetchone()
    conn.close()
    return result['name'] if result else "Unknown"

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

# 1. LOGIN ROUTE  
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    password = data.get('password')
    
    if password == APP_PASSWORD:
        # Return the token to the frontend
        return jsonify({"message": "Login Successful", "token": API_SECRET_TOKEN})
    else:
        return jsonify({"error": "Invalid Password"}), 401

# 2. STATISTICS ROUTE  
@app.route('/api/stats', methods=['GET'])
@auth_required # Protected!
def stats():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get counts and averages
    cursor.execute("SELECT COUNT(*) as total_employees, AVG(salary) as avg_salary FROM tbemployees")
    general_stats = cursor.fetchone()
    
    cursor.execute("SELECT COUNT(*) as total_depts FROM tbdepartments")
    dept_stats = cursor.fetchone()
    
    conn.close()
    
    return jsonify({
        "total_employees": general_stats['total_employees'],
        "avg_salary": round(general_stats['avg_salary'] or 0, 2),
        "total_departments": dept_stats['total_depts']
    })

# 3. EMPLOYEES ROUTE (CRUD + Pagination + Search)
@app.route('/api/employees', methods=['GET', 'POST', 'PUT', 'DELETE'])
@auth_required # Protected!
def employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # === READ (GET) with Pagination & Search ===
    if request.method == 'GET':
        # Parameters
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 5))
        search = request.args.get('search', '')
        
        offset = (page - 1) * limit

        # Base Query
        if search:
            search_param = f"%{search}%"
            query = "SELECT * FROM tbemployees WHERE name LIKE %s OR position LIKE %s LIMIT %s OFFSET %s"
            count_query = "SELECT COUNT(*) as count FROM tbemployees WHERE name LIKE %s OR position LIKE %s"
            params = (search_param, search_param, limit, offset)
            count_params = (search_param, search_param)
        else:
            query = "SELECT * FROM tbemployees LIMIT %s OFFSET %s"
            count_query = "SELECT COUNT(*) as count FROM tbemployees"
            params = (limit, offset)
            count_params = ()

        # Execute Count (For Pagination UI)
        cursor.execute(count_query, count_params)
        total_records = cursor.fetchone()['count']
        total_pages = math.ceil(total_records / limit)

        # Execute Data Fetch
        cursor.execute(query, params)
        employees = cursor.fetchall()
        
        # Format Data
        clean_data = []
        for emp in employees:
            clean_data.append({
                "id": emp['employee_id'],
                "name": emp['name'],
                "position": emp.get('position', ''),
                "department": get_dept_name(emp['department_id']),
                "salary": float(emp['salary'])
            })
            
        conn.close()
        
        # Return enhanced response with pagination  
        return jsonify({
            "data": clean_data,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "total_records": total_records
            }
        })

    # === CREATE (POST) ===
    elif request.method == 'POST':
        data = request.get_json()
        dept_id = get_or_create_dept_id(data['department'])
        
        cursor.execute("SELECT MAX(employee_id) as max_id FROM tbemployees")
        new_id = (cursor.fetchone()['max_id'] or 100) + 1
        
        sql = "INSERT INTO tbemployees (employee_id, name, position, email, department_id, salary) VALUES (%s, %s, %s, %s, %s, %s)"
        fake_email = f"{data['name'].replace(' ', '.').lower()}@company.com"
        
        try:
            cursor.execute(sql, (new_id, data['name'], data['position'], fake_email, dept_id, data['salary']))
            conn.commit()
            return jsonify({"message": "Employee added"}), 201
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            conn.close()

    # === UPDATE (PUT) ===
    elif request.method == 'PUT':
        emp_id = request.args.get('id')
        data = request.get_json()
        dept_id = get_or_create_dept_id(data['department'])
        
        sql = "UPDATE tbemployees SET name=%s, position=%s, department_id=%s, salary=%s WHERE employee_id=%s"
        try:
            cursor.execute(sql, (data['name'], data['position'], dept_id, data['salary'], emp_id))
            conn.commit()
            return jsonify({"message": "Employee updated"}), 200
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            conn.close()

    # === DELETE (DELETE) ===
    elif request.method == 'DELETE':
        emp_id = request.args.get('id')
        try:
            cursor.execute("DELETE FROM tbemployees WHERE employee_id = %s", (emp_id,))
            conn.commit()
            return jsonify({"message": "Employee deleted"}), 200
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5002)
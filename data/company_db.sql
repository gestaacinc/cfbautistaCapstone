-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.4.3 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for company_db
CREATE DATABASE IF NOT EXISTS `company_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `company_db`;

-- Dumping structure for table company_db.tbdepartments
CREATE TABLE IF NOT EXISTS `tbdepartments` (
  `department_id` int NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `location` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`department_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table company_db.tbdepartments: ~12 rows (approximately)
REPLACE INTO `tbdepartments` (`department_id`, `name`, `location`) VALUES
	(1, 'HR', 'Manila'),
	(2, 'IT', 'Makati'),
	(3, 'Marketing', 'Pasig'),
	(4, 'Finance', 'BGC'),
	(5, 'Quality Assurance', 'Unknown'),
	(6, 'LOGISTICS', 'Unknown'),
	(7, 'adf', 'Unknown'),
	(8, 'adfadf', 'Unknown'),
	(9, 'adfadfaf', 'Unknown'),
	(10, 'DPWH', 'Unknown'),
	(11, 'new logistics', 'Unknown'),
	(12, 'NEW IT', 'Unknown'),
	(13, 'ADFA', 'Unknown'),
	(14, 'Accounting', 'Unknown');

-- Dumping structure for table company_db.tbemployees
CREATE TABLE IF NOT EXISTS `tbemployees` (
  `employee_id` int NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `position` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `department_id` int DEFAULT NULL,
  `salary` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`employee_id`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `tbemployees_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `tbdepartments` (`department_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table company_db.tbemployees: ~13 rows (approximately)
REPLACE INTO `tbemployees` (`employee_id`, `name`, `position`, `email`, `department_id`, `salary`) VALUES
	(105, 'Carlo Tan', 'Accountant', 'carlo@company.com', 4, 40000.00),
	(108, 'New GuyS', 'Software Engineer', 'new@company.com', 2, 45000.00),
	(109, 'Capstone Tester', 'QA Engineers', 'capstone.tester@company.com', 5, 55000.00),
	(111, 'adfadf', 'adf', 'adfadf@company.com', 8, 3434.00),
	(112, 'adfadfadf', 'adfa', 'adfadfadf@company.com', 9, 34343434.00),
	(113, 'adf', 'adf', 'adf@company.com', 7, 34343.00),
	(114, 'MikeS', 'President of Philippines', 'mike@company.com', 10, 2323.00),
	(115, 'New Entry', 'Logistics', 'new.entry@company.com', 2, 33.00),
	(116, 'chester', 'it', 'chester@company.com', 11, 20000000.00),
	(117, 'test user', 'new logistics', 'test.user@company.com', 12, 2020323.00),
	(118, 'ADF', 'ADF', 'adf@company.com', 7, 3243.00),
	(119, 'ADFA', 'ADF', 'adfa@company.com', 13, 34.00),
	(120, 'New Employee', 'Accountant', 'new.employee@company.com', 4, 12000.00);

-- Dumping structure for table company_db.tbprojects
CREATE TABLE IF NOT EXISTS `tbprojects` (
  `project_id` int NOT NULL,
  `project_name` varchar(50) DEFAULT NULL,
  `department_id` int DEFAULT NULL,
  `budget` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`project_id`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `tbprojects_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `tbdepartments` (`department_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table company_db.tbprojects: ~4 rows (approximately)
REPLACE INTO `tbprojects` (`project_id`, `project_name`, `department_id`, `budget`) VALUES
	(201, 'Website Redesign', 2, 200000.00),
	(203, 'Social Media Ads', 3, 80000.00),
	(204, 'Q1 Financial Plan', 4, 90000.00);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;

/*
Project: Data Cleaning and Preparation - Electric Vehicle Population

Description:
This project aims to clean and prepare a dataset about the electric vehicle population in a specific area. 
The original data was obtained from Kaggle (https://www.kaggle.com/datasets/daniilkrasnoproshin/electric-vehicle-population-data/data) 
and contains information about electric vehicles, including details such as VIN, location, model year, vehicle type, and more.

Objectives:
1. Remove duplicates to ensure data integrity.
2. Standardize the data (remove unnecessary spaces, format columns, etc.).
3. Rename columns to improve clarity and consistency.
4. Remove unnecessary columns.
5. Prepare the data for further analysis.

Tools Used:
- MySQL for data cleaning and transformation.
- SQL techniques such as TRIM, SUBSTRING, ROW_NUMBER, and ALTER TABLE.

This project is part of my portfolio as a Data Analyst, showcasing skills in data cleaning, preparation, and manipulation using SQL.
*/

-- Review data--


SELECT *
FROM electric_vehicle_population_data;


-- Create a copy of the raw data--

CREATE TABLE ev_population
LIKE electric_vehicle_population_data;

INSERT ev_population
SELECT *
FROM  electric_vehicle_population_data;

SELECT *
FROM ev_population;

-- Create Table to DELETE duplicates--

CREATE TABLE `ev_population2` (
  `VIN (1-10)` text,
  `County` text,
  `City` text,
  `State` text,
  `Postal Code` int DEFAULT NULL,
  `Model Year` int DEFAULT NULL,
  `Make` text,
  `Model` text,
  `Electric Vehicle Type` text,
  `Clean Alternative Fuel Vehicle (CAFV) Eligibility` text,
  `Electric Range` int DEFAULT NULL,
  `Base MSRP` int DEFAULT NULL,
  `Legislative District` int DEFAULT NULL,
  `DOL Vehicle ID` int DEFAULT NULL,
  `Vehicle Location` text,
  `Electric Utility` text,
  `2020 Census Tract` bigint DEFAULT NULL,
  `row_num` INT 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO ev_population2
SELECT *, 
ROW_NUMBER() OVER(
PARTITION BY `VIN (1-10)`, `County`, `City`, `State`, `Postal Code`, `Model Year`, `Make`, `Model`, `Electric Vehicle Type`, `Clean Alternative Fuel Vehicle (CAFV) Eligibility`, `Electric Range`, `Base MSRP`, `Legislative District`, `DOL Vehicle ID`, `Vehicle Location`, `Electric Utility`, `2020 Census Tract`)
AS row_num
FROM ev_population;

-- DELETE Duplicates --

DELETE
FROM ev_population2
WHERE row_num > 1;


-- Srandardizing data

-- TRIM
UPDATE ev_population2
SET 
    `VIN (1-10)` = TRIM(`VIN (1-10)`),
    `County` = TRIM(`County`),
    `City` = TRIM(`City`),
    `State` = TRIM(`State`),
    `Postal Code` = TRIM(`Postal Code`),
    `Model Year` = TRIM(`Model Year`),
    `Make` = TRIM(`Make`),
    `Model` = TRIM(`Model`),
    `Electric Vehicle Type` = TRIM(`Electric Vehicle Type`),
    `Clean Alternative Fuel Vehicle (CAFV) Eligibility` = TRIM(`Clean Alternative Fuel Vehicle (CAFV) Eligibility`),
    `Electric Range` = TRIM(`Electric Range`),
    `Base MSRP` = TRIM(`Base MSRP`),
    `Legislative District` = TRIM(`Legislative District`),
    `DOL Vehicle ID` = TRIM(`DOL Vehicle ID`),
    `Vehicle Location` = TRIM(`Vehicle Location`),
    `Electric Utility` = TRIM(`Electric Utility`),
    `2020 Census Tract` = TRIM(`2020 Census Tract`)
    ;
    
    UPDATE ev_population2
	SET `Vehicle Location` = SUBSTRING(`Vehicle Location`, 7);
    
    SELECT DISTINCT `Electric Utility`
    FROM ev_population2;
    ORDER BY 1;
    
    -- Review for nulls
    
	SELECT 
    COUNT(*) AS total_filas,
    SUM(CASE WHEN `VIN (1-10)` IS NULL THEN 1 ELSE 0 END) AS nulos_VIN,
    SUM(CASE WHEN `County` IS NULL THEN 1 ELSE 0 END) AS nulos_County,
    SUM(CASE WHEN `City` IS NULL THEN 1 ELSE 0 END) AS nulos_City,
    SUM(CASE WHEN `State` IS NULL THEN 1 ELSE 0 END) AS nulos_State,
    SUM(CASE WHEN `Postal Code` IS NULL THEN 1 ELSE 0 END) AS nulos_Postal_Code,
    SUM(CASE WHEN `Model Year` IS NULL THEN 1 ELSE 0 END) AS nulos_Model_Year,
    SUM(CASE WHEN `Make` IS NULL THEN 1 ELSE 0 END) AS nulos_Make,
    SUM(CASE WHEN `Model` IS NULL THEN 1 ELSE 0 END) AS nulos_Model,
    SUM(CASE WHEN `Electric Vehicle Type` IS NULL THEN 1 ELSE 0 END) AS nulos_Electric_Vehicle_Type,
    SUM(CASE WHEN `Clean Alternative Fuel Vehicle (CAFV) Eligibility` IS NULL THEN 1 ELSE 0 END) AS nulos_CAFV_Eligibility,
    SUM(CASE WHEN `Electric Range` IS NULL THEN 1 ELSE 0 END) AS nulos_Electric_Range,
    SUM(CASE WHEN `Base MSRP` IS NULL THEN 1 ELSE 0 END) AS nulos_Base_MSRP,
    SUM(CASE WHEN `Legislative District` IS NULL THEN 1 ELSE 0 END) AS nulos_Legislative_District,
    SUM(CASE WHEN `DOL Vehicle ID` IS NULL THEN 1 ELSE 0 END) AS nulos_DOL_Vehicle_ID,
    SUM(CASE WHEN `Vehicle Location` IS NULL THEN 1 ELSE 0 END) AS nulos_Vehicle_Location,
    SUM(CASE WHEN `Electric Utility` IS NULL THEN 1 ELSE 0 END) AS nulos_Electric_Utility,
    SUM(CASE WHEN `2020 Census Tract` IS NULL THEN 1 ELSE 0 END) AS nulos_2020_Census_Tract
    FROM ev_population2;
    
-- No NULL values found

-- Change the names of some columns
ALTER TABLE ev_population2
    CHANGE COLUMN `VIN (1-10)` `VIN_(1_10)` VARCHAR(255),
    CHANGE COLUMN `Postal Code` `Postal_Code` VARCHAR(255),
    CHANGE COLUMN `Model Year` `Model_Year` VARCHAR(255),
    CHANGE COLUMN `Electric Vehicle Type` `EV_Type` VARCHAR(255),
    CHANGE COLUMN `Clean Alternative Fuel Vehicle (CAFV) Eligibility` `CAFV_Eligibility` VARCHAR(255),
    CHANGE COLUMN `Electric Range` `Electric_Range` VARCHAR(255),
    CHANGE COLUMN `Base MSRP` `Base_MSRP` VARCHAR(255),
    CHANGE COLUMN `Legislative District` `Legislative_District` VARCHAR(255),
    CHANGE COLUMN `DOL Vehicle ID` `DOL_Vehicle_ID` VARCHAR(255),
    CHANGE COLUMN `Vehicle Location` `Vehicle_Location` VARCHAR(255),
    CHANGE COLUMN `Electric Utility` `Electric_Utility` VARCHAR(255),
    CHANGE COLUMN `2020 Census Tract` `2020_Census_Tract` VARCHAR(255);
    
    UPDATE ev_population2
SET CAFV_Eligibility = 
    CASE 
        WHEN CAFV_Eligibility = 'Clean Alternative Fuel Vehicle Eligible' 						THEN 'Eligible'
        WHEN CAFV_Eligibility = 'Eligibility unknown as battery range has not been researched' 	THEN 'Unknown'
        WHEN CAFV_Eligibility = 'Not eligible due to low battery range' 						THEN 'Not Eligible'
    END;
    
    UPDATE ev_population2
SET EV_Type =
	CASE
		WHEN EV_Type = 'Plug-in Hybrid Electric Vehicle (PHEV)' THEN 'HYBRID'
		WHEN EV_Type = 'Battery Electric Vehicle (BEV)' THEN 'ELECTRIC'
		ELSE EV_Type
	END;

    -- DELETE the column used to find duplicates
    
    ALTER TABLE ev_population2
	DROP COLUMN row_num;
    
    -- Review Table
    
        SELECT DISTINCT CAFV_Eligibility
		FROM ev_population2
        ORDER BY 1;
        
		SELECT *
		FROM ev_population2;
 
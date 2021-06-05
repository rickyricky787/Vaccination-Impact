#
# Group 4d: Rafaela Peralva Gomes Da Silva and Ricky Rodriguez
# Problem Statement: Vaccination Impact
#

USE csci435;

LOAD DATA LOCAL INFILE 'continent.csv'
INTO TABLE continent
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'country.csv'
INTO TABLE country
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'vaccine.csv'
INTO TABLE vaccine
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'daily_vaccination.csv'
INTO TABLE daily_vaccination
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(date_id, country_id, @date_recorded, vaccination_total)
SET date_recorded = STR_TO_DATE(@date_recorded, '%Y-%m-%d');

LOAD DATA LOCAL INFILE 'covid_data.csv'
INTO TABLE covid_data
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(date_id, @date_recorded, country_id, new_cases, new_deaths, total_cases, total_deaths)
SET date_recorded = STR_TO_DATE(@date_recorded, '%Y-%m-%d');

LOAD DATA LOCAL INFILE 'total_vaccination_by_brand.csv'
INTO TABLE total_vaccination_by_brand
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(date_id, country_id, @date_recorded, vaccine_id, vaccination_total)
SET date_recorded = STR_TO_DATE(@date_recorded, '%Y-%m-%d');

LOAD DATA LOCAL INFILE 'vaccine_brand_in_country.csv'
INTO TABLE vaccine_brand_in_country
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

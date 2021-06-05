#
# Group 4d: Rafaela Peralva Gomes Da Silva and Ricky Rodriguez
# Problem Statement: Vaccination Impact
#

USE csci435;

## Dropping tables if exists ##
DROP TABLE IF EXISTS total_vaccination_by_brand;

DROP TABLE IF EXISTS vaccine_brand_in_country;

DROP TABLE IF EXISTS covid_data;

DROP TABLE IF EXISTS daily_vaccination;

DROP TABLE IF EXISTS vaccine;

DROP TABLE IF EXISTS country;

DROP TABLE IF EXISTS continent;


### Adding tables ###

CREATE TABLE IF NOT EXISTS country (
    country_id INT AUTO_INCREMENT PRIMARY KEY,
    country_name VARCHAR(40),
    continent_id INT,
    pop_size INT
);

CREATE TABLE IF NOT EXISTS continent (
    continent_id INT AUTO_INCREMENT PRIMARY KEY,
    continent_name VARCHAR(40)
);

CREATE TABLE IF NOT EXISTS vaccine (
    vaccine_id INT AUTO_INCREMENT PRIMARY KEY,
    vaccine_name VARCHAR(40),
    doses INT
);

CREATE TABLE IF NOT EXISTS daily_vaccination (
    date_id INT AUTO_INCREMENT PRIMARY KEY,
    country_id INT,
    date_recorded DATE,
    vaccination_total INT
);

CREATE TABLE IF NOT EXISTS covid_data (
    date_id INT AUTO_INCREMENT PRIMARY KEY,
    date_recorded DATE,
    country_id INT,
    new_cases INT,
    new_deaths INT,
    total_cases INT,
    total_deaths INT
);

CREATE TABLE IF NOT EXISTS total_vaccination_by_brand (
    date_id INT AUTO_INCREMENT PRIMARY KEY,
    country_id INT,
    date_recorded DATE,
    vaccine_id INT,
    vaccination_total INT
);

CREATE TABLE IF NOT EXISTS vaccine_brand_in_country (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_id INT,
    vaccine_id INT
);

### Adding foreign keys for tables ###

ALTER TABLE country ADD (
    FOREIGN KEY (continent_id) REFERENCES continent (continent_id)
    ON DELETE SET NULL
);


ALTER TABLE daily_vaccination ADD (
    FOREIGN KEY (country_id) REFERENCES country (country_id)
    ON DELETE SET NULL
);

ALTER TABLE covid_data ADD (
    FOREIGN KEY (country_id) REFERENCES country (country_id)
    ON DELETE SET NULL
);

ALTER TABLE total_vaccination_by_brand ADD (
    FOREIGN KEY (country_id) REFERENCES country (country_id),
    FOREIGN KEY (vaccine_id) REFERENCES vaccine (vaccine_id)
    ON DELETE SET NULL
);

ALTER TABLE vaccine_brand_in_country ADD (
    FOREIGN KEY (country_id) REFERENCES country (country_id),
    FOREIGN KEY (vaccine_id) REFERENCES vaccine (vaccine_id)
    ON DELETE SET NULL
);
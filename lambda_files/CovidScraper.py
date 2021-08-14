import pandas as pd
import numpy as np
from github import Github

# CovidScrapper
class CovidScraper:
    def __init__(self, github_key):
        self.__API_KEY = github_key
    
    def scrape(self):
        # Function to replace continent name with continent id
        def getContinentId(x):
            if str(x) in continent_dict.keys():
                return continent_dict[str(x)]

        # Function to fix vaccine names
        def fix_vaccines(x):
            if "Sinopharm/Wuhan" in str(x) or "Sinopharm/Beijing" in str(x):
                return "Sinopharm"
            elif "Pfizer/ BioNTech" in str(x):
                return "Pfizer/BioNTech"
            else:
                return str(x)

        # Function to replace vaccine name with vaccine id
        def getVaccineId(x):
            if str(x) in vaccine_dict.keys():
                return vaccine_dict[str(x)]

        # Function to replace country name with country id
        def getCountryId(x):
            if str(x) in country_dict.keys():
                return country_dict[str(x)]


        ### Creating continent.csv ###
        country_df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/locations.csv")

        country_df = country_df.dropna()
        country_df = country_df.reset_index(drop=True)

        continent_df = country_df.drop(columns=["location", "Country/Region", "population_year", "population"])
        continent_df = continent_df.drop_duplicates(ignore_index = True)

        # We shift index by 1 in order to input csv into MySQL
        continent_df.index = continent_df.index + 1

        continent_df.to_csv("/tmp/continent.csv")
        print("Created 'continent.csv'")


        ### Creating country.csv ###
        country_df = country_df.drop(columns=["Country/Region", "population_year"])
        # Fix population data type
        country_df = country_df.astype({'population': 'int'})
        # replace continent with continent_id
        continent_dict = dict()
        for i in range(len(continent_df)):
            continent_name = continent_df.loc[i + 1, "continent"]
            continent_dict[continent_name] = i + 1

        country_df.continent = country_df.continent.apply(getContinentId)

        country_df.index = country_df.index + 1

        country_df.to_csv("/tmp/country.csv")
        print("Created 'country.csv'")

        ### Merging vaccine data per country data from Github into one dataframe called world_df ###
        g = Github(self.__API_KEY )

        repo = g.get_repo("owid/covid-19-data")
        file_list = repo.get_contents("public/data/vaccinations/country_data")
        github_path = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/country_data/"
        for i in range(len(file_list)):
            csv_file = str(file_list[i]).split("/")[-1].split(".")[0]+ ".csv"
            csv_file = csv_file.replace(" ", "%20")
            file_list[i] = github_path + csv_file
        
        dataframe_list = []

        for file in file_list:
            df = pd.read_csv(file)
            dataframe_list.append(df)

        world_df = pd.concat(dataframe_list, ignore_index=True)

        world_df = world_df.drop(columns=["source_url"])

        # Fixing vaccine column
        explode_df = world_df.assign(vaccine=world_df.vaccine.str.split(", ")).explode("vaccine", ignore_index=True)
        explode_df.vaccine = explode_df.vaccine.apply(fix_vaccines)

        ### Creating vaccine.csv ###
        vaccine_df = explode_df.drop(columns=["location", "date", "total_vaccinations", "people_vaccinated", "people_fully_vaccinated", "people_partly_vaccinated"])
        vaccine_df.vaccine.unique().tolist()
        vaccine_df = vaccine_df.drop_duplicates(ignore_index = True)

        vaccine_df.index = vaccine_df.index + 1

        vaccine_df.to_csv("/tmp/vaccine.csv")
        print("Created 'vaccines.csv'")

        ### Creating vaccine_brand_in_country.csv ###
        brand_df = explode_df.drop(columns=["date", "total_vaccinations", "people_vaccinated", "people_fully_vaccinated", "people_partly_vaccinated"])
        brand_df = brand_df.drop_duplicates(ignore_index=True)

        # Creating vaccine dictionary to replace vaccine name with its id
        vaccine_dict = dict()
        for i in range(len(vaccine_df)):
            vaccine_name = vaccine_df.loc[i + 1, "vaccine"]
            vaccine_dict[vaccine_name] = i + 1

        # Replace vaccine name with vaccine_id
        brand_df.vaccine = brand_df.vaccine.apply(getVaccineId)

        # Creating vaccine dictionary to replace country name with its id
        country_dict = dict()
        for i in range(len(country_df)):
            country_name = country_df.loc[i + 1, "location"]
            country_dict[country_name] = i + 1

        # Replacing country name with country_id
        brand_df.location = brand_df.location.apply(getCountryId)

        brand_df = brand_df.dropna()
        brand_df = brand_df.reset_index(drop=True)
        brand_df = brand_df.astype({"location": "int"})

        brand_df.index = brand_df.index + 1

        brand_df.to_csv("/tmp/vaccine_brand_in_country.csv")
        print("Created 'vaccine_brand_in_country.csv'")

        ### Creating total_vaccination_by_brand.csv ###
        vax_brand_df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations-by-manufacturer.csv")

        # Getting id's
        vax_brand_df.location = vax_brand_df.location.apply(getCountryId)
        vax_brand_df.vaccine = vax_brand_df.vaccine.apply(getVaccineId)

        vax_brand_df.index = vax_brand_df.index + 1

        vax_brand_df.to_csv("/tmp/total_vaccination_by_brand.csv")
        print("Created 'total_vaccination_by_brand.csv'")


        ### Creating daily_vaccination.csv ###
        daily_df = world_df.drop(columns=["vaccine", "total_vaccinations", "people_fully_vaccinated", "people_partly_vaccinated"])
        daily_df.location = daily_df.location.apply(getCountryId)
        daily_df = daily_df.dropna()
        daily_df = daily_df.reset_index(drop=True)
        daily_df = daily_df.astype({'people_vaccinated': 'int'})
        daily_df = daily_df.astype({'location': 'int'})

        daily_df.index = daily_df.index + 1

        daily_df.to_csv("/tmp/daily_vaccination.csv")
        print("Created 'daily_vaccination.csv'")


        ### Creating covid_data.csv ###
        covid_df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/full_data.csv")
        covid_df = covid_df.drop(columns=["weekly_cases", "weekly_deaths", "biweekly_cases", "biweekly_deaths"])
        covid_df = covid_df.astype({'new_cases': 'Int64'})
        covid_df = covid_df.astype({'new_deaths': 'Int64'})
        covid_df = covid_df.astype({'total_cases': 'Int64'})
        covid_df = covid_df.astype({'total_deaths': 'Int64'})

        covid_df = covid_df.astype({'new_cases': 'object'})
        covid_df = covid_df.astype({'new_deaths': 'object'})
        covid_df = covid_df.astype({'total_cases': 'object'})
        covid_df = covid_df.astype({'total_deaths': 'object'})

        covid_df.location = covid_df.location.apply(getCountryId)
        covid_df = covid_df.dropna(subset=['location'])
        covid_df = covid_df.astype({'location': 'int'})

        covid_df.index = covid_df.index + 1
        covid_df.fillna('\\N', inplace=True)

        covid_df.to_csv("/tmp/covid_data.csv") # Remove header for SQL
        print("Created 'covid_data.csv'")

        


import os
from CovidScraper import *
from database import connectToDatabase
import pymysql

def read_queries(file):
    query = ""
    for line in open(file):
        if line[0] != "#":
            query += line
    commands = query.split(';')
    commands.pop(-1)
    return commands

def run_queries(con, commands):
    cur = con.cursor()
    for line in commands:
        try:
            cur.execute(line)
        except IOError:
            print("Skipped a command")

def lambda_handler(event, context):
    # Scrape "Our World In Data" repo from Github, normalize it, and save data as csv files.
    key = os.environ.get("GITHUB_TOKEN")
    owid_repo = CovidScraper(key)
    owid_repo.scrape()

    # Connecting to database
    con = connectToDatabase()
    print("Connection to database successful")

    # Reading and excecuting queries from ddl file
    commands = read_queries("ddl.sql")
    print("Excecuting ddl.sql commands")
    run_queries(con, commands)

    # Reading and excecuting queries from dml file
    commands = read_queries("dml.sql")
    print("Excecuting dml.sql commands")
    run_queries(con, commands)

    con.commit()

    return "Complete!"



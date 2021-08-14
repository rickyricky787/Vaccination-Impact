import os
import pymysql
from dotenv import load_dotenv, find_dotenv

def connectToDatabase():

    load_dotenv(find_dotenv())

    HOST = os.environ.get("HOST")
    USER = os.environ.get("USERNAME")
    PASSWORD = os.environ.get("PASSWORD")
    DATABASE = os.environ.get("DATABASE")

    # Connecting to database
    db = pymysql.connect(
        host = HOST, 
        user = USER, 
        password = PASSWORD, 
        database = DATABASE,
        local_infile = True
        )

    return db
import os
from dotenv import load_dotenv, find_dotenv
import pymysql

def connectToDatabase():

    # To get keys from .env files
    load_dotenv(find_dotenv())

    HOST = os.environ.get("HOST")
    USER = os.environ.get("USER_NAME")
    PASSWORD = os.environ.get("PASSWORD")
    DATABASE = os.environ.get("DATABASE")

    # Connecting to database
    db = pymysql.connect(host = HOST, user = USER, password = PASSWORD, database = DATABASE)

    return db
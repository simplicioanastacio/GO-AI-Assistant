# db/db.py
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Root@123",
    "database": "go_assis_db",
    "port": 3306
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

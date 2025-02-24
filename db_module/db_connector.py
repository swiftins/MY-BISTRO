import sqlite3
import psycopg
import mysql.connector
from .config import DB_CONFIG

class DBConnector:
    def __init__(self, db_type):
        self.db_type = db_type
        self.connection = None

    def connect(self):
        if self.db_type == 'sqlite':
            self.connection = sqlite3.connect(DB_CONFIG['sqlite']['database'])
        elif self.db_type == 'postgresql':
            self.connection = psycopg.connect(
                dbname=DB_CONFIG['postgresql']['database'],
                user=DB_CONFIG['postgresql']['user'],
                password=DB_CONFIG['postgresql']['password'],
                host=DB_CONFIG['postgresql']['host'],
                port=DB_CONFIG['postgresql']['port']
            )
        elif self.db_type == 'mysql':
            self.connection = mysql.connector.connect(
                database=DB_CONFIG['mysql']['database'],
                user=DB_CONFIG['mysql']['user'],
                password=DB_CONFIG['mysql']['password'],
                host=DB_CONFIG['mysql']['host'],
                port=DB_CONFIG['mysql']['port']
            )
        else:
            raise ValueError("Unsupported database type")

    def get_connection(self):
        if not self.connection:
            self.connect()
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

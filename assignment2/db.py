import mysql.connector
import config


def get_connection():
    return mysql.connector.connect(**config.DB_CONFIG)

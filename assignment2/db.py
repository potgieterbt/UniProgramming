# import mysql
import mariadb
import config


def get_connection():
    return mariadb.connect(**config.DB_CONFIG)

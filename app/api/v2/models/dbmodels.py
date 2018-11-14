'''All database operations are handled here'''
import os
from flask import json
import psycopg2
from instance.config import Config


class Dtb():
    '''Create connection to the database'''

    def __init__(self):
        '''Get the connection variables'''
        self.db_name = Config.DB_NAME
        self.db_host = Config.DB_HOST
        self.db_user = Config.DB_USER
        self.db_password = Config.DB_PASSWORD
        self.conn = None

    def connection(self):
        '''Create a connection'''
        try:
            if os.getenv("APP_SETTINGS") == "testing":
                self.conn = psycopg2.connect(database="test_dtb",
                                             password=self.db_password,
                                             user=self.db_user,
                                             host=self.db_host
                                             )
            if os.getenv("APP_SETTINGS") == "development":
                self.conn = psycopg2.connect(
                    database=self.db_name,
                    password=self.db_password,
                    user=self.db_user,
                    host=self.db_host
                )
            self.conn = psycopg2.connect(
                os.environ['DATABASE_URL'], sslmode='require')

        except Exception as exception:
            print(exception)
        return self.conn

    def create_tables(self):
        '''Create tables in the database'''
        tables = [

            """
            CREATE TABLE IF NOT EXISTS users (
            user_id serial PRIMARY KEY,
            username varchar(30) not null,
            email varchar(50) not null,
            password varchar(250) not null,
            role varchar(10) not null)
            """,
            """
            CREATE TABLE IF NOT EXISTS products (
            product_id serial PRIMARY KEY,
            title varchar(30) not null,
            description varchar(100) not null,
            category varchar(30) not null,
            price float(4) not null,
            quantity int not null,
            lower_inventory int not null)
            """,
            """
            CREATE TABLE IF NOT EXISTS sales (sale_id serial PRIMARY KEY,
            attendant_id int REFERENCES users(user_id) not null,
            quantity_sold int not null,
            product_id int REFERENCES products(product_id) ON DELETE CASCADE)
            """,
            """
            CREATE TABLE IF NOT EXISTS token_blacklist
            (token_id serial PRIMARY KEY,
            invalid_token text not null)
            """
        ]
        try:
            cur = self.connection().cursor()
            for table in tables:
                cur.execute(table)
        except Exception as exception:
            print(exception)
        self.conn.commit()
        self.conn.close()

    def destroy_tables(self):
        '''Called in the tearDown to destroy the tables'''
        cur = self.connection().cursor()

        sql = [
            "DROP TABLE IF EXISTS users CASCADE",
            "DROP TABLE IF EXISTS products_sales CASCADE",
            "DROP TABLE IF EXISTS products CASCADE",
            "DROP TABLE IF EXISTS sales CASCADE"
        ]
        for query in sql:
            cur.execute(query)
        self.conn.commit()
        self.conn.close()

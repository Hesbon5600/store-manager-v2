import os
from datetime import datetime
import psycopg2
from flask import jsonify, make_response
from instance.config import Config
from werkzeug.security import generate_password_hash


class Dtb():
    def __init__(self):
        self.db_name = Config.DB_NAME
        self.db_host = Config.DB_HOST
        self.db_user = Config.DB_USER
        self.db_password = Config.DB_PASSWORD
        self.conn = None

    def connection(self):
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

        except Exception as e:
            print(e)
        return self.conn

    def create_tables(self):
        tables = [

            """
            CREATE TABLE IF NOT EXISTS users (user_id serial PRIMARY KEY,
            username varchar(30) not null,
            email varchar(50) not null,
            password varchar(250) not null,
            role varchar(10) not null)
            """,
            """
                CREATE TABLE IF NOT EXISTS products (product_id serial PRIMARY KEY,
                title varchar(30) not null,
                description varchar(100) not null,
                category varchar(30) not null,
                price float(4) not null,
                quantity int not null,
                lower_inventory int not null)
            """,

            """
                CREATE TABLE IF NOT EXISTS sales (sale_id serial PRIMARY KEY,
                user_id int REFERENCES users(user_id) not null,
                product_id int REFERENCES products(product_id) not null)
            """
        ]
        try:
            cur = self.connection().cursor()
            for table in tables:
                cur.execute(table)
        except Exception as e:
            print(e)
        self.conn.commit()
        self.conn.close()

    def destroy_tables(self):
        cur = self.connection().cursor()

        sql = [
            "DROP TABLE IF EXISTS users CASCADE",
            "DROP TABLE IF EXISTS products CASCADE",
            "DROP TABLE IF EXISTS sales CASCADE"
        ]
        for query in sql:
            cur.execute(query)
        self.conn.commit()
        self.conn.close()


class User(Dtb):
    def __init__(self, data=None):
        if data:
            # print(data)
            self.username = data['username']
            self.password = generate_password_hash(data['password'])
            self.email = data['email']
            self.role = data['role']
            db = Dtb()
            db.create_tables()

            self.conn = db.connection()

    def save_user(self):
        cur = self.conn.cursor()

        cur.execute(
            "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
            (self.username, self.email, self.password, self.role)
        )
        self.conn.commit()
        self.conn.close()

    def get_all_users(self):
        db = Dtb()
        self.conn = db.connection()
        db.create_tables()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users")
        result = cur.fetchall()
        users = []
        single_user = {}

        for user in result:
            single_user['user_id'] = user[0]
            single_user["username"] = user[1]
            single_user["email"] = user[2]
            single_user["password"] = user[3]
            single_user['role'] = user[4]
            users.append(single_user)

        self.conn.close()
        return users


class PostProduct():

    def save_product(self, data):
        self.title = data['title']
        self.category = data['category']
        self.description = data['description']
        self.quantity = data['quantity']
        self.price = data['price']
        self.lower_inventory = data['lower_inventory']
        db = Dtb()
        db.create_tables()
        self.conn = db.connection()

        cur = self.conn.cursor()

        cur.execute(
            "INSERT INTO products (title, description, category, price, quantity, lower_inventory) VALUES (%s, %s, %s, %s, %s, %s)",
            (self.title, self.description, self.category, self.price,
             self.quantity, self.lower_inventory),
        )
        self.conn.commit()
        self.conn.close()

    def get_all_products(self):
        db = Dtb()
        self.conn = db.connection()
        db.create_tables()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM products")
        result = cur.fetchall()
        products = []
        single_product = {}

        for product in result:
            single_product['product_id'] = product[0]
            single_product["title"] = product[1]
            single_product["description"] = product[2]
            single_product["quantity"] = product[3]
            single_product['lower_inventory'] = product[4]
            products.append(single_product)

        self.conn.close()
        return products

    def update_product(self, data, productId):
        self.title = data['title']
        self.category = data['category']
        self.description = data['description']
        self.quantity = data['quantity']
        self.price = data['price']
        self.lower_inventory = data['lower_inventory']
        self.poductID = productId

        db = Dtb()
        self.conn = db.connection()
        db.create_tables()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM products WHERE title = %s ", (self.title,))
        row = cur.fetchall()
        if row:
            return make_response(jsonify({"message": "Item with the title already exists"}), 400)
        cur.execute(
            "UPDATE products SET title = %s , description = %s, category = %s, price = %s, quantity = %s, lower_inventory = %s WHERE product_id = %s",
            (self.title, self.description, self.category, self.price,
             self.quantity, self.lower_inventory, self.poductID)
        )
        self.conn.commit()
        self.conn.close()
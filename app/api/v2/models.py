'''All database operations are handled here'''
import os
from datetime import datetime
import psycopg2
from flask import abort
from werkzeug.security import generate_password_hash
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
            product_id int REFERENCES products(product_id) not null)
            """,
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


class User(Dtb):
    '''Save, get and update users'''
    def __init__(self, data=None):
        '''Get the user  data'''
        if data:
            self.username = data['username'].strip()
            self.password = generate_password_hash(data['password'].strip())
            self.email = data['email'].strip()
            self.role = data['role'].strip()
            db_obj = Dtb()

            self.conn = db_obj.connection()

    def save_user(self):
        '''Save the users information in the database'''
        db_obj = Dtb()
        cur = self.conn.cursor()

        cur.execute(
            "INSERT INTO users (username, email,\
            password, role) VALUES (%s, %s, %s, %s)",
            (self.username, self.email, self.password, self.role),
        )
        self.conn.commit()
        self.conn.close()

    def get_all_users(self):
        '''Retrieve all users'''
        db_obj = Dtb()
        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users")
        result = cur.fetchall()
        users = []
        for user in result:
            single_user = {}
            single_user['user_id'] = user[0]
            single_user["username"] = user[1]
            single_user["email"] = user[2]
            single_user["password"] = user[3]
            single_user['role'] = user[4]
            users.append(single_user)

        self.conn.close()
        return users

    def update_user(self, user_id):
        '''Update user role to admin'''
        db_obj = Dtb()
        self.role = 'admin'
        self.user_id = user_id
        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        cur.execute(
            """UPDATE users SET role = %s WHERE user_id = %s""",
            (self.role, self.user_id),
        )

        self.conn.commit()
        self.conn.close()


class PostProduct():
    '''Save, get, and update products'''
    def __init__(self, data=None):
        '''Get the product data'''
        if data:
            self.title = data['title']
            self.category = data['category']
            self.description = data['description']
            self.quantity = data['quantity']
            self.price = data['price']
            self.lower_inventory = data['lower_inventory']

    def save_product(self):
        '''Insert the product data in the database'''
        db_obj = Dtb()
        self.conn = db_obj.connection()

        cur = self.conn.cursor()

        cur.execute(
            "INSERT INTO products (title, description, category,\
            price, quantity, lower_inventory) VALUES (%s, %s, %s, %s, %s, %s)",
            (self.title, self.description, self.category, self.price,
             self.quantity, self.lower_inventory),
        )
        self.conn.commit()
        self.conn.close()

    def get_all_products(self):
        '''Get all the products from DB'''
        db_obj = Dtb()
        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM products")
        result = cur.fetchall()
        products = []

        for product in result:
            single_product = {}
            single_product['product_id'] = product[0]
            single_product["title"] = product[1]
            single_product["description"] = product[2]
            single_product['category'] = product[3]
            single_product['price'] = product[4]
            single_product["quantity"] = product[5]
            single_product['lower_inventory'] = product[6]
            products.append(single_product)

        self.conn.close()
        return products

    def update_product(self, product_id):
        '''Update a product'''
        db_obj = Dtb()
        self.product_id = product_id

        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM products WHERE title = %s", (self.title,))
        row = cur.fetchall()
        if row:
            message = "the title '" + self.title + "' is already in use"
            abort(406, message)

        cur.execute(
            """UPDATE products SET title = %s, category = %s,
            price = %s, quantity = %s, lower_inventory = %s, description = %s
            WHERE product_id = %s""", (self.title, self.category, self.price,
                                       self.quantity, self.lower_inventory,
                                       self.description, self.product_id),
        )

        self.conn.commit()
        self.conn.close()

    def update_sold_product(self, data, product_id):
        '''Update sold product'''
        db_obj = Dtb()
        self.product_id = product_id
        self.title = data['title']
        self.category = data['category']
        self.description = data['description']
        self.quantity = data['quantity']
        self.price = data['price']
        self.lower_inventory = data['lower_inventory']
        self.product_id = product_id

        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        cur.execute(
            """UPDATE products SET title = %s, category = %s,
            price = %s, quantity = %s, lower_inventory = %s, description = %s
            WHERE product_id = %s""", (self.title, self.category, self.price,
                                       self.quantity, self.lower_inventory,
                                       self.description, self.product_id),
        )

        self.conn.commit()
        self.conn.close()

    def delete_product(self, product_id):
        '''Delete a product from the database'''
        self.product_id = product_id
        db_obj = Dtb()
        self.conn = db_obj.connection()
        db_obj.create_tables()
        cur = self.conn.cursor()

        # delete a product
        try:
            cur.execute(
                "DELETE FROM products WHERE product_id = %s",
                (self.product_id, )
            )
        except Exception as exception:
            print(exception)
        self.conn.commit()
        self.conn.close()


class PostSale(Dtb):
    '''Post, and get sales from the database'''
    def __init__(self, new_sale=None):
        '''Get the values from user input'''
        if new_sale:
            self.attendant_id = new_sale['attendant_id']
            self.product_id = new_sale['product_id']
            self.product_quantity = new_sale['product_quantity']

    def get_all_sales(self):
        '''Get sales from the database'''
        db_obj = Dtb()
        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        cur.execute("SELECT products.product_id, products.title,\
        products.description, products.category, products.price,\
        users.user_id, users.username, sales.sale_id\
        FROM products JOIN sales ON\
        products.product_id=sales.product_id JOIN users ON\
        users.user_id=sales.attendant_id")
        # cur.execute("SELECT * FROM sales")
        result = cur.fetchall()
        sales = []

        for sale in result:
            single_sale = {}
            single_sale['product_id'] = sale[0]
            single_sale['product_title'] = sale[1]
            single_sale['product_description'] = sale[2]
            single_sale['product_category'] = sale[3]
            single_sale["product_price"] = sale[4]
            single_sale['attendant_id'] = sale[5]
            single_sale['attendant_name'] = sale[6]
            single_sale['sale_id'] = sale[7]
            sales.append(single_sale)

        self.conn.close()
        return sales

    def save_sale(self):
        '''Populate the sales table'''
        db_obj = Dtb()
        db_obj.create_tables()
        self.conn = db_obj.connection()

        cur = self.conn.cursor()

        cur.execute(
            "INSERT INTO sales (attendant_id, product_id) VALUES (%s, %s)",
            (self.attendant_id, self.product_id),
        )
        cur.execute(
            "SELECT * FROM sales WHERE product_id = %s", (self.product_id,))
        row = cur.fetchall()
        self.conn.commit()
        self.conn.close()

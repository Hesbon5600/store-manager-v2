""""""
import os
from datetime import datetime
import psycopg2
from flask import abort
from werkzeug.security import generate_password_hash
from instance.config import Config


class Dtb:
    def __init__(self):
        self.db_name = Config.DB_NAME
        self.db_host = Config.DB_HOST
        self.db_user = Config.DB_USER
        self.db_password = Config.DB_PASSWORD
        self.conn = None

    def connection(self):
        try:
            if os.getenv("APP_SETTINGS") == "testing":
                self.conn = psycopg2.connect(
                    database="test_dtb",
                    password=self.db_password,
                    user=self.db_user,
                    host=self.db_host,
                )
            if os.getenv("APP_SETTINGS") == "development":
                self.conn = psycopg2.connect(
                    database=self.db_name,
                    password=self.db_password,
                    user=self.db_user,
                    host=self.db_host,
                )

        except Exception as exception:
            print(exception)
        return self.conn

    def create_tables(self):
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
            CREATE TABLE IF NOT EXISTS product_image_options (
            image_id serial PRIMARY KEY,
            image_url varchar(250) not null
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS products (
            product_id serial PRIMARY KEY,
            title varchar(30) not null,
            description varchar(100) not null,
            category varchar(30) not null,
            image_id int REFERENCES product_image_options(image_id) not null,
            price float(4) not null,
            quantity int not null,
            lower_inventory int not null)
            """,
            """
            CREATE TABLE IF NOT EXISTS sales (sale_id serial PRIMARY KEY,
            attendant_id int REFERENCES users(user_id) not null,
            product_id int REFERENCES products(product_id) not null,
            quantity int not null)
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
        cur = self.connection().cursor()

        sql = [
            "DROP TABLE IF EXISTS users CASCADE",
            "DROP TABLE IF EXISTS sales CASCADE",
            "DROP TABLE IF EXISTS products CASCADE",
            "DROP TABLE IF EXISTS product_image_options CASCADE",
        ]
        for query in sql:
            cur.execute(query)
        self.conn.commit()
        self.conn.close()


class User(Dtb):
    def __init__(self, data=None):
        if data:
            self.username = data["username"].strip()
            self.password = generate_password_hash(data["password"].strip())
            self.email = data["email"].strip()
            self.role = data["role"].strip()
            db_obj = Dtb()

            self.conn = db_obj.connection()

    def save_user(self):
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
        db_obj = Dtb()
        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users")
        result = cur.fetchall()
        users = []
        for user in result:
            single_user = {}
            single_user["user_id"] = user[0]
            single_user["username"] = user[1]
            single_user["email"] = user[2]
            single_user["password"] = user[3]
            single_user["role"] = user[4]
            users.append(single_user)

        self.conn.close()
        return users

    def get_single_user(self, user_id):
        db_obj = Dtb()
        self.user_id = user_id
        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = %s", (self.user_id,))
        result = cur.fetchone()
        user = {}
        user["user_id"] = result[0]
        user["username"] = result[1]
        user["email"] = result[2]
        user["password"] = result[3]
        user["role"] = result[4]

        self.conn.close()
        return user

    def update_user(self, user_id, role="admin"):
        db_obj = Dtb()
        self.role = role
        self.user_id = user_id
        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        cur.execute(
            """UPDATE users SET role = %s WHERE user_id = %s""",
            (self.role, self.user_id),
        )

        self.conn.commit()
        self.conn.close()


class PostProduct:
    def __init__(self, data=None):
        if data:
            self.title = data["title"]
            self.category = data["category"]
            self.description = data["description"]
            self.quantity = data["quantity"]
            self.price = data["price"]
            self.lower_inventory = data["lower_inventory"]
            self.image_id = data["image_id"]

    def save_product(self):
        db_obj = Dtb()
        self.conn = db_obj.connection()

        cur = self.conn.cursor()

        cur.execute(
            "INSERT INTO products (title, description, category,\
            price, quantity, lower_inventory, image_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                self.title,
                self.description,
                self.category,
                self.price,
                self.quantity,
                self.lower_inventory,
                self.image_id,
            ),
        )
        self.conn.commit()
        self.conn.close()

    def get_all_products(self):
        db_obj = Dtb()
        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        # select product with image_urls
        cur.execute("SELECT products.*, product_image_options.image_url FROM products JOIN product_image_options ON products.image_id = product_image_options.image_id")
        result = cur.fetchall()
        products = []

        for product in result:
            single_product = {}
            single_product["product_id"] = product[0]
            single_product["title"] = product[1]
            single_product["description"] = product[2]
            single_product["category"] = product[3]
            single_product["price"] = product[4]
            single_product["quantity"] = product[5]
            single_product["lower_inventory"] = product[6]
            single_product["image_url"] = product[8]
            products.append(single_product)

        self.conn.close()
        return products

    def get_single_product(self, product_id):
        db_obj = Dtb()
        self.product_id = product_id
        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM products WHERE product_id = %s", (self.product_id,))
        result = cur.fetchone()
        product = {}
        product["product_id"] = result[0]
        product["title"] = result[1]
        product["description"] = result[2]
        product["category"] = result[3]
        product["price"] = result[4]
        product["quantity"] = result[5]
        product["lower_inventory"] = result[6]

        self.conn.close()
        return product

    def update_product(self, product_id):
        db_obj = Dtb()
        self.product_id = product_id

        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM products WHERE title = %s", (self.title,))
        row = cur.fetchone()
        if row and row[0] != self.product_id:
            message = "the title '" + self.title + "' is already in use"
            abort(406, message)

        cur.execute(
            """UPDATE products SET title = %s, category = %s,
            price = %s, quantity = %s, lower_inventory = %s, description = %s
            WHERE product_id = %s""",
            (
                self.title,
                self.category,
                self.price,
                self.quantity,
                self.lower_inventory,
                self.description,
                self.product_id,
            ),
        )

        self.conn.commit()
        self.conn.close()

        return self.get_single_product(self.product_id)

    def update_sold_product(self, data, product_id):
        db_obj = Dtb()
        self.product_id = product_id
        self.title = data["title"]
        self.category = data["category"]
        self.description = data["description"]
        self.quantity = data["quantity"]
        self.price = data["price"]
        self.lower_inventory = data["lower_inventory"]
        self.product_id = product_id

        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        cur.execute(
            """UPDATE products SET title = %s, category = %s,
            price = %s, quantity = %s, lower_inventory = %s, description = %s
            WHERE product_id = %s""",
            (
                self.title,
                self.category,
                self.price,
                self.quantity,
                self.lower_inventory,
                self.description,
                self.product_id,
            ),
        )

        self.conn.commit()
        self.conn.close()

    def delete_product(self, product_id):
        self.product_id = product_id
        db_obj = Dtb()
        self.conn = db_obj.connection()
        cur = self.conn.cursor()

        # delete a product
        try:
            cur.execute(
                "DELETE FROM products WHERE product_id = %s", (self.product_id,)
            )
        except Exception as exception:
            print(exception)
        self.conn.commit()
        self.conn.close()


class PostSale(Dtb):

    def get_single_sale(self, sale_id):
        db_obj = Dtb()
        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        # sale_id, product_id, product_title, product_description, product_category, product_price, attendant_id, attendant_name
        # quantity_sold, total_price

        cur.execute(
            "SELECT products.product_id, products.title,\
        products.description, products.category, products.price,\
        users.user_id, users.username, sales.sale_id\
        FROM products JOIN sales ON\
        products.product_id=sales.product_id JOIN users ON\
        users.user_id=sales.attendant_id WHERE sales.sale_id = %s",
            (sale_id,),
        )
        result = cur.fetchone()
        breakpoint()

        single_sale = {}
        single_sale["product_id"] = result[0]
        single_sale["product_title"] = result[1]
        single_sale["product_description"] = (result[2],)
        single_sale["product_category"] = result[3]
        single_sale["product_price"] = result[4]
        single_sale["attendant_id"] = result[5]
        single_sale["attendant_name"] = result[6]
        single_sale["sale_id"] = result[7]

        self.conn.close()
        return single_sale

    def save_sale(self, new_sale):
        self.attendant_id = new_sale["attendant_id"]
        self.product_id = new_sale["product_id"]
        self.product_quantity = new_sale["product_quantity"]
        db_obj = Dtb()
        self.conn = db_obj.connection()

        cur = self.conn.cursor()

        cur.execute(
            "INSERT INTO sales (attendant_id, product_id, quantity)\
            VALUES (%s, %s, %s)",
            (self.attendant_id, self.product_id, self.product_quantity),
        )

        self.conn.commit()
        self.conn.close()

    def get_sales_by_attendant(self, attendant_id):
        db_obj = Dtb()
        self.attendant_id = attendant_id
        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        cur.execute(
            "SELECT products.product_id, products.title,\
        products.description, products.category, products.price,\
        users.user_id, users.username, sales.sale_id, sales.quantity\
        FROM products JOIN sales ON\
        products.product_id=sales.product_id JOIN users ON\
        users.user_id=sales.attendant_id WHERE users.user_id = %s",
            (self.attendant_id,),
        )
        result = cur.fetchall()
        sales = []
        for sale in result:
            single_sale = {}
            single_sale["product_id"] = sale[0]
            single_sale["product_title"] = sale[1]
            single_sale["product_description"] = sale[2]
            single_sale["product_category"] = sale[3]
            single_sale["product_price"] = sale[4]
            single_sale["attendant_id"] = sale[5]
            single_sale["attendant_name"] = sale[6]
            single_sale["sale_id"] = sale[7]
            single_sale["quantity_sold"] = sale[8]
            single_sale["total_price"] = sale[8] * sale[4]
            sales.append(single_sale)

        self.conn.close()
        return sales

    def get_all_sales(self):
        db_obj = Dtb()
        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        cur.execute(
            "SELECT products.product_id, products.title,\
        products.description, products.category, products.price,\
        users.user_id, users.username, sales.sale_id, sales.quantity\
        FROM products JOIN sales ON\
        products.product_id=sales.product_id JOIN users ON\
        users.user_id=sales.attendant_id"
        )
        result = cur.fetchall()
        sales = []
        for sale in result:
            single_sale = {}
            single_sale["product_id"] = sale[0]
            single_sale["product_title"] = sale[1]
            single_sale["product_description"] = sale[2]
            single_sale["product_category"] = sale[3]
            single_sale["product_price"] = sale[4]
            single_sale["attendant_id"] = sale[5]
            single_sale["attendant_name"] = sale[6]
            single_sale["sale_id"] = sale[7]
            single_sale["quantity_sold"] = sale[8]
            single_sale["total_price"] = sale[8] * sale[4]
            sales.append(single_sale)

        self.conn.close()
        return sales


class ProductImageOptions(Dtb):
    def save_image(self, image_url):
        self.image_url = image_url
        db_obj = Dtb()
        self.conn = db_obj.connection()
        cur = self.conn.cursor()

        # save an image
        cur.execute(
            "INSERT INTO product_image_options (image_url)\
            VALUES (%s)",
            (self.image_url,),
        )

        self.conn.commit()
        self.conn.close()

    def get_all_images(self):
        db_obj = Dtb()
        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM product_image_options")
        result = cur.fetchall()
        images = []

        for image in result:
            single_image = {}
            single_image["image_id"] = image[0]
            single_image["image_url"] = image[1]
            images.append(single_image)

        self.conn.close()
        return images

    def get_single_image(self, image_id):
        db_obj = Dtb()
        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM product_image_options WHERE image_id = %s",
            (image_id,),
        )
        result = cur.fetchone()
        single_image = {}
        single_image["image_id"] = result[0]
        single_image["image_url"] = result[1]

        self.conn.close()
        return single_image

    def update_image(self, image_id, image_url):
        self.image_id = image_id
        self.image_url = image_url
        db_obj = Dtb()
        self.conn = db_obj.connection()
        cur = self.conn.cursor()

        # update an image
        cur.execute(
            "UPDATE product_image_options SET image_url = %s WHERE image_id = %s",
            (self.image_url, self.image_id),
        )

        self.conn.commit()
        self.conn.close()

    def delete_image(self, image_id):
        self.image_id = image_id
        db_obj = Dtb()
        self.conn = db_obj.connection()
        cur = self.conn.cursor()

        # delete an image
        try:
            cur.execute(
                "DELETE FROM product_image_options WHERE image_id = %s",
                (self.image_id,),
            )
        except Exception as exception:
            print(exception)
        self.conn.commit()

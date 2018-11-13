'''This module handles products in the database'''
from .dbmodels import Dtb
from ..views.productinput import ProductInput


class PostProduct(ProductInput):
    '''Save, get, and update products'''
    def __init__(self, data=None):
        super().__init__(data)

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

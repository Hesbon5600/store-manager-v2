'''This module handles sales in the database'''
from .dbmodels import Dtb


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
        products.description, sales.quantity_sold, products.quantity,\
         products.category, products.price,\
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
            single_sale['quantity_sold'] = sale[3]
            single_sale['product_quantity'] = sale[4]
            single_sale['product_category'] = sale[5]
            single_sale["product_price"] = sale[6]
            single_sale['attendant_id'] = sale[7]
            single_sale['attendant_name'] = sale[8]
            single_sale['sale_id'] = sale[9]
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
            "INSERT INTO sales (attendant_id, product_id, quantity_sold)\
             VALUES (%s, %s, %s)",
            (self.attendant_id, self.product_id, self.product_quantity),
        )
        cur.execute(
            "SELECT * FROM sales WHERE product_id = %s", (self.product_id,))
        row = cur.fetchall()
        self.conn.commit()
        self.conn.close()

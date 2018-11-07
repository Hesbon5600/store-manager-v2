'''Module for the sutup and teardown'''
import unittest
import json
from app.api.v2.models import *
from app import create_app
from instance.config import app_config


class BaseTest(unittest.TestCase):
    '''Define setup and teardown methods '''

    def setUp(self):
        # Create a database object
        self.db_object = Dtb()
        self.db_object.destroy_tables()
        self.db_object.create_tables()
        self.app = create_app(config_name="testing")
        # Creates a test client for this application.
        self.test_client = self.app.test_client()
        # Admin signup details
        self.admin_info = json.dumps({
            "username": "hes45bon",
            "password": "kdTG23@h",
            "email": "hesbon500@gmail.com",
            "role": "admin"

        })
        # Provide admin login detail
        self.admin_login_details = json.dumps({
            "username": "hes45bon",
            "password": "kdTG23@h"
        })
        # Provide attendant signup info
        self.attendant_info = json.dumps({
            "username": "hesbon",
            "email": "hesbon@gmail.com",
            "password": "Hesbon5600@",
            "role": "attendant"
        })
        self.attendant_login_info = json.dumps({
            "username": "hesbon",
            "password": "Hesbon5600@"
        })
        # Product details
        self.product = json.dumps({
            "title": "omoo",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": 1,
            "price": 20.00,
            "quantity": 3
        })
        # Sale detail
        self.sale = json.dumps({
            "product_title": "omoo",
            "product_quantity": 1
        })
        self.general_header = {
                'content-type': 'application/json'
            }
        # Signup admin
        self.signup_admin = self.test_client.post(
            "/api/v2/auth/signup",
            data=self.admin_info,
            headers=self.general_header)
        # Login admin and get the token
        login_admin = self.test_client.post(
            "/api/v2/auth/login",
            data=self.admin_login_details,
            content_type='application/json')
        self.admin_token = json.loads(login_admin.data.decode())

        # Signup attendant
        signup_attendant = self.test_client.post(
            "/api/v2/auth/signup",
            data=self.attendant_info,
            headers=self.general_header)

        login_attendant = self.test_client.post(
            "/api/v2/auth/login",
            data=self.attendant_login_info,
            content_type='application/json')
        self.attendant_token = json.loads(login_attendant.data.decode())
        self.admin_header = {
            'x-access-token': self.admin_token['token'],
            'content-type': 'application/json'
        }
        self.attendant_header = {
            'x-access-token': self.attendant_token['token'],
            'content-type': 'application/json'
        }

        self.test_client.post("/api/v2/products",
                              headers=self.admin_header,
                              data=self.product,
                              )
        self.create_sale = self.test_client.post(
            "/api/v2/sales",
            data=self.sale,
            headers=self.attendant_header)

        self.context = self.app.app_context()

    def tearDown(self):
        # Delete the created
        self.db_object.destroy_tables()

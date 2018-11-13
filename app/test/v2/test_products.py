'''Module to Test the products'''
from .base_test import *


class TestProducts(BaseTest):
    '''Tests for the products '''

    def test_admin_create_product(self):
        '''Admin can create a product '''
        product = json.dumps({
            "title": "omo",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": "1",
            "price": "20.00",
            "quantity": "2"
        })
        response = self.test_client.post(
            "/api/v2/products",
            data=product,
            headers=self.admin_header)
        self.assertEqual(response.json[
                         'message'], "Product created Successfully")
        self.assertEqual(response.status_code, 201)

    def test_attendant_create_product(self):
        '''Attendant should not be able to create a product'''
        response = self.test_client.post(
            "/api/v2/products",
            data=self.product,
            headers=self.attendant_header)
        self.assertEqual(response.json[
                         'message'], "You must be an admin")
        self.assertEqual(response.status_code, 401)

    def test_get_all_products(self):
        '''User can get all products'''
        response = self.test_client.get(
            '/api/v2/products', headers=self.attendant_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[
                         'message'], "Successfully fetched all products")

    def test_get_all_products_no_token(self):
        '''User cannot get products if not logged in'''
        response = self.test_client.get(
            '/api/v2/products')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json[
                         'message'], "Token is invalid")

    def test_description_not_string(self):
        '''Description of the products must be a string'''
        product = json.dumps({
            "title": "Kiwi",
            "category": "toilateries",
            "description": 5656,
            "lower_inventory": "1",
            "price": "20.00",
            "quantity": "2"
        })
        response = self.test_client.post(
            "/api/v2/products",
            data=product,
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json[
                         'message'], "5656 is not of type 'string'")

    def test_category_not_string(self):
        '''Category of the products must be a string'''
        product = json.dumps({
            "title": "520",
            "category": 6516,
            "description": "description for omo",
            "lower_inventory": "1",
            "price": "20.00",
            "quantity": "2"
        })
        response = self.test_client.post(
            "/api/v2/products",
            data=product,
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json[
                         'message'], "6516 is not of type 'string'")

    def test_quantity_not_int(self):
        '''Quantity of the products must be a whole number'''
        product = json.dumps({
            "title": "520",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": "1",
            "price": "20.00",
            "quantity": "50ojo0"
        })
        response = self.test_client.post(
            "/api/v2/products",
            data=product,
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json[
                         'message'], "Product quantity must be anumber")

    def test_inventory_not_int(self):
        '''Lower inventory of the products must be an integer'''
        product = json.dumps({
            "title": "520",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": "45.50",
            "price": "20.00",
            "quantity": "2"
        })
        response = self.test_client.post(
            "/api/v2/products",
            data=product,
            headers=self.admin_header)
        self.assertEqual(response.json[
                         'message'], "Product Lower inventory must be whole number")
        self.assertEqual(response.status_code, 400)

    def test_quantity_less_than_zero(self):
        '''Quantity of the products must be more than zero'''
        product = json.dumps({
            "title": "dhc",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": "1",
            "price": "20.00",
            "quantity": "-2"
        })
        response = self.test_client.post(
            "/api/v2/products",
            data=product,
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json[
                         'message'], "Product Quantity should be a positive value value")

    def test_inventory_less_than_zero(self):
        '''Lower inventory of the products must be more than zero'''
        product = json.dumps({
            "title": "520",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": "-1",
            "price": "20.00",
            "quantity": "2"
        })
        response = self.test_client.post(
            "/api/v2/products",
            data=product,
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json[
                         'message'], "Product price should be value greater than 0")

    def test_price_less_than_zero(self):
        '''Price of the products must be more than 0'''
        product = json.dumps({
            "title": "hghgvh",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": "1",
            "price": "-20.00",
            "quantity": "2"
        })
        response = self.test_client.post(
            "/api/v2/products",
            data=product,
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json[
                         'message'], "Product price should be greater than 0")

    def test_get_single_product(self):
        '''User can get a single product'''
        response = self.test_client.get(
            '/api/v2/products/1',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[
                         'message'], "Successfully fetched one product")

    def test_delete_a_products(self):
        '''Admin can delete a product'''
        response = self.test_client.delete(
            '/api/v2/products/1', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[
                         'message'], "Product deleted Successfully")

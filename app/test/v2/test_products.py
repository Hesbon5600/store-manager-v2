from .base_test import *


class TestProducts(BaseTest):

    def test_admin_create_product(self):
        product = json.dumps({
            "title": "omo",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": 1,
            "price": 20.00,
            "quantity": 2
        })
        response = self.test_client.post(
            "/api/v2/products",
            data=product,
            headers={
                'content-type': 'application/json',
                'x-access-token': self.admin_token['token']})
        self.assertEqual(response.json[
                         'Message'], "Product created Successfully")
        self.assertEqual(response.status_code, 201)

    def test_attendant_create_product(self):

        response = self.test_client.post(
            "/api/v2/products",
            data=self.product,
            headers={
                'content-type': 'application/json',
                'x-access-token': self.attendant_token['token']})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json[
                         'Message'], "You must be an admin")

    def test_get_all_products(self):
        response = self.test_client.get(
            '/api/v2/products', headers={
                'x-access-token': self.attendant_token['token']})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[
                         'Message'], "Successfully fetched all products")

    def test_get_all_products_no_token(self):
        response = self.test_client.get(
            '/api/v2/products')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json[
                         'Message'], "Token is missing, You must login first")

    def test_description_not_string(self):
        product = json.dumps({
            "title": "Kiwi",
            "category": "toilateries",
            "description": 78768,
            "lower_inventory": 1,
            "price": 20.00,
            "quantity": 2
        })
        response = self.test_client.post(
            "/api/v2/products",
            data=product,
            headers={
                'content-type': 'application/json',
                'x-access-token': self.admin_token['token']
            })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json[
                         'message'], "78768 is not of type 'string'")

    def test_category_not_string(self):
        product = json.dumps({
            "title": "520",
            "category": 65654,
            "description": "description for omo",
            "lower_inventory": 1,
            "price": 20.00,
            "quantity": 2
        })
        response = self.test_client.post(
            "/api/v2/products",
            data=product,
            headers={
                'content-type': 'application/json',
                'x-access-token': self.admin_token['token']
            })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json[
                         'message'], "65654 is not of type 'string'")

    def test_quantity_not_int(self):
        product = json.dumps({
            "title": "520",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": 1,
            "price": 20.00,
            "quantity": "500"
        })
        response = self.test_client.post(
            "/api/v2/products",
            data=product,
            headers={
                'content-type': 'application/json',
                'x-access-token': self.admin_token['token']
            })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json[
                         'message'], "'500' is not of type 'integer'")

    def test_price_not_float(self):
        product = json.dumps({
            "title": "520",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": 1,
            "price": 20,
            "quantity": 2
        })
        response = self.test_client.post(
            "/api/v2/products",
            data=product,
            headers={
                'content-type': 'application/json',
                'x-access-token': self.admin_token['token']
            })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json[
                         'message'], "Product price must be of the format 00.00")

    def test_inventory_not_int(self):
        product = json.dumps({
            "title": "520",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": 45.50,
            "price": 20.00,
            "quantity": 2
        })
        response = self.test_client.post(
            "/api/v2/products",
            data=product,
            headers={
                'content-type': 'application/json',
                'x-access-token': self.admin_token['token']
            })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json[
                         'message'], "45.5 is not of type 'integer'")

    def test_quantity_less_than_zero(self):
        product = json.dumps({
            "title": "dhc",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": 1,
            "price": 20.00,
            "quantity": -2
        })
        response = self.test_client.post(
            "/api/v2/products",
            data=product,
            headers={
                'content-type': 'application/json',
                'x-access-token': self.admin_token['token']
            })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json[
                         'message'], "Product Quantity should be a positive value value")

    def test_inventory_less_than_zero(self):
        product = json.dumps({
            "title": "520",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": -1,
            "price": 20.00,
            "quantity": 2
        })
        response = self.test_client.post(
            "/api/v2/products",
            data=product,
            headers={
                'content-type': 'application/json',
                'x-access-token': self.admin_token['token']
            })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json[
                         'message'], "Product price should be value greater than 0")

    def test_price_less_than_zero(self):
        product = json.dumps({
            "title": "hghgvh",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": 1,
            "price": -20.00,
            "quantity": 2
        })
        response = self.test_client.post(
            "/api/v2/products",
            data=product,
            headers={
                'content-type': 'application/json',
                'x-access-token': self.admin_token['token']
            })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json[
                         'message'], "Product price should be greater than 0")

    def test_get_single_product(self):
        response = self.test_client.get(
            '/api/v2/products/1',
            headers={
                'x-access-token': self.admin_token['token']})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[
                         'Message'], "Successfully fetched one product")

    def test_delete_a_products(self):
        response = self.test_client.delete(
            '/api/v2/products/1', headers={
                'x-access-token': self.admin_token['token']})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[
                         'Message'], "Product deleted Successfully")

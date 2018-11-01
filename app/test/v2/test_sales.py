'''Module to test the sales'''
from .base_test import *


class TestSales(BaseTest):
    '''Tests for the sales'''
    def test_post_sale_admin(self):
        '''Admin can post a sale'''
        response = self.test_client.post("/api/v2/sales",
                                         data=json.dumps({"product_title": "omoo",
                                                          "product_quantity": 1}),
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.admin_token['token']})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json[
                         'Message'], "You must be an attendant")

    def test_post_sale_attendant(self):
        '''Attendant cannot post a sale'''
        response = self.test_client.post("/api/v2/sales",
                                         data=json.dumps({"product_title": "omoo",
                                                          "product_quantity": 1}),
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.attendant_token['token']})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json[
                         'Message'], "Sale made successfully")

    def test_product_out_of_stock(self):
        '''Impossible to sell products out of stock'''
        self.test_client.post("/api/v2/sales",
                              data=json.dumps({"product_title": "omoo",
                                               "product_quantity": 1}),
                              headers={
                                  'content-type': 'application/json',
                                  'x-access-token': self.attendant_token['token']})
        response = self.test_client.post("/api/v1/sales",
                                         data=json.dumps({"product_title": "omoo",
                                                          "product_quantity": 1}),
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.attendant_token['token']})

        self.assertEqual(response.status_code, 404)

    def test_post_sale_non_existent_product(self):
        '''Non existent products cannot be userd to post a sale'''
        response = self.test_client.post("/api/v2/sales",
                                         data=json.dumps({"product_title": "salt",
                                                          "product_quantity": 1}),
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.attendant_token['token']})

        self.assertEqual(response.status_code, 404)

    def test_admin_get_all_sales(self):
        '''Admin can get all sales'''
        response = self.test_client.get('/api/v2/sales', headers={
            'x-access-token': self.admin_token['token']})
        self.assertEqual(response.status_code, 200)

    def test_attendant_get_all_sales(self):
        '''Attendant cannot get all sales'''
        response = self.test_client.get('/api/v2/sales', headers={
            'x-access-token': self.attendant_token['token']})
        self.assertEqual(response.status_code, 403)

    def test_admin_get_single_sale(self):
        '''Admin can get a single sale'''
        response = self.test_client.get('/api/v2/sales/1', headers={
            'x-access-token': self.admin_token['token']})
        self.assertEqual(response.status_code, 200)

    def test_attendant_get_single_sale(self):
        '''Attendant cannot get a single sale'''
        response = self.test_client.get('/api/v2/sales/1')
        self.assertEqual(response.status_code, 401)

from .base_test import *


class TestSales(BaseTest):

    def test_post_sale_admin(self):
        response = self.test_client.post("/api/v2/sales",
                                         data=json.dumps({"product_id": 1}),
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.admin_token['token']})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json[
                         'Message'], "Product deleted Successfully")

    def test_product_out_of_stock(self):
        self.test_client.post("/api/v2/sales",
                              data=json.dumps({"product_id": 1}),
                              headers={
                                  'content-type': 'application/json',
                                  'x-access-token': self.attendant_token['token']})
        response = self.test_client.post("/api/v1/sales",
                                         data=json.dumps({"product_id": 1}),
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.attendant_token['token']})

        self.assertEqual(response.status_code, 404)

    def test_post_sale_non_existent_product(self):
        response = self.test_client.post("/api/v2/sales",
                                         data=json.dumps({"product_id": 2}),
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.attendant_token['token']})

        self.assertEqual(response.status_code, 404)

    def test_admin_get_all_sales(self):
        response = self.test_client.get('/api/v2/sales', headers={
            'x-access-token': self.admin_token['token']})
        self.assertEqual(response.status_code, 200)

    def test_attendant_get_all_sales(self):
        response = self.test_client.get('/api/v2/sales', headers={
            'x-access-token': self.attendant_token['token']})
        self.assertEqual(response.status_code, 403)

    def test_admin_get_single_sale(self):
        response = self.test_client.get('/api/v2/sales/1', headers={
            'x-access-token': self.admin_token['token']})
        self.assertEqual(response.status_code, 200)

    def test_attendant_get_single_sale(self):
        response = self.test_client.get('/api/v2/sales/1')
        self.assertEqual(response.status_code, 401)

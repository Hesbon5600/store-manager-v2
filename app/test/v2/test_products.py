from .base_test import *


class TestProducts(BaseTest, unittest.TestCase):

    def test_admin_create_product(self):
        product = json.dumps({
            "title": "Panga Soap",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": 1,
            "price": 20.00,
            "quantity": 2
        })
        response = self.test_client.post("/api/v2/products",
                                         data=product,
                                         headers={
                                             'content-type': 'application/json',
                                            'x-access-token': self.admin_token['token']})
        # print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_attendant_create_product(self):

        response = self.test_client.post("/api/v2/products",
                                         data=self.product,
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.attendant_token['token']})
        self.assertEqual(response.status_code, 401)
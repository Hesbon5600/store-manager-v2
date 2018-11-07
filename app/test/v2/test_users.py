'''Module to test the user input'''
from .base_test import *


class TestUser(BaseTest):
    '''Define a class for the tests'''

    def test_admin__signup(self):
        '''Admin can sign up sucessfully'''
        admin_info = json.dumps({
            "username": "heSbon52",
            "email": "hesb56on@yahoo.com",
            "password": "Kipt2oo5600@",
            "role": "admin"
        })
        response = self.test_client.post(
            "/api/v2/auth/signup",
            data=admin_info,
            headers=self.general_header)
        self.assertEqual(
            response.json[
                'Message'], "User 'heSbon52' successfully registered as 'admin")

        self.assertEqual(response.status_code, 201)

    def test_attendant__signup(self):
        '''Attendant can signup successfully'''
        # Provide attendant login info
        attendant_info = json.dumps({
            "username": "hesbon2",
            "email": "hesbon2@gmail.com",
            "password": "Hesbon5600@",
            "role": "attendant"
        })
        response = self.test_client.post(
            "/api/v2/auth/signup",
            data=attendant_info,
            headers=self.general_header)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json[
                'Message'], "User 'hesbon2' successfully registered as 'attendant")

    def test_existing_username(self):
        '''An existing username cannot be used'''
        user = json.dumps({
            "username": "hesbon",
            "email": "hesbon2@gmail.com",
            "password": "Hesbon5600@",
            "role": "attendant"
        })
        response = self.test_client.post(
            "/api/v2/auth/signup", data=user,
            headers=self.general_header)
        self.assertEqual(
            response.json[
                'message'], "Username 'hesbon' already taken")
        self.assertEqual(response.status_code, 406)

    def test_missing_username(self):
        '''Username must be present during signup'''
        user = json.dumps({
            "username": "",
            "email": "hesbon2@gmail.com",
            "password": "slGG23@bha",
            "role": "admin"})
        response = self.test_client.post(
            "/api/v2/auth/signup", data=user,
            headers=self.general_header)
        self.assertEqual(response.json['message'], "Username is missing")
        self.assertEqual(response.status_code, 400)

    def test_missing_password(self):
        '''Password must be present during signup'''
        user = json.dumps({
            "username": "jdhgfjg",
            "email": "hesbon2@gmail.com",
                        "password": "",
                        "role": "admin"})
        response = self.test_client.post(
            "/api/v2/auth/signup", data=user,
            headers=self.general_header)
        self.assertEqual(response.json[
                         'message'], "Password is missing")
        self.assertEqual(response.status_code, 400)

    def test_missing_role(self):
        '''Role must be present during signup'''
        user = json.dumps({
            "username": "lskfkk",
            "email": "hesbon2@gmail.com",
                        "password": "slGG23@bha",
                        "role": ""})
        response = self.test_client.post(
            "/api/v2/auth/signup", data=user,
            headers=self.general_header)
        self.assertEqual(response.json[
                         'message'], "Role is missing")
        self.assertEqual(response.status_code, 400)

    def test_username_not_string(self):
        '''Username must be a sting'''
        user = json.dumps({
            "username": 580,
            "email": "hesbon2@gmail.com",
            "password": "slGG23@bha",
                        "role": "mister"})
        response = self.test_client.post(
            "/api/v2/auth/signup", data=user,
            headers=self.general_header)
        self.assertEqual(
            response.json[
                'message'], "580 is not of type 'string'")
        self.assertEqual(response.status_code, 400)

    def test_password_not_string(self):
        '''Password must be a sting'''
        user = json.dumps({
            "username": "ljh6",
            "email": "hesbon2@gmail.com",
            "password": 85924,
            "role": "mister"})
        response = self.test_client.post(
            "/api/v2/auth/signup", data=user,
            headers=self.general_header)
        self.assertEqual(
            response.json[
                'message'], "85924 is not of type 'string'")
        self.assertEqual(response.status_code, 400)

    def test_role_not_string(self):
        '''Role must be a sting'''
        user = json.dumps({
            "username": "ljh6",
            "email": "hesbon2@gmail.com",
            "password": "slGG23@bha",
            "role": 8925})
        response = self.test_client.post(
            "/api/v2/auth/signup", data=user,
            headers=self.general_header)
        self.assertEqual(
            response.json[
                'message'], "8925 is not of type 'string'")
        self.assertEqual(response.status_code, 400)

    def test_password_less_than_6_ch(self):
        '''Password must be at least 6 characters long'''
        user = json.dumps({
            "username": "kipt47oo",
            "email": "hesbon2@gmail.com",
                        "password": "sJ2@j",
                        "role": "admin"})
        response = self.test_client.post(
            "/api/v2/auth/signup", data=user,
            headers=self.general_header)
        self.assertEqual(
            response.json[
                'message'], "Password must be at least 6 and at most 10 ch long")
        self.assertEqual(response.status_code, 400)

    def test_password_with_no_digit(self):
        '''Password must have a digit'''
        user = json.dumps({
            "username": "kipt4afoo",
            "email": "hesbon2@gmail.com",
                        "password":  "sJ@#vbmJ@j",
                        "role": "admin"})
        response = self.test_client.post(
            "/api/v2/auth/signup", data=user,
            headers=self.general_header)
        self.assertEqual(response.json[
                         'message'], "Password must have a digit")
        self.assertEqual(response.status_code, 400)

    def test_password_with_no_uppercase(self):
        '''Password must have an uppercase letter'''
        user = json.dumps({
            "username": "kipt47oo",
            "email": "hesbon2@gmail.com",
                        "password": "shjhg@323@j",
                        "role": "admin"})
        response = self.test_client.post(
            "/api/v2/auth/signup", data=user,
            headers=self.general_header)
        self.assertEqual(
            response.json[
                'message'], "Password must have an upper case character")
        self.assertEqual(response.status_code, 400)

    def test_password_with_no_lowercase(self):
        '''Password must have a lowercase letter'''
        user = json.dumps({
            "username": "kipdst47oo",
            "email": "hesbon2@gmail.com",
                        "password": "FUYH2B@@FYT",
                        "role": "admin"})
        response = self.test_client.post(
            "/api/v2/auth/signup", data=user,
            headers=self.general_header)
        self.assertEqual(
            response.json[
                'message'], "Password must have a lower case character")
        self.assertEqual(response.status_code, 400)

    def test_password_with_no_special_ch(self):
        '''Password must have a special character'''
        user = json.dumps({
            "username": "kipt47oo",
            "email": "hesbon2@gmail.com",
                        "password": "sJ2jfDF234j",
                        "role": "admin"})
        response = self.test_client.post(
            "/api/v2/auth/signup", data=user,
            headers=self.general_header)
        self.assertEqual(response.json[
                         'message'], "Password must have one of the special charater [#@$]")
        self.assertEqual(response.status_code, 400)

    def test_password_more_than_12_ch(self):
        '''Password should be less than 12 characters long'''
        user = json.dumps({
            "username": "kiptoo45",
            "email": "hesbon2@gmail.com",
                        "password": "sJsbkhsbkkjdfnv2@j",
                        "role": "admin"})
        response = self.test_client.post(
            "/api/v2/auth/signup", data=user,
            headers=self.general_header)
        self.assertEqual(response.json[
                         'message'], "Password must be at least 6 and at most 10 ch long")
        self.assertEqual(response.status_code, 400)

    def test_attendant_login(self):
        '''Attendant can login'''
        attendant_login_details = json.dumps({
            "username": "hesbon",
                        "password": "Hesbon5600@"
        })
        response = self.test_client.post(
            "/api/v2/auth/login",
            data=attendant_login_details,
            headers=self.general_header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[
                         'Message'], "Successfully logged in as 'attendant")

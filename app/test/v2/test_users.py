from .base_test import *


class TestUser(BaseTest):
    def test_admin__signup(self):
        admin_info = json.dumps({
            "username": "heSbon52",
            "email": "hesb56on@yahoo.com",
                        "password": "Kipt2oo5600@",
                        "role": "admin"
        })
        response = self.test_client.post("/api/v2/auth/signup",
                                         data=admin_info,
                                         headers={
                                             'content-type': 'application/json'
                                         })
        # print(response.json)
        self.assertEqual(response.json[
                         'Message'], "User 'heSbon52' successfully registered as 'admin")

        self.assertEqual(response.status_code, 201)

    def test_attendant__signup(self):
        # Provide attendant login info
        attendant_info = json.dumps({
            "username": "hesbon2",
            "email": "hesbon2@gmail.com",
            "password": "Hesbon5600@",
            "role": "attendant"
        })
        response = self.test_client.post("/api/v2/auth/signup",
                                         data=attendant_info,
                                         headers={
                                             'content-type': 'application/json'
                                         })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json[
                         'Message'], "User 'hesbon2' successfully registered as 'attendant")
    def test_existing_username(self):
        user = json.dumps({
            "username": "hesbon",
            "email": "hesbon2@gmail.com",
            "password": "Hesbon5600@",
            "role": "attendant"
        })
        response = self.test_client.post("/api/v2/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(response.json[
                         'message'], "Username 'hesbon' already taken")
        self.assertEqual(response.status_code, 406)

    def test_missing_username(self):
        user = json.dumps({
            "username": "",
            "email": "hesbon2@gmail.com",
                        "password": "slGG23@bha",
                        "role": "admin"})
        response = self.test_client.post("/api/v2/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(response.json[
                         'message'], "Username is missing")
        self.assertEqual(response.status_code, 400)

    def test_missing_password(self):
        user = json.dumps({
            "username": "jdhgfjg",
            "email": "hesbon2@gmail.com",
                        "password": "",
                        "role": "admin"})
        response = self.test_client.post("/api/v2/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(response.json[
                         'message'], "Password is missing")
        self.assertEqual(response.status_code, 400)

    def test_missing_role(self):
        user = json.dumps({
            "username": "lskfkk",
            "email": "hesbon2@gmail.com",
                        "password": "slGG23@bha",
                        "role": ""})
        response = self.test_client.post("/api/v2/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(response.json[
                         'message'], "Role is missing")
        self.assertEqual(response.status_code, 400)


    def test_username_not_string(self):
        user = json.dumps({
            "username": 580,
            "email": "hesbon2@gmail.com",
            "password": "slGG23@bha",
                        "role": "mister"})
        response = self.test_client.post("/api/v2/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(response.json[
                         'message'], "Username must be a string")
        self.assertEqual(response.status_code, 400)

    def test_password_not_string(self):
        user = json.dumps({
            "username": "ljh6",
            "email": "hesbon2@gmail.com",
            "password": 85924,
            "role": "mister"})
        response = self.test_client.post("/api/v2/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(response.json[
                         'message'], "Password must be a string")
        self.assertEqual(response.status_code, 400)

    def test_role_not_string(self):
        user = json.dumps({
            "username": "ljh6",
            "email": "hesbon2@gmail.com",
            "password": "slGG23@bha",
            "role": 8925})
        response = self.test_client.post("/api/v2/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(response.json[
                         'message'], "Role must be a string")
        self.assertEqual(response.status_code, 400)

    def test_password_less_than_6_ch(self):
        user = json.dumps({
            "username": "kipt47oo",
            "email": "hesbon2@gmail.com",
                        "password": "sJ2@j",
                        "role": "admin"})
        response = self.test_client.post("/api/v2/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(response.json[
                         'message'], "Password must be at least 6 and at most 10 ch long")
        self.assertEqual(response.status_code, 400)

    def test_password_with_no_digit(self):
        user = json.dumps({
            "username": "kipt4afoo",
            "email": "hesbon2@gmail.com",
                        "password":  "sJ@#vbmJ@j",
                        "role": "admin"})
        response = self.test_client.post("/api/v2/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(response.json[
                         'message'], "Password must have a digit")
        self.assertEqual(response.status_code, 400)

    def test_password_with_no_uppercase(self):
        user = json.dumps({
            "username": "kipt47oo",
            "email": "hesbon2@gmail.com",
                        "password": "shjhg@323@j",
                        "role": "admin"})
        response = self.test_client.post("/api/v2/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(response.json[
                         'message'], "Password must have an upper case character")
        self.assertEqual(response.status_code, 400)

    def test_password_with_no_lowercase(self):
        user = json.dumps({
            "username": "kipdst47oo",
            "email": "hesbon2@gmail.com",
                        "password": "FUYH2B@@FYT",
                        "role": "admin"})
        response = self.test_client.post("/api/v2/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(response.json[
                         'message'], "Password must have a lower case character")
        self.assertEqual(response.status_code, 400)

    def test_password_with_no_special_ch(self):
        user = json.dumps({
            "username": "kipt47oo",
            "email": "hesbon2@gmail.com",
                        "password": "sJ2jfDF234j",
                        "role": "admin"})
        response = self.test_client.post("/api/v2/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(response.json[
                         'message'], "Password must have one of the special charater [#@$]")
        self.assertEqual(response.status_code, 400)

    def test_password_more_than_12_ch(self):
        user = json.dumps({
            "username": "kiptoo45",
            "email": "hesbon2@gmail.com",
                        "password": "sJsbkhsbkkjdfnv2@j",
                        "role": "admin"})
        response = self.test_client.post("/api/v2/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(response.json[
                         'message'], "Password must be at least 6 and at most 10 ch long")
        self.assertEqual(response.status_code, 400)

    def test_attendant_login(self):
        attendant_login_details = json.dumps({
            "username": "hesbon",
                        "password": "Hesbon5600@"
        })
        response = self.test_client.post("/api/v2/auth/login",
                                         data=attendant_login_details,
                                         headers={
                                             'content-type': 'application/json'
                                         })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[
                         'Message'], "Successfully logged in as 'attendant")

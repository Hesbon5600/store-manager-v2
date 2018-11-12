'''This module handles users in the database'''
from werkzeug.security import generate_password_hash
from .dbmodels import Dtb


class User(Dtb):
    '''Save, get and update users'''

    def __init__(self, data=None):
        '''Get the user  data'''
        if data:
            self.username = data['username'].strip()
            self.password = generate_password_hash(data['password'].strip())
            self.email = data['email'].strip()
            self.role = data['role'].strip()
        self.db_obj = Dtb()
        self.conn = self.db_obj.connection()
        self.cur = self.conn.cursor()

    def save_user(self):
        '''Save the users information in the database'''
        self.cur.execute(
            "INSERT INTO users (username, email,\
            password, role) VALUES (%s, %s, %s, %s)",
            (self.username, self.email, self.password, self.role),
        )
        self.conn.commit()
        self.conn.close()

    def get_all_users(self):
        '''Retrieve all users'''
        db_obj = Dtb()
        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users")
        result = cur.fetchall()
        users = []
        for user in result:
            single_user = {}
            single_user['user_id'] = user[0]
            single_user["username"] = user[1]
            single_user["email"] = user[2]
            single_user["password"] = user[3]
            single_user['role'] = user[4]
            users.append(single_user)

        self.conn.close()
        return users

    def update_user(self, user_id):
        '''Update user role to admin'''
        db_obj = Dtb()
        self.role = 'admin'
        self.user_id = user_id
        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        cur.execute(
            """UPDATE users SET role = %s WHERE user_id = %s""",
            (self.role, self.user_id),
        )

        self.conn.commit()
        self.conn.close()

    def logout(self, token):
        db_obj = Dtb()
        self.conn = db_obj.connection()
        cur = self.conn.cursor()
        try:
            cur.execute(
                "INSERT INTO token_blacklist (invalid_token)\
             VALUES (%s)",
                (token,),
            )
        except Exception as exception:
            print(exception)
        self.conn.commit()
        self.conn.close()
        return True

    def get_invalid_tokens(self, token):
        '''Retrieve all users'''
        db_obj = Dtb()
        self.conn = db_obj.connection()
        cur = self.conn.cursor()

        cur.execute("""SELECT * FROM token_blacklist WHERE\
         invalid_token = %s""",
                    (token,),)
        result = cur.fetchone()
        if result:
            return True
        self.conn.close()

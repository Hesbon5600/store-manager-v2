"""Handles all functionality of routing requests"""
from functools import wraps
import jwt
from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource
from werkzeug.security import check_password_hash
from flask_expects_json import expects_json

from instance.config import app_config
from .expected_json import *
from .models import *
from .utils import *
import datetime


def token_required(func):
    """Define a wrapper that handles decoding of the token"""
    """Identifies the user whom the token belongs to"""

    @wraps(func)
    def decorated(*args, **kwargs):
        user_obj = User()
        users = user_obj.get_all_users()
        token = None
        current_user = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            return make_response(
                jsonify({"message": "Token is missing, You must login first"}), 401
            )
        try:
            data = jwt.decode(
                token, app_config["development"].SECRET_KEY, algorithms=["HS256"]
            )

            for user in users:
                if user["username"] == data["username"]:
                    current_user = user
        except Exception as e:
            print(e)
            return make_response(jsonify({"message": "Token is invalid"}), 403)
        return func(current_user, *args, **kwargs)

    return decorated


class UserRegistration(Resource):
    """Handles user registration"""

    @expects_json(USER_REGISTRATION_JSON)
    def post(self):
        """Get data from the user, call validation method"""
        """pass the data to the User class for saving"""
        data = request.get_json()
        if not data:
            return make_response(
                jsonify({"Status": "Failed", "message": "No signup data provided"}), 400
            )

        validate = ValidateUser(data)
        validate.validate_user_details()
        user = User(data)
        user.save_user()
        return make_response(
            jsonify(
                {
                    "Status": "Ok",
                    "message": "User '"
                    + data["username"]
                    + "' successfully registered as '"
                    + data["role"],
                }
            ),
            201,
        )


class UserLogin(Resource):
    """Registered users can login"""

    @expects_json(USER_LOGIN_JSON)
    def post(self):
        """User provides username and password"""
        self.user_obj = User.get_all_users(self)
        data = request.get_json()
        username = data["username"].strip()
        password = data["password"].strip()

        if (
            not data
            or not username
            or not password
            or "username" not in data
            or "password" not in data
        ):
            return make_response(
                jsonify({"Status": "Failed", "message": "Login required"}), 400
            )

        for user in self.user_obj:
            if user["username"] == username and check_password_hash(
                user["password"], password
            ):

                token = jwt.encode(
                    {
                        "username": user["username"],
                        "email": user["email"],
                        "user_id": user["user_id"],
                        "role": user["role"],
                        "exp": datetime.datetime.utcnow()
                        + datetime.timedelta(minutes=3000),
                    },
                    app_config["development"].SECRET_KEY,
                    algorithm="HS256",
                )
                return make_response(
                    jsonify(
                        {
                            "message": "Successfully logged in as '" + user["role"],
                            "token": token.decode("UTF-8"),
                        }
                    ),
                    200,
                )

        return make_response(
            jsonify(
                {
                    "Status": "Failed",
                    "message": "No such user found. Check your login credentials",
                }
            ),
            404,
        )


class GetUsers(Resource):
    """Get all users"""

    @token_required
    def get(current_user, self):
        """Function to return the saved users from the database"""
        users = User.get_all_users(self)
        if not current_user:
            response = make_response(
                jsonify({"Status": "Failed", "message": "You must first login"}), 401
            )
        else:
            response = make_response(
                jsonify(
                    {
                        "Status": "Ok",
                        "message": "Successfully fetched all users",
                        "users": users,
                    }
                ),
                200,
            )
        return response


class PromoteUser(Resource):
    """Make an attendant to be an admin"""

    @token_required
    def put(current_user, self, user_id):
        """Takes the user_id and updates the role to admin"""
        """The initial role must be an attendant"""
        user_id = int(user_id)
        # data = request.get_json()
        if current_user and current_user["role"] != "admin":
            return make_response(
                jsonify({"Status": "Failed", "message": "You must be an admin"}), 401
            )
        user = User.get_single_user(self, user_id)

        if not user:
            return make_response(
                jsonify({"Status": "Failed", "message": "No such user"}), 404
            )

        update_user = User()
        update_user.update_user(user_id)
        return make_response(
            jsonify(
                {
                    "Status": "Ok",
                    "message": "User '"
                    + user["username"]
                    + "' has been promoted to admin",
                }
            ),
            200,
        )


class Product(Resource):
    """Deals with posting a product and\
    returning the products from db"""

    # Get all products
    @token_required
    def get(current_user, self):
        """Function to return the saved users from the database"""
        self.prod_obj = PostProduct.get_all_products(self)
        if not current_user:
            response = make_response(
                jsonify({"Status": "Failed", "message": "You must first login"}), 401
            )
        if len(self.prod_obj) < 1:
            response = make_response(
                jsonify({"Status": "Failed", "message": "No available products"}), 404
            )
        else:
            response = make_response(
                jsonify(
                    {
                        "Status": "Ok",
                        "message": "Successfully fetched all products",
                        "products": self.prod_obj,
                    }
                ),
                200,
            )

        return response

    @token_required
    @expects_json(PRODUCT_JSON, force=True)
    def post(current_user, self):
        """Take the product data and save it in a database"""
        data = request.get_json()
        if current_user and current_user["role"] != "admin":
            return make_response(
                jsonify({"Status": "Failed", "message": "You must be an admin"}), 401
            )
        if current_user and current_user["role"] == "admin":
            valid_product = ValidateProduct(data)
            valid_product.validate_duplicates()
            valid_product.validate_product_details()
            product = PostProduct(data)
            product.save_product()

            self.prod_obj = PostProduct.get_all_products(self)
            for product in self.prod_obj:
                if product["title"] == data["title"]:
                    return make_response(
                        jsonify(
                            {
                                "Status": "Ok",
                                "message": "Product created Successfully",
                                "My Products": product,
                            }
                        ),
                        201,
                    )


class SingleProduct(Resource):
    """Get a single product from the DB"""

    @token_required
    def get(current_user, self, product_id):
        """Given the product ID select a\
        product that matches it from the DB"""
        self.prod_obj = PostProduct.get_all_products(self)
        if not current_user:
            return make_response(
                jsonify({"Status": "Failed", "message": "You must be logged in first"}),
                401,
            )
        for product in self.prod_obj:
            if product["product_id"] == int(product_id):
                return make_response(
                    jsonify(
                        {
                            "Status": "Ok",
                            "message": "Successfully fetched one product",
                            "product": product,
                        }
                    ),
                    200,
                )

        return make_response(
            jsonify({"Status": "Failed", "message": "No such product"}), 404
        )

    @token_required
    @expects_json(PRODUCT_JSON)
    def put(current_user, self, product_id):
        """Update a specific product details"""
        product_id = int(product_id)
        data = request.get_json()
        if current_user and current_user["role"] != "admin":
            return make_response(
                jsonify({"Status": "Failed", "message": "You must be an admin"}), 401
            )
        if current_user and current_user["role"] == "admin":
            valid_product = ValidateProduct(data)
            valid_product.validate_product_details()
            prod_objs = PostProduct.get_all_products(self)
            product_to_update = None
            for product in prod_objs:
                if product["product_id"] == product_id:
                    product_to_update = product
                    break
            if product_to_update is None:
                return make_response(
                    jsonify({"Status": "Failed", "message": "No such product"}), 404
                )

            product = PostProduct(data)
            updated_product = product.update_product(product_id)
            return make_response(
                jsonify(
                    {
                        "Status": "Ok",
                        "message": "Product updated Successfully",
                        "products": updated_product,
                    }
                ),
                200,
            )

    @token_required
    def delete(current_user, self, product_id):
        """Delete a specific product"""
        product_id = int(product_id)
        data = request.get_json()
        if current_user and current_user["role"] != "admin":
            return make_response(
                jsonify({"Status": "Failed", "message": "You must be an admin"}), 401
            )
        if current_user and current_user["role"] == "admin":
            self.prod_obj = PostProduct.get_all_products(self)
            if len(self.prod_obj) > 0:
                for product in self.prod_obj:
                    if product["product_id"] == product_id:
                        product = PostProduct()
                        product.delete_product(product_id)
                        return make_response(
                            jsonify(
                                {
                                    "Status": "Ok",
                                    "message": "Product deleted Successfully",
                                }
                            ),
                            200,
                        )
                return make_response(
                    jsonify(
                        {
                            "Status": "Failed",
                            "message": "Product does nor exist",
                            "Avilable products": self.prod_obj,
                        }
                    ),
                    404,
                )
            return make_response(
                jsonify({"Status": "Failed", "message": "No available products"}), 404
            )


class Sale(Resource):
    """Post and get sales"""

    @token_required
    @expects_json(SALE_JSON)
    def post(current_user, self):
        """Attendant can make a sale"""
        total = 0
        data = request.get_json()
        if current_user and current_user["role"] != "attendant":
            return make_response(
                jsonify({"Status": "Failed", "message": "You must be an attendant"}),
                403,
            )
        product_id = data["product_id"]
        product = PostProduct.get_single_product(self, product_id)
        if not product:
            return make_response(
                jsonify({"Status": "Failed", "message": "Product does not exist"}), 404
            )
        product_quantity = data["product_quantity"]

        if product_quantity < 1:
            return make_response(
                jsonify(
                    {
                        "Status": "Failed",
                        "message": "You are attempting to sale less than one product",
                    }
                ),
                403,
            )

        if product_quantity > product["quantity"]:
            return make_response(
                jsonify(
                    {
                        "Status": "Failed",
                        "message": "You are attempting to sale more products than available",
                    }
                ),
                403,
            )

        attendant_id = current_user["user_id"]
        post_sale = PostSale()
        new_sale = {
            "attendant_id": attendant_id,
            "product_id": product_id,
            "product_quantity": product_quantity,
        }
        post_sale.save_sale(new_sale)
        product["quantity"] = product["quantity"] - product_quantity
        product_id = product_id
        update_prod = PostProduct()
        update_prod.update_sold_product(product, product_id)
        self.sale_obj = PostSale.get_all_sales(self)
        for sale in self.sale_obj:
            if product["product_id"] in sale.values():
                total = total + int(product["price"]) * product_quantity
        return make_response(
            jsonify(
                {
                    "Status": "Ok",
                    "message": "Sale made successfully",
                    "Remaining products": product,
                    "Total": total,
                }
            ),
            201,
        )

    # Get all sale entries
    @token_required
    def get(current_user, self):
        """Admin can get all sales"""
        if current_user and current_user["role"] == "admin":
            sales = PostSale.get_all_sales(self)

        else:
            sales = PostSale.get_sales_by_attendant(self, current_user["user_id"])
        if len(sales) > 0:
            return make_response(
                jsonify({"Status": "Ok", "message": "Success", "sales": sales}),
                200,
            )
        else:
            return make_response(
                jsonify({"Status": "Failed", "message": "No sales made"}), 404
            )


class SingleSale(Resource):
    """Getting a single sale record"""

    @token_required
    def get(current_user, self, sale_id):
        """Admin and the attendant who made the sale\
        Can view the sale record"""
        self.sale_obj = PostSale.get_all_sales(self)
        for sale in self.sale_obj:
            if current_user["role"] == "admin":
                if int(sale_id) == sale["sale_id"]:
                    return make_response(
                        jsonify({"Status": "Ok", "message": "Success", "Sale": sale}),
                        200,
                    )
            else:
                return make_response(
                    jsonify(
                        {
                            "Status": "Failed",
                            "message": "You cannor access this sale record",
                        }
                    ),
                    401,
                )
        else:
            return make_response(
                jsonify({"Status": "Failed", "message": "No such sale record"}), 404
            )


class AddListImageOptions(Resource):
    """Add and list product image options"""

    @token_required
    @expects_json(IMAGE_JSON)
    def post(current_user, self):
        """Admin can add product image options"""
        if current_user and current_user["role"] == "admin":
            data = request.get_json()
            image_url = data["image_url"]
            image = ProductImageOptions()
            image.save_image(image_url=image_url)
            return make_response(
                jsonify(
                    {
                        "Status": "Ok",
                        "message": "Image added successfully",
                        "image": image.get_all_images(),
                    }
                ),
                201,
            )
        return make_response(
            jsonify({"Status": "Failed", "message": "You must be an admin"}), 401
        )

    @token_required
    def get(current_user, self):
        """Admin can get all product image options"""
        images = ProductImageOptions.get_all_images(self)
        if len(images) > 0:
            return make_response(
                jsonify({"Status": "Ok", "message": "Success", "images": images}),
                200,
            )
        else:
            return make_response(
                jsonify({"Status": "Failed", "message": "No images available"}), 404
            )

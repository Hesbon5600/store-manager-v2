"""The predefined properties of the input fields for the app"""
PRODUCT_JSON = {
    "type": "object",
    "maxProperties": 7,
    "properties": {
        "title": {"type": "string"},
        "quantity": {"type": "integer"},
        "description": {"type": "string"},
        "category": {"type": "string"},
        "price": {"type": "integer"},
        "lower_inventory": {"type": "integer"},
        "image_id": {"type": "integer"},
    },
    "required": [
        "title",
        "price",
        "description",
        "category",
        "quantity",
        "lower_inventory",
    ],
}

USER_REGISTRATION_JSON = {
    "type": "object",
    "maxProperties": 4,
    "properties": {
        "username": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"},
        "role": {"type": "string"},
    },
    "required": ["username", "password", "email", "role"],
}

USER_LOGIN_JSON = {
    "type": "object",
    "maxProperties": 2,
    "properties": {"username": {"type": "string"}, "password": {"type": "string"}},
    "required": ["username", "password"],
}

SALE_JSON = {
    "type": "object",
    "maxProperties": 2,
    "properties": {
        "product_id": {"type": "integer"},
        "product_quantity": {"type": "integer"},
    },
    "required": ["product_id", "product_quantity"],
}

IMAGE_JSON = {
    "type": "object",
    "maxProperties": 1,
    "properties": {"image_url": {"type": "string"}},
    "required": ["image_url"],
}

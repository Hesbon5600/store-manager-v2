
PRODUCT_JSON = {
    'type': 'object',
    'maxProperties': 6,
    'properties': {
        'title': {'type': 'string'},
        'quantity': {'type': 'integer'},
        'description': {'type': 'string'},
        'category': {'type': 'string'},
        'price': {'type': 'number'},
        'lower_inventory': {'type': 'integer'},
    },
    'required': ['title', 'price', 'description',
                 'category', 'quantity', 'lower_inventory']
}

USER_REGISTRATION_JSON = {
    'type': 'object',
    'maxProperties': 4,
    'properties': {
        'username': {'type': 'string'},
        'email': {'type': 'string'},
        'password': {'type': 'string'},
        'role': {'type': 'string'}
    },
    'required': ['username', 'password', 'email', 'role']
}

USER_LOGIN_JSON = {
    'type': 'object',
    'maxProperties': 2,
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['username', 'password']
}

SALE_JSON = {
    'type': 'object',
    'maxProperties': 2,
    'properties': {
        'product_title': {'type': 'string'},
        'product_quantity': {'type': 'integer'}
    },
    'required': ['product_title', 'product_quantity']
}

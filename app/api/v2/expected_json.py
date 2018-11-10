'''The predefined properties of the input fields for the app'''
PRODUCT_JSON = {
    'type': 'object',
    'maxProperties': 6,
    'properties': {
        'title': {'type': 'string'},
        'quantity': {'type': 'string'},
        'description': {'type': 'string'},
        'category': {'type': 'string'},
        'price': {'type': 'string'},
        'lower_inventory': {'type': 'string'},
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
        'product_quantity': {'type': 'string'}
    },
    'required': ['product_title', 'product_quantity']
}

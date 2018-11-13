class ProductInput():
    def __init__(self, data=None):
        '''Get the product data'''
        if data:
            self.title = data['title']
            self.category = data['category']
            self.description = data['description']
            self.quantity = data['quantity']
            self.price = data['price']
            self.lower_inventory = data['lower_inventory']
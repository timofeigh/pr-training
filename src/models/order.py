from models.exceptions import InvlaidOrderError
from models.product import Product


class Order:
    def __init__(self, user, products, order_id=None):
        self.user = user
        self.products = products
        self.order_id = order_id

    def __str__(self):
        if self.order_id:
            return f'Заказ #{self.order_id} на сумму {self.calculate_total()} руб.(Пользователь: {self.user.name})'
        else:
            return f'Заказ на сумму {self.calculate_total()} руб. (Пользователь: {self.user.name})'
    
    def calculate_total(self):
        total = 0
        if len(self.products) == 0:
            raise InvlaidOrderError('Заказ невалиден: пустой список товаров')
        else:
            for product in self.products:
                total += product.get_total_price()
            return total
    
    def add_product(self, product):
        if isinstance(product, Product):
            self.products.append(product)

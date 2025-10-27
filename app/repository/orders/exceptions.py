class OrderException(Exception):
    pass


class ProductOutOfStockException(OrderException):
    pass


class NotEnoughProductException(OrderException):
    pass

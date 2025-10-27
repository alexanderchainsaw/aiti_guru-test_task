from dataclasses import dataclass

from .orders.repository import OrdersRepository


@dataclass
class RepositoryController:
    orders: OrdersRepository


class RepositoryControllerTransact(RepositoryController):
    pass

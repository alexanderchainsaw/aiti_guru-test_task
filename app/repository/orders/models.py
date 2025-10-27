import datetime
import decimal
from typing import Optional

from app.repository.models import SQLModel


class Category(SQLModel):
    tablename = "categories"

    id: int
    name: str
    parent_id: Optional[int]
    created_timestamp: datetime.datetime


class CategoryClosure(SQLModel):
    tablename = "category_closure"

    ancestor: int
    descendant: int
    depth: int


class BaseProduct(SQLModel):
    tablename = "products"

    id: int
    name: str
    quantity: int
    price: decimal.Decimal
    created_timestamp: datetime.datetime


class ProductRaw(BaseProduct):
    category_id: Optional[int]


class Product(BaseProduct):
    category: Category


class BaseOrderStatus(SQLModel):
    tablename = "order_statuses"

    id: int
    status_name: str
    description: Optional[str]


class BaseOrder(SQLModel):
    tablename = "orders"

    id: int
    created_at: datetime.datetime


class OrderRaw(BaseOrder):
    client_id: Optional[int]
    status_id: Optional[int]


class BaseOrderItem(SQLModel):
    tablename = "order_items"

    order_id: int
    quantity: int
    price_at_order: decimal.Decimal


class OrderItemRaw(BaseOrderItem):
    product_id: int


class OrderItem(BaseOrderItem):
    product: Product


class BaseClient(SQLModel):
    id: int
    name: str
    address: Optional[str]


class Order(BaseOrder):
    client: BaseClient
    status: BaseOrderStatus

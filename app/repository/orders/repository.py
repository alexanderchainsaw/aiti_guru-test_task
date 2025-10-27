from app.repository.exceptions import EntityDoesntExistException
from app.repository.repository import Repository

from .exceptions import NotEnoughProductException, ProductOutOfStockException
from .models import BaseOrderStatus, BaseProduct, OrderItemRaw


class OrdersRepository(Repository):

    async def _get_order_exists(self, order_id: int) -> bool:
        row = await self.fetch_row("SELECT id FROM orders WHERE id = $1", order_id)
        return bool(row)

    async def get_product_quantity_in_order(self, order_id: int, product_id: int) -> int:
        row = await self.fetch_row(
            """
            SELECT quantity FROM order_items
            WHERE order_id = $1 AND product_id = $2
            """,
            order_id,
            product_id,
        )
        if not row:
            return 0
        return row["quantity"]

    async def get_base_product(self, product_id: int) -> BaseProduct | None:
        row = await self.fetch_row(
            f"""
            SELECT {BaseProduct.build_str_values_sql()}
            FROM {BaseProduct.tablename}
            WHERE id = $1
            """,
            product_id,
        )
        if not row:
            return None
        return BaseProduct(**row)

    async def add_product_to_order(
        self, order_id: int, product_id: int, quantity: int
    ) -> OrderItemRaw:
        if not self._get_order_exists(order_id=order_id) or not (
            product := await self.get_base_product(product_id)
        ):
            raise EntityDoesntExistException
        if not product.quantity:
            raise ProductOutOfStockException
        if product.quantity < quantity:
            raise NotEnoughProductException
        await self._decrease_product_quantity(product_id=product_id, quantity=quantity)
        return await self._add_product_to_order(
            order_id=order_id, product=product, quantity=quantity
        )

    async def _add_product_to_order(
        self, order_id: int, product: BaseProduct, quantity: int
    ) -> OrderItemRaw:
        row = await self.fetch_row(
            f"""
            INSERT INTO "order_items"
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (order_id, product_id)
            DO UPDATE SET quantity = "order_items".quantity + EXCLUDED.quantity
            RETURNING {OrderItemRaw.build_str_values_sql()}
            """,
            order_id,
            product.id,
            quantity,
            product.price,
        )
        return OrderItemRaw(**row)

    async def _decrease_product_quantity(self, product_id: int, quantity: int) -> None:
        await self.fetch_row(
            """
            UPDATE products
            SET quantity = quantity - $1
            WHERE id = $2
            """,
            quantity,
            product_id,
        )

    async def get_order_statuses(self) -> list[BaseOrderStatus] | None:
        rows = await self.fetch(
            f"""
            SELECT {BaseOrderStatus.build_str_values_sql()}
            FROM {BaseOrderStatus.tablename}
            """
        )
        if not rows:
            return None
        return [BaseOrderStatus(**row) for row in rows]

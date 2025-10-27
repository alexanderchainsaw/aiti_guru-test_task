import json
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterable

from asyncpg import Connection, Pool, create_pool
from dishka import Provider, Scope, provide

from app.config import settings
from app.repository.repository_controller import RepositoryController, RepositoryControllerTransact

from .orders.repository import OrdersRepository

logger = logging.getLogger(__name__)


class RepositoryProvider(Provider):
    scope = Scope.APP

    async def init_connection(self, conn):
        await conn.set_type_codec(
            "jsonb",
            encoder=json.dumps,
            decoder=json.loads,
            schema="pg_catalog",
        )
        await conn.set_type_codec(
            "json",
            encoder=json.dumps,
            decoder=json.loads,
            schema="pg_catalog",
        )

        await conn.set_type_codec(
            "numeric",
            encoder=str,
            decoder=str,
            schema="pg_catalog",
            format="text",
        )

    @provide
    async def get_pool(self) -> AsyncIterable[Pool]:
        pool = await create_pool(
            dsn=settings.database_dsn,
            init=self.init_connection,
        )
        yield pool
        await pool.close()

    @asynccontextmanager
    async def get_transaction(
        self,
        pool: Pool,
    ) -> AsyncIterable[Connection]:
        logger.info("Getting transaction")
        connection = await pool.acquire()
        transaction = connection.transaction()
        await transaction.start()
        try:
            yield connection
            await transaction.commit()
            logger.info("Transaction commited")
        except Exception as e:
            await transaction.rollback()
            logger.info("Transaction rolled back")
            raise e
        finally:
            await pool.release(connection)

    @provide
    async def get_repo_controller(
        self,
        pool: Pool,
    ) -> RepositoryController:
        return RepositoryController(
            orders=OrdersRepository(db=pool),
        )

    @provide(scope=Scope.REQUEST)
    async def get_repo_controller_transact(
        self,
        pool: Pool,
    ) -> AsyncIterable[RepositoryControllerTransact]:

        async with self.get_transaction(pool) as con:
            yield RepositoryControllerTransact(orders=OrdersRepository(db=pool, connection=con))

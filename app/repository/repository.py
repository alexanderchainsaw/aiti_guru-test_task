from asyncpg import Connection, Pool, Record


class Repository:
    def __init__(self, db: Pool, connection: Connection | None = None,) -> None:
        self._db = db
        self._connection = connection

    async def fetch_row(
        self,
        sql: str,
        *args,
        connection: Connection | None = None,
    ) -> Record | None:
        if connection:
            row = await connection.fetchrow(sql, *args)
        else:
            async with self._db.acquire() as c:
                row = await c.fetchrow(sql, *args)
        if not row:
            return
        return row

    async def execute(
        self,
        sql: str,
        *args,
        connection: Connection | None = None,
    ):
        if connection:
            await connection.execute(sql, *args)
        else:
            async with self._db.acquire() as c:
                await c.execute(sql, *args)

    async def fetch(
        self,
        sql: str,
        *args,
        connection: Connection | None = None,
    ) -> list[Record] | None:
        if connection:
            rows = await connection.fetch(sql, *args)
        else:
            async with self._db.acquire() as c:
                rows = await c.fetch(sql, *args)
        if not rows:
            return None
        return rows

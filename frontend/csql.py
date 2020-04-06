import asyncio
import aiomysql
import time
import random


class ConstantSQL:
    """Encapsulate the database connection."""

    def __init__(self):
        """Initializer for ConstantSQL."""
        self._conn = False
        self._execution_queue = []

    async def connect(self, config):
        """Connect to the database."""
        if self._conn is not False:
            self._conn.close()
            await self._conn.wait_closed()
        self._conn = await aiomysql.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            db=config["db"],
            autocommit=True
        )

    async def execute(self, sql, params=tuple()):
        """Execute SQL.

        Args:
            sql: A valid SQL string
            params: An indexable object

        Returns:
            A database cursor.
        """
        queued_start_time = time.time()

        queue_position = asyncio.get_event_loop().create_future()
        self._execution_queue.append(queue_position)

        if len(self._execution_queue) == 1:
            queue_position.set_result(None)

        if len(self._execution_queue) > 10:
            print("Warning: SQL execution queue is at", len(self._execution_queue))

        await queue_position

        try:
            async with self._conn.cursor() as cur:
                await cur.execute(sql, params)
                return cur
        except RuntimeError as e:
            if str(e) == (
                "read() called while another coroutine is "
                "already waiting for incoming data"
            ):
                print(
                    "CSQL ERROR---------------",
                    "RuntimeError: read() called while another coroutine is already"
                    " waiting for incoming data. Make new conn for different csql conn."
                )
                quit()
        finally:
            self._execution_queue = self._execution_queue[1:]
            if len(self._execution_queue) > 0:
                self._execution_queue[0].set_result(None)

            if time.time() - queued_start_time > 0.01:
                print("Warning: SQL execution queue time of", time.time() - queued_start_time)

import asyncio
import asyncpg
import logging
from typing import Any, Dict, List, Optional, Union
from asyncpg import Pool, Connection
from functools import wraps
import time
import json
from contextlib import asynccontextmanager
import os

class PostgresDatabase:
    """
    A class to manage PostgreSQL database connections and operations.
    
    This class provides a high-level interface for database operations,
    including connection pooling, automatic retries, and various query methods.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialise the PostgresDatabase instance.

        :param config: A dictionary containing database configuration parameters.
        """
        self.config = config
        self.pool: Optional[Pool] = None  # Connection pool, initialised later
        self.logger = logging.getLogger(__name__)
        self.query_cache: Dict[str, Any] = {}  # Cache for query results
        self.statement_cache: Dict[str, asyncpg.Statement] = {}  # Cache for prepared statements
        self.retries = config.get('max_retries', 3)  # Number of retries for failed operations
        self.retry_delay = config.get('retry_delay', 1)  # Delay between retries in seconds
        self._lock = asyncio.Lock()  # Lock for thread-safe operations

    @classmethod
    def from_env(cls):
        """
        Create a PostgresDatabase instance from environment variables.

        This class method allows easy instantiation of the database
        connection using environment variables for configuration.
        """
        config = {
            'host': os.getenv('PG_DB_HOST'),
            'port': int(os.getenv('PG_DB_PORT', '5432')),
            'user': os.getenv('POSTGRES_USER'),
            'password': os.getenv('POSTGRES_PASSWORD'),
            'database': os.getenv('POSTGRES_DB'),
            'min_connections': int(os.getenv('PG_DB_MIN_CONNECTIONS', '10')),
            'max_connections': int(os.getenv('PG_DB_MAX_CONNECTIONS', '100')),
            'command_timeout': int(os.getenv('PG_DB_COMMAND_TIMEOUT', '60')),
            'max_inactive_connection_lifetime': int(os.getenv('PG_DB_MAX_INACTIVE_CONNECTION_LIFETIME', '300')),
        }
        return cls(config)

    async def initialise(self):
        """
        Initialise the database connection pool.

        This method sets up the connection pool using the provided configuration.
        It also sets up any connection-specific settings.
        """
        try:
            pool_config = {
                'host': self.config['host'],
                'port': self.config['port'],
                'user': self.config['user'],
                'password': self.config['password'],
                'database': self.config['database'],
                'min_size': self.config.get('min_connections', 10),
                'max_size': self.config.get('max_connections', 100),
                'command_timeout': self.config.get('command_timeout', 60),
                'max_inactive_connection_lifetime': self.config.get('max_inactive_connection_lifetime', 300),
                'connection_class': asyncpg.connection.Connection,
                'init': self.setup_connection  # Use the setup_connection method
            }
            self.pool = await asyncpg.create_pool(**pool_config)
            self.logger.info("Database pool initialised successfully.")
        except Exception as e:
            self.logger.error(f"Failed to initialise database pool: {str(e)}")
            raise

    @staticmethod
    async def setup_connection(conn: Connection):
        """
        Set up a new database connection.

        This method is called for each new connection in the pool.
        It sets up any connection-specific configurations, like custom type codecs.
        """
        # Register json type codec
        await conn.set_type_codec(
            'json',
            encoder=lambda value: json.dumps(value) if value is not None else None,
            decoder=lambda value: json.loads(value) if value is not None else None,
            schema='pg_catalog',
            format='text'
        )
        # Register jsonb type codec
        await conn.set_type_codec(
            'jsonb',
            encoder=lambda value: json.dumps(value) if value is not None else None,
            decoder=lambda value: json.loads(value) if value is not None else None,
            schema='pg_catalog',
            format='text'
        )

    def retry_operation(max_retries: int = 3, retry_delay: float = 1.0):
        """
        Decorator for retrying database operations.

        This decorator will retry the decorated function in case of certain
        database-related exceptions, with a specified number of retries and delay.

        :param max_retries: Maximum number of retry attempts.
        :param retry_delay: Delay between retries in seconds.
        """
        def decorator(func):
            @wraps(func)
            async def wrapper(self, *args, **kwargs):
                for attempt in range(max_retries):
                    try:
                        async with self._lock:
                            return await func(self, *args, **kwargs)
                    except (asyncpg.exceptions.ConnectionDoesNotExistError, asyncpg.exceptions.InterfaceError) as e:
                        if attempt == max_retries - 1:
                            self.logger.error(f"Operation failed after {max_retries} attempts: {str(e)}")
                            raise
                        self.logger.warning(f"Operation failed, retrying (attempt {attempt + 1}/{max_retries}): {str(e)}")
                        await asyncio.sleep(retry_delay)
                        if self.pool.is_closed():
                            await self.initialise()
                # If all retries fail, re-raise the last exception
                raise e
            return wrapper
        return decorator

    async def get_connection(self):
        """
        Get a connection from the pool.

        :return: A database connection from the pool.
        """
        if self.pool is None:
            raise Exception("Database pool is not initialised.")
        return await self.pool.acquire()

    @asynccontextmanager
    async def transaction(self):
        """
        Context manager for database transactions.

        This allows use of the 'async with' syntax for transactions,
        automatically handling commit and rollback.
        """
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                yield conn

    @retry_operation()
    async def execute(self, query: str, *args, timeout: Optional[float] = None) -> str:
        """
        Execute a SQL query.

        :param query: The SQL query to execute.
        :param args: Arguments to be used in the query.
        :param timeout: Optional timeout for the query execution.
        :return: The result of the query execution.
        """
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args, timeout=timeout)

    @retry_operation()
    async def fetch(self, query: str, *args, timeout: Optional[float] = None) -> List[asyncpg.Record]:
        """
        Fetch multiple rows from a SQL query.

        :param query: The SQL query to execute.
        :param args: Arguments to be used in the query.
        :param timeout: Optional timeout for the query execution.
        :return: A list of records matching the query.
        """
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args, timeout=timeout)

    @retry_operation()
    async def fetchrow(self, query: str, *args, timeout: Optional[float] = None) -> Optional[asyncpg.Record]:
        """
        Fetch a single row from a SQL query.

        :param query: The SQL query to execute.
        :param args: Arguments to be used in the query.
        :param timeout: Optional timeout for the query execution.
        :return: A single record matching the query, or None if no match.
        """
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args, timeout=timeout)

    @retry_operation()
    async def fetchval(self, query: str, *args, column: int = 0, timeout: Optional[float] = None) -> Any:
        """
        Fetch a single value from a SQL query.

        :param query: The SQL query to execute.
        :param args: Arguments to be used in the query.
        :param column: The index of the column to return.
        :param timeout: Optional timeout for the query execution.
        :return: A single value from the specified column of the query result.
        """
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args, column=column, timeout=timeout)

    async def batch_insert(self, table: str, columns: List[str], values: List[List[Any]], chunk_size: int = 1000):
        """
        Perform a batch insert operation.

        This method inserts multiple rows into a table in chunks to optimise performance.

        :param table: The name of the table to insert into.
        :param columns: The list of column names.
        :param values: A list of rows, where each row is a list of values.
        :param chunk_size: The number of rows to insert in each chunk.
        """
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES "
        async with self.transaction() as conn:
            for i in range(0, len(values), chunk_size):
                chunk = values[i:i + chunk_size]
                value_placeholders = [f"({', '.join('$' + str(j) for j in range(i * len(columns) + 1, (i + 1) * len(columns) + 1))})" for i in range(len(chunk))]
                chunk_query = query + ', '.join(value_placeholders)
                flattened_values = [item for sublist in chunk for item in sublist]
                await conn.execute(chunk_query, *flattened_values)

    @retry_operation()
    async def execute_prepared_statement(self, name: str, *args):
        """
        Execute a prepared statement.

        :param name: The name of the prepared statement.
        :param args: Arguments to be used in the prepared statement.
        :return: The result of executing the prepared statement.
        """
        if name not in self.statement_cache:
            raise ValueError(f"Prepared statement '{name}' not found")
        
        async with self.pool.acquire() as conn:
            stmt = self.statement_cache[name]
            return await stmt.fetch(*args)

    @retry_operation()
    async def prepare_statement(self, name: str, query: str):
        """
        Prepare and cache a statement for repeated execution.

        :param name: A name to identify the prepared statement.
        :param query: The SQL query to prepare.
        """
        async with self.pool.acquire() as conn:
            stmt = await conn.prepare(query)
            self.statement_cache[name] = stmt

    @retry_operation()
    async def execute_many(self, query: str, args_list: List[List[Any]]):
        """
        Execute a query with multiple sets of parameters.

        :param query: The SQL query to execute.
        :param args_list: A list of parameter sets, one for each execution of the query.
        """
        async with self.transaction() as conn:
            await conn.executemany(query, args_list)

    async def listen(self, channel: str, callback: callable):
        """
        Listen for notifications on a channel.

        :param channel: The name of the channel to listen on.
        :param callback: A callable to be invoked when a notification is received.
        """
        async with self.pool.acquire() as conn:
            await conn.add_listener(channel, callback)
            while True:
                await asyncio.sleep(3600)  # Keep the connection alive

    @retry_operation()
    async def notify(self, channel: str, payload: str):
        """
        Send a notification to a channel.

        :param channel: The name of the channel to send the notification to.
        :param payload: The payload of the notification.
        """
        async with self.pool.acquire() as conn:
            await conn.execute(f"NOTIFY {channel}, '{payload}'")

    @retry_operation()
    async def create_index(self, table: str, columns: List[str], index_name: Optional[str] = None, unique: bool = False):
        """
        Create an index on specified columns.

        :param table: The name of the table to create the index on.
        :param columns: The list of columns to include in the index.
        :param index_name: Optional name for the index. If not provided, one will be generated.
        :param unique: Whether the index should enforce uniqueness.
        """
        index_type = "UNIQUE" if unique else ""
        index_name = index_name or f"idx_{table}_{'_'.join(columns)}"
        query = f"CREATE {index_type} INDEX IF NOT EXISTS {index_name} ON {table} ({', '.join(columns)})"
        await self.execute(query)

    @retry_operation()
    async def vacuum(self, table: str):
        """
        Perform VACUUM operation on a table.

        :param table: The name of the table to vacuum.
        """
        async with self.pool.acquire() as conn:
            await conn.execute(f"VACUUM ANALYZE {table}")

    @retry_operation()
    async def get_table_size(self, table: str) -> int:
        """
        Get the size of a table in bytes.

        :param table: The name of the table.
        :return: The size of the table in bytes.
        """
        query = f"SELECT pg_total_relation_size('{table}')"
        return await self.fetchval(query)

    @retry_operation()
    async def explain_analyse(self, query: str, *args) -> str:
        """
        Get the execution plan for a query.

        :param query: The SQL query to analyse.
        :param args: Arguments to be used in the query.
        :return: The execution plan in JSON format.
        """
        explain_query = f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {query}"
        return await self.fetchval(explain_query, *args)

    async def close(self):
        """
        Close the database pool.

        This method should be called when the database connection is no longer needed.
        """
        if self.pool:
            await self.pool.close()
            self.logger.info("Database pool closed.")

    def __del__(self):
        """
        Ensure the pool is closed when the object is deleted.

        This method creates a task to close the pool when the object is garbage collected.
        """
        if self.pool:
            asyncio.create_task(self.close())

# Usage example:
async def main():
    # Create a database instance using environment variables
    db = PostgresDatabase.from_env()
    await db.initialise()
    
    # Example query
    result = await db.fetch("SELECT * FROM users WHERE active = $1", True)
    print(result)
    
    # Close the database connection
    await db.close()

if __name__ == "__main__":
    asyncio.run(main())

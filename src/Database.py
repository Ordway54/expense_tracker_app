import sqlite3 as sq
import atexit

class Database:
    
    def __init__(self):
        """Initializes a Database object."""

        self.conn = sq.Connection(r'src\transactions.db')
        self.cur = self.conn.cursor()

        # ensure database connection is closed upon exit
        atexit.register(self._on_exit)

    def add_transaction(self, transaction: dict,
                        table_name: str = 'transactions'):
        
        """Adds a transaction to the database."""

        # use placeholders to bind values to query (stop SQL injections)
        placeholders = ', '.join(['?' for _ in range(len(transaction))])
        columns = tuple(transaction.keys())
        values = tuple(transaction.values())

        query = f"INSERT INTO {table_name} {columns} VALUES ({placeholders})"

        self.conn.execute(query,values)
        self.conn.commit()

    def remove_transaction(self, transaction: dict, table_name:str = 'transactions'):
        """Removes a transaction from the database."""

        condition = ""
        
        # form WHERE condition for SQL DELETE statement
        for i,(key,value) in enumerate(transaction.items()):

            last_key_index = len(transaction) - 1

            # if last key, don't add trailing 'AND' operator
            if i == last_key_index:
                condition = condition + f"{key} = '{value}'"
            else:
                condition = condition + f"{key} = '{value}' AND "

        statement = f"DELETE FROM {table_name} WHERE {condition}"

        self.conn.execute(statement)
        self.conn.commit()

    def update_transaction(self, column, new_value, condition, table_name: str = 'transactions',*kwargs):
        """Updates a transaction in the database."""
        
        query = f"UPDATE {table_name} SET {column} = {new_value} WHERE {condition}"

        self.conn.execute(query)
        self.conn.commit()

    def query_all(self, table_name: str = 'transactions'):
        """Queries the database."""

        query = f"SELECT * FROM {table_name}"

        res = self.conn.execute(query)

        return [item for item in res.fetchall()]

    def query(self, query:str):
        """Returns the results of the query."""
        res = self.conn.execute(query)

        return [item for item in res.fetchall()]
        
    def _on_exit(self):
        self.conn.close()
        print("Database connection closed successfully.")
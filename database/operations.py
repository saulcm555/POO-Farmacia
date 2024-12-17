from .interfaces import ISQLOperations
from .interfaces import IConnection
from typing import List, Optional
import sqlite3

class SQLOperations(ISQLOperations):
    def __init__(self, connection: IConnection):
        if not isinstance(connection, IConnection):
            raise ValueError("connection must be a IConnection instance")
        self.connection = connection
        

    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[sqlite3.Row]:
        # Dividir el query por punto y coma (;) para separar las sentencias SQL
        queries = query.split(';')
        result = []
        
        with self.connection:
            cursor = self.connection.cursor()
            
            for single_query in queries:
                single_query = single_query.strip()
                if single_query:  # Ignorar consultas vacías
                    cursor.execute(single_query, params or ())
                    result.append(cursor.fetchall())
            
            self.connection.commit()
        
        return result


    def execute_many(self, query: str, params_list: List[tuple]):
        with self.connection:
            cursor = self.connection.cursor()

            cursor.executemany(query, params_list)
            self.connection.commit()
            return cursor.fetchall()
   
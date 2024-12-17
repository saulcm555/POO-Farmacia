from abc import ABC, abstractmethod
from typing import List, Optional
import sqlite3


class ISQLOperations(ABC):

    @abstractmethod
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[sqlite3.Row]:
        pass

    @abstractmethod
    def execute_many(self, query: str, params_list: List[tuple]):
        pass
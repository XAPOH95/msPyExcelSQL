from .connection import Connection
from pyodbc import Cursor, Connection

class ExcelController:
    """Role of class is to get cursor from connection and execute SQL requests"""
    db:Connection = None
    def __init__(self) -> None:
        if self.db is None:
            raise Exception("db is None! Setup db connection!")

    def _get_cursor(self):
        return self.db.cursor()

    def run(self, request:'ExcelRequest') -> Cursor:
        cursor = self._get_cursor()
        return cursor.execute(str(request))

    def run_with_params(self, request:'ExcelRequest', params:tuple) -> Cursor:
        cursor = self._get_cursor()
        return cursor.execute(str(request), params)
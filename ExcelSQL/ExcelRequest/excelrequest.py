"""
This module take care about ODBC Excel dialect and let build most common requests
"""

from .request_mixins import SelectImplementation, UpdateImplementation, InsertImplementation, DeleteImplementation
from ExcelSQL.ExcelSheet.excelcolumn import ExcelColumn, ColumnContainer

class ExcelRequest:
    _command:str
    columns:ColumnContainer

    def __init__(self, sheet:'ExcelSheet', columns:tuple['ExcelColumn'] = None) -> None:
        self.sheet = sheet
        self.set_columns(columns)

    def set_columns(self, columns:tuple['ExcelColumn'] = None):
        self.columns = ColumnContainer(columns)

    def __str__(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return str(self)

    def _join(self, elements:list):
        return ' '.join([str(ele) for ele in elements if ele])

class SelectRequest(ExcelRequest, SelectImplementation):
    """Use this class to make SELECT request"""
    _command = 'SELECT'

    def __str__(self) -> str:
        elements = [
            self._command,
            self._distinct,
            str(self.columns),
            self._aggr,
            'FROM',
            str(self.sheet),
            self._where,
            self._in,
            self._like,
            self._group_by,
            self._having,
            self._order_by,
            self._limit
            ]
        return self._join(elements)

class UpdateRequest(ExcelRequest, UpdateImplementation):
    """Use this class to make Update request"""
    _command = 'UPDATE'

    def __str__(self) -> str:
        elements = [
            self._command,
            str(self.sheet),
            'SET',
            self._set,
            self._where
        ]
        return self._join(elements)

class InsertRequest(ExcelRequest, InsertImplementation):
    """Use this class to make Insert request"""
    _command = 'INSERT INTO'

    def values_to_insert(self, values:tuple):
        if len(self.columns) == 0:
            return super().values_to_insert(values)
        if len(self.columns) != len(values):
            raise IndexError(f"Lenght of columns is not matching with inserted values lenght \nawaited {len(self.columns)} values but got only {len(values)}")
        return super().values_to_insert(values)
        
    def __str__(self) -> str:
        elements = [
            self._command,
            str(self.sheet),
            self.columns.get_columns_in_parentheses(),
            'VALUES',
            self._values
        ]
        return self._join(elements)

class DeleteRequest(ExcelRequest, DeleteImplementation):
    """Use this class if you need to delete record in excel.\nWell, actually its not DELETE, its UPDATE to NULL"""
    _command = 'UPDATE'

    def __init__(self, sheet: 'ExcelSheet', columns: tuple['ExcelColumn']) -> None:
        """ODBC driver cant delete rows, it can only turn row to NULL values\nAll sheet columns required"""
        super().__init__(sheet, columns)
        self._records_to_delete(columns)

    def __str__(self) -> str:
        elements = [
            self._command,
            str(self.sheet),
            'SET',
            self._delete,
            self._where
        ]
        return self._join(elements)
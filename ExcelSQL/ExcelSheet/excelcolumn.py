from datetime import datetime
from ExcelSQL.ExcelRequest.requestUtils import Agregator, Formatter, Selector

class BasicColumn:
    def __init__(self, title:str, valuetype) -> None:
        """Default column in excel sheet.

        Args:
            sheet (ExcelSheet): sheet where column located
            title (str): title of column, whitespaces allowed but not welcomed.
            valuetype (_type_): link to python class of types that column containt. One of int|float|str|datetime 
        """
        self.title = title.replace('.', '#')
        self.valuetype = valuetype

    def __str__(self) -> str:
        if self.title.count(' '):
            return f'[{self.title}]'
        return self.title

    def __repr__(self) -> str:
        return str(self)

    def get_agregator(self):
        return Agregator(self)

    def get_formatter(self):
        return Formatter(self)

    def get_selector(self):
        return Selector(self)

    def to_format(self, value):
        """trying to convert given value to column type"""
        if self.valuetype is datetime:
            return self._to_datetimeformat(value)
        elif value is None:
            return None
        return self.valuetype(value)

    def _to_datetimeformat(self, value):
        raise NotImplementedError

    def to_model_keys(self):
        symbols = (' ', '#')
        model_format = self.title
        for symbol in symbols:
            model_format = model_format.replace(symbol, '_')
        return model_format

class ExcelColumn(BasicColumn):
    """Role of class is to represent a column of sheet in excel, its title and format."""
    def __init__(self, sheet: 'ExcelSheet', title: str, valuetype) -> None:
        """Column should know to what excel sheet its belongs to. So thats why column object should be create in ExcelSheet constructor"""
        super().__init__(title, valuetype)
        self.sheet = sheet

class IdColumn(ExcelColumn):
    """Role of class is to let excelsheet know that this column is id"""
    pass

class ColumnContainer:
    """Basic class to contain columns and format them to excel odbc driver dialect"""
    def __init__(self, columns:tuple) -> None:
        self.columns = list()
        if columns is None:
            return
        self.columns = columns

    def all(self):
        return '*'

    def get_model_keys(self):
        """Method returns tiple of column names with whitespaces, dots and hashsigns converted underscore.
        
        So this keys can used and dictkey and be passed to model constructor
        
        For example, columns "total cost" and "comp.inc." will be converted to
        \t"total cost" => total_cost
        
        \t"comp.inc." => comp_inc_"""
        column:BasicColumn
        return tuple([column.to_model_keys() for column in self.columns])

    def get_columns(self):
        return ', '.join([str(column) for column in self.columns])

    def get_pug(self):
        return "(" + ", ".join(['?' for column in self.columns]) + ")"

    def get_columns_in_parentheses(self):
        if self.columns:
            return '(' + self.get_columns() + ')'
        return self.get_columns()
        
    def __str__(self) -> str:
        if self.columns:
            return self.get_columns()
        return self.all()

    def __len__(self):
        return len(self.columns)

    def __iter__(self) -> ExcelColumn:
        for column in self.columns:
            yield column

class ExcelColumnContainer(ColumnContainer):
    def __init__(self, ExcelSheet:'ExcelSheet'):
        self._id_column:IdColumn = None

        values = self._get_excelsheet_value(ExcelSheet)
        columns = self._find_excelcolumns(values)
        
        super().__init__(columns)

    def get_id_column(self):
        return self._id_column

    def _get_excelsheet_value(self, ExcelSheet:'ExcelSheet'):
        return [
            *ExcelSheet.__class__.__dict__.values(),
            *ExcelSheet.__dict__.values()]

    def _find_excelcolumns(self, values):
        columns = list()
        for value in values:
            if isinstance(value, IdColumn):
                self._id_column = value
            if isinstance(value, ExcelColumn):
                columns.append(value)
        return columns
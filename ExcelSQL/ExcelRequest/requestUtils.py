class requestUtil:
    def __init__(self, column:str):
        """Lazy way to format column title to SQL agregation form. Like, total -> SUM(total)

        Args:
            column (str): str or ExcelColumn
        """
        self._column = str(column)

class Agregator(requestUtil):
    """let you convert column name to agr sql function"""
    def _get_parentheses(self):
        return f'({self._column})'

    def count(self):
        return 'COUNT'+self._get_parentheses()

    def sum(self):
        return 'SUM'+self._get_parentheses()

    def avg(self):
        return 'AVG'+self._get_parentheses()

    def min(self):
        return 'MIN'+self._get_parentheses()

    def max(self):
        return 'MAX'+self._get_parentheses()

class Formatter(requestUtil):
    """if you need round"""
    def round_to_int(self):
        return 'ROUND'+f'({self._column}, 0)'

    def round_to_2f(self):
        return 'ROUND'+f'({self._column}, 2)'

    def round_to_f(self, precision:int):
        return 'ROUND'+f'({self._column}, {precision})' 

class Selector(requestUtil):
    """if you need to make expression"""
    def isNull(self):
        return self._column + ' IS NULL'

    def isNotNull(self):
        return self._column + ' IS NOT NULL'

    def pugged(self):
        """returns my_column = ?"""
        return self._column + " = ?"
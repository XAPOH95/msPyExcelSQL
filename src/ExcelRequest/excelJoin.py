from .request_mixins import JoinImplementation


class JoinRequest(JoinImplementation):
    _command = 'SELECT'
    _left_sheet:'ExcelSheet' = None
    _right_sheet:'ExcelSheet' = None
    _columns:str = '*'

    def __init__(self, left_sheet:'ExcelSheet', right_sheet:'ExcelSheet'):
        self._left_sheet = left_sheet
        self._right_sheet = right_sheet

    def __str__(self) -> str:
        elements = [
            self._command,
            self._columns,
            'FROM',
            self._left_sheet,
            self._how,
            self._right_sheet,
            self._on,
            self._where
        ]
        return self._join(elements)

    def _join(self, elements:list):
        return ' '.join([str(ele) for ele in elements if ele])

    def reset_columns(self):
        self._columns = '*'

    def set_columns(self, left: tuple, right:tuple):
        """tuples of awaited columns"""
        self._columns = ', '.join(
            self._concat_sheet_with_tuple_of_columns(
                self._left_sheet, left) +
            self._concat_sheet_with_tuple_of_columns(
                self._right_sheet, right))


    def join_on(self, left: tuple, right: tuple):
        super().join_on(left, right)
        on:list = list()
        for i in range(len(left)):
            on.append(self._concat_eq_cols(left[i], right[i]))
        self._on = 'ON ' + ', '.join(on)

    def _concat_sheet_with_tuple_of_columns(self, sheet, columns:tuple):
        concated = list()
        for column in columns:
            concated.append(
                self._concat_sheet_with_column(
                    sheet, column))
        return concated

    def _concat_sheet_with_column(self, sheet, column):
        return str(sheet) + '.' + str(column)

    def _concat_eq_cols(self, left, right):
        eq = ' = '
        left_concat = self._concat_sheet_with_column(self._left_sheet, left)
        right_concat = self._concat_sheet_with_column(self._right_sheet, right)
        return left_concat + eq + right_concat


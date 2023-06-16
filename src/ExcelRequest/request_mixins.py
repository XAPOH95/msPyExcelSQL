from ..ExcelSheet.excelcolumn import ExcelColumn

class mixinLimit:
    _limit:str = ""

    def limit(self, limit:int = None):
        if limit is None:
            self._limit = ''
        else:
            self._limit = "LIMIT " + str(limit)

class mixinDistinct:
    _distinct:str = ''

    def distinct(self, value:bool):
        if value:
            self._distinct = "DISTINCT"
        else:
            self._distinct = ""

class mixinWhere:
    _where:str = ""

    def where(self, expression:str = ''):
        if expression:
            self._where = 'WHERE ' + expression
        else:
            self._where = ''

class mixinGroupBy:
    _group_by:str = ''

    def group_by(self, column:'ExcelColumn' = ''):
        if column:
            self._group_by = "GROUP BY " + str(column)
        else:
            self._group_by = ""

class mixinHaving:
    _having:str = ""

    def having(self, expression:str = ""):
        if expression:
            self._having = "HAVING " + expression
        else:
            self._having = ""

class mixinOrderBy:
    _order_by:str = ""

    def order_by(self, column:'ExcelColumn' = '', desc:bool = False):
        if column:
            self._order_by = "ORDER BY " + str(column)
            if desc:
                self._order_by += " DESC"
        else:
            self._order_by = ""

class mixinIn:
    _in:str = ""

    def set_in(self, values: tuple = None):
        if values is None:
            self._in = ''
        else:
            self._in = 'IN (' + str(values) + ')'

class mixinLike:
    _like:str = ""

    def like(self, expression:str = ''):
        if expression:
            self._like = 'LIKE ' + expression
        else:
            self._like = ''

class mixinAgregation:
    _aggr:str = ""

    def agregation(self, expression:str = ''):
        if expression:
            self._aggr = expression
        else:
            self._aggr = ''

class mixinSet:
    _set:str = ""

    def columns_to_update(self, columns:tuple):
        self._set = ', '.join([str(column) + ' = ?' for column in columns])

class mixinInsert:
    _values:str = ""

    def values_to_insert(self, values:tuple):
        self._values = "(" + ', '.join(['?' for val in values]) + ")"

class mixinDelete:
    _delete:str = ""
    _null = "NULL"

    def _records_to_delete(self, columns:tuple):
        self._delete = ', '.join([str(column) + ' = ' + self._null for column in columns])

class mixinOn:
    _on:str = ""

    def join_on(self, left:tuple, right:tuple):
        if len(left) != len(right):
            raise IndexError("Length of columns doesnt match!")

class mixinJoin:
    _how:str = ""

    def inner(self):
        self._how = "INNER JOIN"
    
    def left(self):
        self._how = 'LEFT JOIN'

    def right(self):
        self._how = 'RIGHT JOIN'

    def full(self):
        self._how = 'FULL JOIN'

class JoinImplementation(mixinOn, mixinJoin, mixinWhere):
    """Mix of join elements"""
    pass

class SelectImplementation(mixinDistinct, mixinWhere, mixinOrderBy, mixinGroupBy, mixinHaving, mixinLimit, mixinIn, mixinLike, mixinAgregation):
    """Mix of most common SELECT specifies"""
    pass

class UpdateImplementation(mixinWhere, mixinSet):
    pass

class InsertImplementation(mixinInsert):
    pass

class DeleteImplementation(mixinWhere, mixinDelete):
    pass
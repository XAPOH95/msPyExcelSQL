import pyodbc

class Connection:
    """Role of class is to find odbc driver and connect to given file"""
    _connection:pyodbc.Connection = None
    for _driver in pyodbc.drivers():
        if 'xlsx' in _driver:
            break
    else:
        raise Exception("MS Excel Driver not found!")

    def __new__(cls, path:str):
        if cls._connection is None:
            cls._connection = pyodbc.connect(
                f'DRIVER={cls._driver};DBQ=' + path + ';ReadOnly=0;',
                autocommit=True
            )
            print('Successfully connected to ', path, "\n", 'DRIVER=', cls._driver, '\nReadOnly=0, autocommit=True', sep='')
            return cls._connection
        return cls._connection
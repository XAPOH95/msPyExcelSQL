import sys

def example():
    """
    cmd python msPyExcelSQL example type_file_name(optional)
    
    creates example file (defualt deployed.py)
    """
    try:
        name = str(sys.argv[1])
    except IndexError as ex:
        name = None
    Deploy(name)

class Deploy:
    """Class is used to deploy demo file for fast rewrite and go"""
    filename = 'deployed.py'
    
    imprts = "from msPyExcelSQL import ExcelController, Connection, ModelSheet, IdColumn, ExcelColumn, DatetimeColumn, ExcelModel, ModelIdentification, ExcelSheet\n"
    
    controller = """
class MyController(ExcelController):
    # To have fun do following:
    # 1. create example.xlsx
    # 2. create sheet with name MyModel
    # 2.1 call first row id, name, total_cost, time
    # 3. create sheet with name MyExcel
    # 3.1 call first row position, title, stock, total_cost

    def __init__(self) -> None:
        self.db = Connection('example.xlsx')
    """
    modelsheet = """
class MyModelSheet(ModelSheet):
    def __init__(self) -> None:
        self.idi = IdColumn(self, 'id', int)        # because id is reserved by python better to call attr idi or idf
        self.name = ExcelColumn(self, 'name', str)
        self.total = ExcelColumn(self, 'total_cost', float)
        self.timestamp = DatetimeColumn(self, 'time', ("%d/%m/%Y", "%d/%m/%Y %H:%M", "%d/%m/%y"))   # regex for excel dateformat
        super().__init__(MyController())    # always call super last and pass controller. Some blackmagic happens underhood
        # if you pass MyController() before defining of columns, columns will not be registred

    def get_model(self, kwargs:dict) -> 'ExcelModel':
        return MyModel(
            id = int(kwargs.get('id')),  # you can do forced typecast while passing params
            name = kwargs.get('name'),
            total_cost = kwargs.get('total_cost'),
            time = kwargs.get('time')
        )
        # or you can just do return MyModel(**kwargs)
    """
    model = """
class MyModel(ExcelModel):
    _alias = {'total':'total_cost', 'period':'time'}    # alias is used for matching columns in excel with attrs of class

    def __init__(self, id:int, name:str, total_cost:float, time) -> None:
        # params should match column names in excel file but if you are using whitespaces in column names whitespaces will be converted to underscore _
        # also dot with be converted to underscore
        self._sheet = MyModelSheet()
        self.idi = ModelIdentification('id', id)    # to let ExcelSheet know that this is id column
        self.name = name
        self.total = float(total_cost) # you can do forced typecast when creating instance of class
        self.period = time              # odbc driver casts python datetime on date
    """
    regular_sheet = """
class MyExcelSheet(ExcelSheet):
    def __init__(self) -> None:
        self.position = IdColumn(self, 'position', int)
        self.title = ExcelColumn(self, 'title', str)
        self.stock = ExcelColumn(self, 'stock', int)
        self.total = ExcelColumn(self, 'total_cost', float)
        super().__init__(MyController())

    """
    final = """
def insert_model():
    import random
    import datetime

    for i in range(30):
        model = MyModel(None, "yes its works!", random.randint(1, 10)/10, datetime.datetime.now())
        model.save()
    # should appear in example.xlsx on MyModel sheet

    # on ryzen7 4800H and nvme m.2 pcie3.0 ssd odbc driver inserted 1280 rows with 4 random values each second
    # if excel file is open only 20 records has been inserted each second

def read_model():
    model = MyModelSheet().find_model_by_id(1)
    print("Hello, Im", model.name)

def update_model():
    model = MyModelSheet().find_model_by_id(1)
    model.name = "ODBC"
    model.update()

def delete_model():
    model = MyModelSheet().find_model_by_id(1)
    model.delete()

if __name__ == "__main__":
    # if you created example.xlsx
    # call functions above    
    """
    def __init__(self, filename:str = None):
        if filename is None:
            self._deploy()
        else:
            self._check_name(filename)
    
    def _check_name(self, name:str):
        if name.endswith('.py'):
            self.filename = name
        elif name.count('.') > 0:
            print('Wrong name', name, 'Used default name:', self.filename)
        else:
            self.filename = name + '.py'
        self._deploy()

    def _deploy(self):
        with open(self.filename, "w", encoding='utf-8') as file:
            file.write(self.imprts)
            file.write(self.controller)
            file.write(self.modelsheet)
            file.write(self.model)
            file.write(self.regular_sheet)
            file.write(self.final)

if __name__ == '__main__':
    example()
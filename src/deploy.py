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
    def __init__(self) -> None:
        self.db = Connection('example.xlsx')
    """
    modelsheet = """
class MyModelSheet(ModelSheet):
    def __init__(self) -> None:
        self.idi = IdColumn(self, 'id', int)
        self.name = ExcelColumn(self, 'name', str)
        self.total = ExcelColumn(self, 'total_cost', float)
        self.timestamp = DatetimeColumn(self, 'time', ("%d/%m/%Y", "%d/%m/%Y %H:%M, %d/%m/%y"))
        super().__init__(MyController())

    def get_model(self, kwargs:dict) -> 'ExcelModel':
        return MyModel(**kwargs)
    """
    model = """
class MyModel(ExcelModel):
    _alias = {'total':'total_cost', 'period':'time'}

    def __init__(self, id:int, name:str, total_cost:float, time) -> None:
        self._sheet = MyModelSheet()
        self.idi = ModelIdentification('id', id)
        self.name = name
        self.total = total_cost
        self.period = time
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
        with open(self.filename, "w") as file:
            file.write(self.imprts)
            file.write(self.controller)
            file.write(self.modelsheet)
            file.write(self.model)
            file.write(self.regular_sheet)

if __name__ == '__main__':
    example()
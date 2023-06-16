import sys

def main():
    """
    cmd python msPyExcelSQL\\ExcelSQL\\deploy.py type_file_name
    """
    try:
        name = str(sys.argv[1])
    except IndexError as ex:
        name = None
    Deploy(name)

class Deploy:
    """Class is used to deploy demo file for fast rewrite and go"""
    filename = 'deployed.py'
    
    imprts = "from msPyExcelSQL.ExcelSQL import Main\n"
    
    controller = """
class MyController(Main.ExcelController):
    def __init__(self) -> None:
        self.db = Main.Connection('example.xlsx')
    """
    modelsheet = """
class MyModelSheet(Main.ModelSheet):
    def __init__(self) -> None:
        self.idi = Main.IdColumn(self, 'id', int)
        self.name = Main.ExcelColumn(self, 'name', str)
        self.total = Main.ExcelColumn(self, 'total_cost', float)
        self.timestamp = Main.DatetimeColumn(self, 'time', (%d/%m/%Y, %d/%m/%Y %H:%M, %d/%m/%y))
        super().__init__(MyController())

    def get_link_to_model(self) -> 'Main.ExcelModel':
        return MyModel
    """
    model = """
class MyModel(Main.ExcelModel):
    _alias = {'total':'total_cost', 'period':'time'}

    def __init__(self, id:int, name:str, total_cost:float, time) -> None:
        self._sheet = MyModelSheet()
        self.idi = Main.ModelIdentification('id', id)
        self.name = name
        self.total = total_cost
        self.period = time
    """
    regular_sheet = """
class MyExcelSheet(Main.ExcelSheet):
    def __init__(self) -> None:
        self.position = Main.IdColumn(self, 'position', int)
        self.title = Main.ExcelColumn(self, 'title', str)
        self.stock = Main.ExcelColumn(self, 'stock', int)
        self.total = Main.ExcelColumn(self, 'total_cost', float)
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
    main()
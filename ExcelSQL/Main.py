from .ExcelController.connection import Connection
from .ExcelController.excelcontroller import ExcelController
from .ExcelModel.model import ModelIdentification, ExcelModel
from .ExcelSheet.excelsheet import ModelExcelSheet
from .ExcelSheet.excelcolumn import ExcelColumn, IdColumn

__all__ = [
    'Connection',
    'ExcelController',
    'ModelIdentification',
    'ExcelModel',
    'ModelExcelSheet',
    'ExcelColumn',
    'IdColumn'
]

def deploy():
    """Function to deploy"""
    filename = 'deployed.py'
    imprts = """
from ExcelSQL.Main import Connection
from ExcelSQL.Main import ExcelController
from ExcelSQL.Main import ModelIdentification, ExcelModel
from ExcelSQL.Main import ModelExcelSheet
from ExcelSQL.Main import ExcelColumn, IdColumn
    """
    controller = """
class MyController(ExcelController):
    def __init__(self) -> None:
        self.db = Connection('tests/example.xlsx')
    """

    excelsheet = """
class MyExcelSheet(ModelExcelSheet):
    def __init__(self) -> None:
        self.idi = IdColumn(self, 'id', int)
        self.name = ExcelColumn(self, 'name', str)
        self.total = ExcelColumn(self, 'total_cost', float)
        super().__init__(MyController())

    def get_link_to_model(self) -> 'ExcelModel':
        return MyModel
    """

    model = """
class MyModel(ExcelModel):
    _alias = {'total':'total_cost'}

    def __init__(self, id:int, name:str, total_cost:float) -> None:
        self._sheet = MyExcelSheet()
        self.idi = ModelIdentification('id', id)
        self.name = name
        self.total = total_cost
    """
    file = open(filename, "w")
    file.write(imprts)
    file.write(controller)
    file.write(excelsheet)
    file.write(model)
    file.close()


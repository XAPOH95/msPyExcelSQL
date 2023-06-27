from .interfaces import Commands
from .excelcolumn import ExcelColumnContainer, ExcelColumn, BasicColumn

from ..ExcelController.excelcontroller import ExcelController
from ..ExcelModel.model import iSingleModel, iModelFabric, ExcelModel

class BasicSheet:
    def __init__(self, controller:ExcelController) -> None:
        self._controller = controller
        self.colcontainer = ExcelColumnContainer(self)

    def __str__(self):
        if  self.__class__.__name__.endswith('Sheet'):
            return "[" + self.__class__.__name__.replace('Sheet', '$') + "]"
        raise Exception("Class name should ends with Sheet")

    def __repr__(self) -> str:
        return str(self)

class ExcelSheet(BasicSheet, Commands):
    """Inherit struct and implements commands.

    Naming convention is following:
            class ExcelSheet sibling name must exactly match name of excelsheet, its case sensetive.
            class must endwith -Sheet suffix
            excelsheet in workbook cant contain whitespaces and "Sheet" capitalized word
            eg, if sheet in excel is called "mysheet" so python class should be called mysheetSheet

    To work with excel worksheet you need to inherit from this class with name convention.
    All public methods returns request object that should be passed to ExcelController for execution
    """
    def select(self):
        request = super().select()
        return request

    def records(self) -> int:
        request = self.select()
        request.set_columns(('COUNT(*)',))
        return self._controller.run(request).fetchone()[0]


    def update(self):
        request = super().update(self.colcontainer.columns)
        return request

    def insert(self, values:tuple):
        request = super().insert(self.colcontainer.columns)
        request.values_to_insert(values)
        return request

    def delete(self):
        request = super().delete(self.colcontainer.columns)
        return request

    def find(self, where: str):
        request = super().find(self.colcontainer.columns, where)
        return request

    def run(self, request, params:tuple = None):
        if params is not None:
            if isinstance(params, tuple):
                return self._controller.run_with_params(str(request), params)
            raise ValueError("params should be tuple!")
        return self._controller.run(str(request))
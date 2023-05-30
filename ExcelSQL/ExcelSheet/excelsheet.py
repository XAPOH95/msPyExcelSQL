from .interfaces import Commands
from .excelcolumn import ExcelColumnContainer, ExcelColumn, BasicColumn

from ExcelSQL.ExcelController.excelcontroller import ExcelController
from ExcelSQL.ExcelModel.model import iSingleModel, iModelFabric, ExcelModel

class ExcelSheet(Commands):
    def __init__(self, controller:ExcelController) -> None:
        self._controller = controller
        self.colcontainer = ExcelColumnContainer(self)

    def __str__(self):
        if  self.__class__.__name__.endswith('Sheet'):
            return "[" + self.__class__.__name__.replace('Sheet', '$') + "]"
        raise Exception("Class name should ends with Sheet")

    def __repr__(self) -> str:
        return str(self)

    def select(self):
        request = super().select()
        return request

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

    def records(self) -> int:
        request = super().select()
        request.set_columns(('COUNT(*)',))
        return self._controller.run(request).fetchone()[0]


class ModelExcelSheet(ExcelSheet, iSingleModel):
    """Role of class is listen orders of ExcelModel and prepare request, then ask database to execute. To fulfill its obligations class should know about ALL columns in excehSheet. So for each column should be created ExcelColumn object"""
    def __init__(self, controller: ExcelController) -> None:
        super().__init__(controller)
        self.model_keys = self.colcontainer.get_model_keys()

    ### general model interface implementation
    def find_model_by_id(self, index:int) -> ExcelModel:
        request = self._prepare_select_by_id_request()
        response = self._controller.run_with_params(request, (index,)).fetchall()[0]
        kvp = {self.model_keys[i]:response[i] for i in range(len(response))}
        return self.get_link_to_model()(**kvp)

    def find_model_by_expression(self, columns: tuple, values: tuple):
        """to create one model from expression like
        SELECT * FROM [Sheet1$] WHERE name = ? AND [total cost] = ?"""
        request = self._prepare_select_by_expression_request(columns)
        response = self._controller.run_with_params(request, values).fetchall()[0]
        kvp = {self.model_keys[i]:response[i] for i in range(len(response))}
        return self.get_link_to_model()(**kvp)


    def _prepare_select_by_expression_request(self, columns: tuple):
        request = self.select()
        where_statement = list()
        for column in columns:
            where = self._prepare_arg_column(column).get_selector().pugged()
            where_statement.append(where)
        request.where(' AND '.join(where_statement))    # WHERE col1 = ? AND [col 2] = ? AND col#3 = ?
        return request

    def _prepare_arg_column(self, column) -> BasicColumn:
        """method to convert str to BasicColumn, if ExcelColumn passed, do nothing"""
        if isinstance(column, ExcelColumn):
            return column
        return BasicColumn(column, None)

    def _prepare_select_by_id_request(self):
        request = self.select() 
        where = self.colcontainer.get_id_column().get_selector().pugged() # get select statement
        request.where(where)  # SELECT * FROM Sheet$ WHERE 'id column name' = ?
        return request

    def insert_model(self, model:ExcelModel):
        """Method has side effect on model id. Because if you created and inserted model into database and then update it, model wont be found cause id of new model is 0"""
        self._assign_id_to_model(model)
        record = list()
        row = dict(model)
        for key in self.model_keys:
            record.append(row.get(key))
        self.insert(record)

    def insert(self, record:list):
        request = super().insert(record)
        formatted_values = self._format_records(record)
        self._run_db_modification(request, formatted_values)

    def update_model(self, model: ExcelModel):
        record = list()
        row = dict(model)
        for key in self.model_keys:
            value = row.get(key)
            if isinstance(value, ExcelModel):
                record.append(value.get_id())
            else:
                record.append(value)                       
        self.update(record, int(model.get_id()))

    def update(self, record:list, index):
        request = super().update()
        request.where(self.colcontainer.get_id_column().get_selector().pugged())
        request.columns_to_update(self.colcontainer)
        formatted_values = self._format_records(record)
        formatted_values.append(index)
        self._run_db_modification(request, formatted_values)

    def delete_model(self, model: 'ExcelModel'):
        model_id = model.get_id()
        if model_id:
            request = self.delete()
            self._run_db_modification(request, (int(model_id),))

    def delete(self):
        request =  super().delete()
        request.where(self.colcontainer.get_id_column().get_selector().pugged())
        return request

    def _assign_id_to_model(self, model:'ExcelModel'):
        """SIDE EFFECT!!! this method assign id to model and changes it id value"""
        if model.get_id() is None:
            return
        index = self.records() + 1
        model.assign_id(index)

    def _format_records(self, values:list):
        formatted_values = list()
        for index, column in enumerate(self.colcontainer):
            formatted_values.append(column.to_format(values[index]))
        return formatted_values

    def _run_db_modification(self, request:str, params:list):
        self._controller.run_with_params(request, tuple(params))
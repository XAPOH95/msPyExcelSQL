from .excelsheet import BasicSheet
from .excelcolumn import BasicColumn, ExcelColumn
from ..ExcelRequest.excelrequest import DeleteRequest, InsertRequest, UpdateRequest, SelectRequest

from ..ExcelModel.model import iSingleModel, ExcelModel

class ModelSheet(BasicSheet, iSingleModel):
    """Role of class is listen orders of ExcelModel and prepare request, then ask database to execute. To fulfill its obligations class should know about ALL columns in excehSheet. So for each column should be created ExcelColumn object"""
    def __init__(self, controller: "ExcelController") -> None:
        super().__init__(controller)        
        self.model_keys = self.colcontainer.get_model_keys()

    def records(self) -> int:
        request = SelectRequest(self)
        request.set_columns(('COUNT(*)',))
        return self._controller.run(request).fetchone()[0]

    ### general model interface implementation
    def find_model_by_id(self, index:int) -> ExcelModel:
        request = self._prepare_select_by_id_request()
        response = self._controller.run_with_params(request, (index,)).fetchall()[0]
        kvp = {self.model_keys[i]:response[i] for i in range(len(response))}
        return self.get_model(kvp)

    def find_model_by_expression(self, columns: tuple, values: tuple):
        """to create one model from expression like
        SELECT * FROM [Sheet1$] WHERE name = ? AND [total cost] = ?"""
        request = self._prepare_select_by_expression_request(columns)
        response = self._controller.run_with_params(request, values).fetchall()[0]
        kvp = {self.model_keys[i]:response[i] for i in range(len(response))}
        return self.get_model(kvp)

    def _prepare_select_by_expression_request(self, columns: tuple):
        request = SelectRequest(self)
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
        request = SelectRequest(self) 
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
        self._insert(record)

    def _insert(self, record:list):
        request = InsertRequest(self, self.colcontainer.columns)
        request.values_to_insert(record)
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
        self._update(record, int(model.get_id()))

    def _update(self, record:list, index):
        request = UpdateRequest(self, self.colcontainer.columns)
        request.where(self.colcontainer.get_id_column().get_selector().pugged())
        request.columns_to_update(self.colcontainer)
        formatted_values = self._format_records(record)
        formatted_values.append(index)
        self._run_db_modification(request, formatted_values)

    def delete_model(self, model: 'ExcelModel'):
        model_id = model.get_id()
        if model_id:
            request = self._delete()
            self._run_db_modification(request, (int(model_id),))

    def _delete(self):
        request =  DeleteRequest(self, self.colcontainer.columns)
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
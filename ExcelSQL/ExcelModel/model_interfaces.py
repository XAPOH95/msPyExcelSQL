class iModel:
    def get_link_to_model(self) -> 'ExcelModel':
        """Must return LINK (pointer) to ExcelModel class sibling"""
        raise NotImplementedError

class iSingleModel(iModel):
    """The interface that should be implemented in ExcelSheet if this sheet is planned to be considered as a model"""
    def find_model_by_id(self, index:int):
        raise NotImplementedError

    def find_model_by_expression(self, expression:str):
        raise NotImplementedError

    def insert_model(self, model:'ExcelModel'):
        raise NotImplementedError

    def update_model(self, model:'ExcelModel'):
        raise NotImplementedError

class iModelFabric(iModel):
    """Implementing of this interface allows to handle """
    def find_models_by_id(self, index_tuple:tuple[int]):
        raise NotImplementedError

    def find_models_by_expression(self, expression:str):
        raise NotImplementedError

    def insert_models(self, models:tuple['ExcelModel']):
        raise NotImplementedError

    def update_models(self, models:tuple['ExcelModel']):
        raise NotImplementedError
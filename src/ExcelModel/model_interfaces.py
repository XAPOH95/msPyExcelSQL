class iModel:
    def get_model(self, *args, **kwargs) -> 'ExcelModel':
        """
        MUST IMPLEMENT THIS METHOD BYSELF
        In this method *args, **kwargs should be passed in Model constructor and then return new object
                
        Basic implementation looks like:
        
        if args:
            return MyModel(args)
        else:
            return MyModel(kwargs)

        or if just key_value_pair is passed just

        return MyModel(**key_value_pair)

        Or, if your model keyword arguments doesnt match with DB columns should distribute them manually

        return MyModel(
            id = kwargs.get('identity'),
            name = kwargs.get('some_long_name_parameter_'), # whitespace is converted to underscore and # too
        )

        type can be casted while passing args, especially time/date

        period = kwargs.get('time') # "21/11/06 16:30" or None
        if period:
            period = datetime.strptime(period, %d/%m/%y %H:%M)

        return MyModel(
            id = int(kwargs.get('id')),
            name = kwargs.get('name'),
            period = period
        )

        """
        raise NotImplementedError

class iSingleModel(iModel):
    """The interface that should be implemented in ExcelSheet if this sheet is planned to be considered as a model"""
    def find_model_by_id(self, index:int):
        raise NotImplementedError

    def find_model_by_expression(self, columns:tuple, values:tuple):
        raise NotImplementedError

    def insert_model(self, model:'ExcelModel'):
        raise NotImplementedError

    def update_model(self, model:'ExcelModel'):
        raise NotImplementedError

    def delete_model(self, model:'ExcelModel'):
        raise NotImplementedError


class iModelFabric(iModel):
    """Implementing of this interface allows to handle multiply models."""
    def find_models_by_id(self, index_tuple:tuple[int]):
        raise NotImplementedError

    def find_models_by_expression(self, columns:tuple, values:tuple):
        raise NotImplementedError

    def insert_models(self, models:tuple['ExcelModel']):
        raise NotImplementedError

    def update_models(self, models:tuple['ExcelModel']):
        raise NotImplementedError

    def delete_models(self, models:tuple['ExcelModel']):
        raise NotImplementedError
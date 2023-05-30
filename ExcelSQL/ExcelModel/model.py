from .model_interfaces import iModel, iModelFabric, iSingleModel

class ModelIdentification:
    """Role of class is to solve problem of model identification"""
    db_id_column:str
    idf:int

    def __init__(self, db_id_column:str, idf:int = 0) -> None:
        self.db_id_column = db_id_column
        if isinstance(idf, int):
            self.idf = int(idf) 
        else:
            self.idf = idf


    def get_idf(self):
        return self.idf

    def update_idf(self, idf):
        self.idf = idf

    def __str__(self) -> str:
        return str(self.db_id_column)

    def __repr__(self) -> str:
        return repr(self.idf)

    def __int__(self):
        return int(self.idf)

    def __eq__(self, other: object) -> bool:
        eqInt = int(self) == other
        eqStrId = str(self.idf) == str(other)
        eqStr = str(self) == str(other)
        if any([eqInt, eqStrId, eqStr]):
            return True
        return False

class ExcelModel:
    """Role of class is to solve problem of saving and updating records in excel database
    
    To do its job class MUST know about ExcelSheet which it belongs to, so define "_sheet" attribute)
    
    If attrs name of object is different to column in excel file, attr "_alias" should be defined"""
    _sheet:iSingleModel = None
    _alias:dict = None

    def save(self):
        """Calls insert_model method of excelsheet to insert new record in file"""
        self._sheet.insert_model(self)

    def update(self):
        self._sheet.update_model(self)

    def delete(self):
        """Delete a record for model in excel file. Actually its not delete, its UPDATE the record to NULL due to excel specials."""
        self._sheet.delete_model(self)

    def get_id(self):
        """returns Modeldentification object"""
        for attr in self.__dict__.values():
            if isinstance(attr, ModelIdentification):
                return attr
        return None

    def assign_id(self, index):
        """Assign will be successfull only if entity has ModelIdentification attr"""
        idf = self.get_id()
        if idf is None:
            return
        idf.update_idf(index)

    def __iter__(self):
        kvp = self.__iter__get_kvp()
        for key, value in kvp.items():
            if isinstance(value, ModelIdentification):
                yield (str(value), value.get_idf())
            elif isinstance(value, ExcelModel):
                yield (key, value.get_id())
            else:
                yield (key, value)

    def __iter__get_kvp(self) -> dict:
        kvp = {k:v for k, v in self.__dict__. items() if not k.startswith('_')}
        if self._alias:
            return {self._alias.get(key, key):value for key, value in kvp.items()}
        return kvp
from ..ExcelRequest.excelrequest import DeleteRequest, InsertRequest, UpdateRequest, SelectRequest

class iInsert:
    def insert(self):
        raise NotImplementedError

class iDelete:
    def delete(self):
        raise NotImplementedError

class iSelect:
    def select(self):
        raise NotImplementedError

class iFind:
    def find(self):
        raise NotImplementedError

class iUpdate:
    def update(self):
        raise NotImplementedError

class Commands(iInsert, iDelete, iSelect, iFind, iUpdate):
    """Base implementation"""
    def insert(self, columns):
        return InsertRequest(self, columns)

    def delete(self, columns):
        return DeleteRequest(self, columns)

    def update(self, columns):
        return UpdateRequest(self, columns)

    def select(self):
        return SelectRequest(self)

    def find(self, columns:tuple, where:str):
        request = SelectRequest(self, columns)
        request.where(where)
        return request
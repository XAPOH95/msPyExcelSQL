import unittest
from src.ExcelRequest.excelrequest import ExcelRequest, SelectRequest, UpdateRequest, InsertRequest, DeleteRequest
from src.ExcelSheet.excelcolumn import ExcelColumn

class ExcelRequestTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """MOCKING SHEET NAME"""
        class ExcelRequest_mocked(ExcelRequest):
            pass

        class SelectRequest_mocked(SelectRequest):
            def __init__(self, columns: tuple['ExcelColumn'] = None) -> None:
                super().__init__('[Sheet1$]', columns)

        class UpdateRequest_mocked(UpdateRequest):
            def __init__(self, columns: tuple['ExcelColumn'] = None) -> None:
                super().__init__('[Sheet1$]', columns)

        class InsertRequest_mocked(InsertRequest):
            def __init__(self, columns: tuple['ExcelColumn'] = None) -> None:
                super().__init__('[Sheet1$]', columns)

        class DeleteRequest_mocked(DeleteRequest):
            def __init__(self, columns: tuple['ExcelColumn']) -> None:
                super().__init__('[Sheet1$]', columns)

        cls.excelRequest_mocked = ExcelRequest_mocked
        cls.selectRequest_mocked = SelectRequest_mocked
        cls.updateRequest_mocked = UpdateRequest_mocked
        cls.insertRequest_mocked = InsertRequest_mocked
        cls.deleteRequest_mocked = DeleteRequest_mocked

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    ### Block of test methods

    @unittest.skip('Performance check')
    def test_performance(self):
        import datetime
        start = datetime.datetime.now()
        ## код здесь
        end = datetime.datetime.now() - start
        print(f'Done in {end} s.')

    def test_can_init_excelrequest(self):
        x = self.excelRequest_mocked('Sheet1$')
        pass

    def test_can_init_select(self):
        x = self.selectRequest_mocked((
            ExcelColumn('Sheet1$', 'id', int),
            ExcelColumn('Sheet1$', 'total value', float),
        ))
        pass

    def test_select_sql_request_to_excel_workbook(self):
        awaited_select_all = "SELECT * FROM [Sheet1$]"
        awaited_select_few = "SELECT id, [total value] FROM [Sheet1$]"
        awaited_select_few_where = "SELECT id, [total value] FROM [Sheet1$] WHERE id = ?"
        awaited_between = "SELECT id FROM [Sheet1$] WHERE id BETWEEN ? AND ?"
        awaited_group_by = "SELECT name, COUNT(*) FROM [Sheet1$] GROUP BY name"
        awaited_group_by_having = "SELECT name, COUNT(*) FROM [Sheet1$] GROUP BY name HAVING COUNT(*) > ?"
        awaited_like = "SELECT name FROM [Sheet1$] WHERE name LIKE ?"
        awaited_distinct = "SELECT DISTINCT name FROM [Sheet1$]"
        awaited_limit = "SELECT * FROM [Sheet1$] LIMIT 10"
        awaited_or = "SELECT * FROM [Sheet1$] WHERE ? OR ?"
        awaited_in = 'SELECT * FROM [Sheet1$] WHERE id IN (value1, value2)'

        columnsTuple = (ExcelColumn('Sheet1$', 'id', int),
                ExcelColumn('Sheet1$', 'total value', float),
                ExcelColumn('Sheet1$', 'name', str))

        request = self.selectRequest_mocked()
        self.assertEqual(awaited_select_all, str(request))

        request.set_columns(columnsTuple[:2])
        self.assertEqual(awaited_select_few, str(request))

        request.where(f'{columnsTuple[0].get_selector().pugged()}')
        self.assertEqual(awaited_select_few_where, str(request))

        request.where(f"{columnsTuple[0]} BETWEEN ? AND ?")
        request.columns = str(columnsTuple[0])
        self.assertEqual(awaited_between, str(request))

        request.where()
        request.group_by(str(columnsTuple[2]))
        request.columns = f'{columnsTuple[2]},'
        request.agregation("COUNT(*)")
        self.assertEqual(awaited_group_by, str(request))

        request.having("COUNT(*) > ?")
        self.assertEqual(awaited_group_by_having, str(request))

        request.agregation()
        request.group_by()
        request.having()
        request.columns = str(columnsTuple[2])
        request.where(str(columnsTuple[2]))
        request.like('?')
        self.assertEqual(awaited_like, str(request))

        request.distinct(True)
        request.where()
        request.like()
        self.assertEqual(awaited_distinct, str(request))

        request.limit(10)
        request.distinct(False)
        request.columns = "*"
        self.assertEqual(awaited_limit, str(request))

        request.limit()
        request.where("? OR ?")
        self.assertEqual(awaited_or, str(request))

        request.where(str(columnsTuple[0]))
        request.set_in(('value1, value2'))
        self.assertEqual(awaited_in, str(request))

    def test_update_sql_request_to_excel_workbook(self):
        awaited = "UPDATE [Sheet1$] SET id = ?, [total value] = ?, name = ? WHERE id = ?"

        columnsTuple = (ExcelColumn('Sheet1$', 'id', int),
                ExcelColumn('Sheet1$', 'total value', float),
                ExcelColumn('Sheet1$', 'name', str))

        update = self.updateRequest_mocked(columnsTuple)
        update.columns_to_update(columnsTuple)
        update.where(f'{columnsTuple[0]} = ?')
        self.assertEqual(awaited, str(update))

    def test_insert_sql_request_to_excel_workbook(self):
        awaited_some_columns = 'INSERT INTO [Sheet1$] (id, [total value]) VALUES (?, ?)'
        awaited_all = 'INSERT INTO [Sheet1$] VALUES (?, ?, ?)'

        columnsTuple = (ExcelColumn('Sheet1$', 'id', int),
                ExcelColumn('Sheet1$', 'total value', float),
                ExcelColumn('Sheet1$', 'name', str))

        insert = self.insertRequest_mocked()
        insert.values_to_insert((10, 'X', 12.8))
        self.assertEqual(awaited_all, str(insert))

        insert_2 = self.insertRequest_mocked(columnsTuple[:2])
        insert_2.values_to_insert((19, 'X'))
        self.assertEqual(awaited_some_columns, str(insert_2))

        with self.assertRaises(IndexError):
            insert = self.insertRequest_mocked(columnsTuple)
            insert.values_to_insert((1, 2, 3, 4))


    def test_delete_sql_request_to_excel_workbook(self):
        awaited = "UPDATE [Sheet1$] SET id = NULL, [total value] = NULL, name = NULL WHERE id = ?"

        columnsTuple = (ExcelColumn('Sheet1$', 'id', int),
                ExcelColumn('Sheet1$', 'total value', float),
                ExcelColumn('Sheet1$', 'name', str))

        deleteR = self.deleteRequest_mocked(columnsTuple)
        deleteR.where(str(columnsTuple[0]) + ' = ?')
        self.assertEqual(awaited, str(deleteR))
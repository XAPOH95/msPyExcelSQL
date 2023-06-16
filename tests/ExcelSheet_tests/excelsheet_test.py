import unittest
from src.ExcelSheet.excelsheet import ExcelSheet
from src.ExcelSheet.excelcolumn import ExcelColumn, ExcelColumnContainer, DatetimeColumn
from src.ExcelRequest.requestUtils import Agregator

from datetime import datetime

class ExcelSheetTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        class FakeCursor:
            def fetchall(self):
                return 'fetchall'

            def fetchone(self):
                return 'fetchone'

        class FakeController:
            def run(self, request):
                return FakeCursor()

            def run_with_params(self, request, params:tuple):
                return FakeCursor()

        class Excel_mockedSheet(ExcelSheet):
            def __init__(self) -> None:
                self.a = ExcelColumn(self, 'A', int)
                self.b = ExcelColumn(self, 'B', float)
                self.c = ExcelColumn(self, 'C', str)
                self.total_cost = ExcelColumn(self, 'total cost', float)
                self.comp_inc = ExcelColumn(self, 'comp.inc.', float)
                self.period = DatetimeColumn(self, 'period', '')
                super().__init__(FakeController())

        cls.excelSheet_mocked = Excel_mockedSheet

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

    def test_can_init_excelsheet(self):
        excelsheet = self.excelSheet_mocked()
        self.assertIsNotNone(excelsheet)

    def test_can_convert_column_names_to_model_case(self):
        awaited = ('A', 'B', 'C', 'total_cost', 'comp_inc_', 'period')
        awaited_excel = 'A, B, C, [total cost], comp#inc#, period'
        excelsheet = self.excelSheet_mocked()
        result = excelsheet.colcontainer.get_model_keys()
        result_excel = excelsheet.colcontainer.get_columns()
        self.assertTupleEqual(awaited, result)
        self.assertEqual(awaited_excel, result_excel)

    def test_can_count_records(self):
        awaited = 'f'
        records = self.excelSheet_mocked().records()
        self.assertEqual(awaited, records)

    def test_ExcelSheet_to_str_return_excel_formatted_name(self):
        """Due to specials of ms excel ODBC SQL dialect all sheets should end with $ sign"""
        awaited = '[Excel_mocked$]'
        result = str(self.excelSheet_mocked())
        self.assertEqual(awaited, result)


class ExcelColumnTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        class ExcelColumn_mocked(ExcelColumn):
            def __init__(self, title: str, valuetype) -> None:
                super().__init__('mySheet$', title, valuetype)

        cls.excelColumn_mocked = ExcelColumn_mocked

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

    def test_can_init_excelcolumn(self):
        c1 = self.excelColumn_mocked('A', int)
        c2 = self.excelColumn_mocked('B', str)
        c3 = self.excelColumn_mocked('C', float)
        pass

    def test_can_cast_datetime_on_column(self):
        awaited = '2023-10-25 00:00:00'
        awaited_with_hm = '2023-10-25 19:08:00'

        period = DatetimeColumn('[Sheet1]', 'period', ('%d/%m/%Y',))
        
        result_date = period.to_format('25/10/2023')

        with self.assertRaises(ValueError):
            period.to_format('25/10/2023 19:08')

        new_period = DatetimeColumn('[Sheet1$]', 'period', ('%d/%m/%Y', '%d/%m/%Y %H:%M'))

        result_with_hm = new_period.to_format('25/10/2023 19:08')

        result_datetime_to_datetime = new_period.to_format(datetime.now())

        self.assertEqual(awaited, str(result_date))
        self.assertEqual(awaited_with_hm, str(result_with_hm))

    def test_can_str_column(self):
        awaited = 'my_regular_column'
        awaited_with_ws = '[my wrecked column]'
        awaited_with_dot = 'm#wr#col#'
        awaited_with_ws_and_dot = '[m# wr# col#]'

        result = self.excelColumn_mocked('my_regular_column', str)
        result_with_ws = self.excelColumn_mocked('my wrecked column', str)
        result_with_dot = self.excelColumn_mocked('m.wr.col.', str)
        result_with_dot_and_ws = self.excelColumn_mocked('m. wr. col.', str)
        self.assertEqual(awaited, str(result))
        self.assertEqual(awaited_with_ws, str(result_with_ws))
        self.assertEqual(awaited_with_dot, str(result_with_dot))
        self.assertEqual(awaited_with_ws_and_dot, str(result_with_dot_and_ws))

    def test_can_cast_format(self):
        awaited = 1
        awaited2 = '2077'
        awaited3 = 2.2
        result1 = self.excelColumn_mocked('A', int)
        result2 = self.excelColumn_mocked('B', str)
        result3 = self.excelColumn_mocked('C', float)

        self.assertEqual(awaited, result1.to_format(1))
        self.assertEqual(awaited2, result2.to_format("2077"))
        self.assertEqual(awaited3, result3.to_format("2.2"))

class AgregatorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        class Agregator_mocked(Agregator):
            pass

        cls.agregator_mocked = Agregator_mocked

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_can_init_agregator(self):
        col = 'my_cool_column'

        awaited_COUNT = f"COUNT({col})"
        awaited_SUM = f"SUM({col})"
        awaited_AVG = f"AVG({col})"
        awaited_MIN = f"MIN({col})"
        awaited_MAX = f"MAX({col})"

        ec = ExcelColumn('Sheet$', col, float)
        agr = self.agregator_mocked(ec)

        result_count = agr.count()
        result_sum = agr.sum()
        result_avg = agr.avg()
        result_min = agr.min()
        result_max = agr.max()

        self.assertEqual(awaited_COUNT, result_count)
        self.assertEqual(awaited_SUM, result_sum)
        self.assertEqual(awaited_AVG, result_avg)
        self.assertEqual(awaited_MIN, result_min)
        self.assertEqual(awaited_MAX, result_max)

    def test_can_init_agregator_with_whitespaces(self):
        col = 'my cool column'

        awaited_COUNT = f"COUNT([{col}])"
        awaited_SUM = f"SUM([{col}])"
        awaited_AVG = f"AVG([{col}])"
        awaited_MIN = f"MIN([{col}])"
        awaited_MAX = f"MAX([{col}])"

        ec = ExcelColumn('Sheet$', col, float)
        agr = self.agregator_mocked(ec)

        result_count = agr.count()
        result_sum = agr.sum()
        result_avg = agr.avg()
        result_min = agr.min()
        result_max = agr.max()

        self.assertEqual(awaited_COUNT, result_count)
        self.assertEqual(awaited_SUM, result_sum)
        self.assertEqual(awaited_AVG, result_avg)
        self.assertEqual(awaited_MIN, result_min)
        self.assertEqual(awaited_MAX, result_max)

class ExcelColumnContainerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class MyExcelSheet:
            idi = ExcelColumn('[Sheet1$]', 'id', int)
            title = ExcelColumn('[Sheet1$]', 'title', str)
            total = ExcelColumn('[Sheet1$]', 'total', float)
            col_with_ws = ExcelColumn('[Sheet1$]', 'total value of something', float)

        class ExcelColumnContainer_mocked(ExcelColumnContainer):
            pass

        cls.excelColumnContainer_mocked = ExcelColumnContainer_mocked
        cls.ExcelSheet = MyExcelSheet()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_can_get_columns_and_pug_from_excelsheet(self):
        awaited_columns = 'id, title, total, [total value of something]'
        awaited_pug = '(?, ?, ?, ?)'
        container = self.excelColumnContainer_mocked(self.ExcelSheet)
        cols = container.get_columns()
        pug = container.get_pug()
        self.assertEqual(awaited_columns, cols)
        self.assertEqual(awaited_pug, pug)

        
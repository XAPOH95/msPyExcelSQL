import unittest
from ExcelSQL.ExcelController.excelcontroller import ExcelController

class ExcelControllerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        class FakeCursor:
            def execute(self, *args):
                return args

        class FakeConnection:
            def __init__(self, path:str) -> None:
                self.path = path
            def cursor(self):
                return FakeCursor()

        class ExcelController_mocked(ExcelController):
            db = FakeConnection('path/to/file.xlsx')

            def get_cursor(self):
                return super()._get_cursor()

        cls.excelController_mocked = ExcelController_mocked

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

    def test_can_create_ExcelController(self):
        controller = self.excelController_mocked()
        self.assertIsNotNone(controller)

    def test_can_get_cursor(self):
        controller = self.excelController_mocked()
        cursor = controller.get_cursor()
        self.assertIsNotNone(cursor)

    def test_can_run_statement(self):
        awaited = ('SELECT * FROM myTable$',)
        awaited_with_params = ('SELECT * FROM myTable$ WHERE id = ? AND year = ?', (10, 2023))

        controller = self.excelController_mocked()
        result = controller.run("""SELECT * FROM myTable$""")
        result_with_params = controller.run_with_params("""SELECT * FROM myTable$ WHERE id = ? AND year = ?""", (10, 2023))

        self.assertTupleEqual(awaited, result)
        self.assertTupleEqual(awaited_with_params, result_with_params)
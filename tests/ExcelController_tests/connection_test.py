import unittest
from ExcelSQL.ExcelController.connection import Connection

class ConnectionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        class Connection_mocked(Connection):
            def __new__(cls):
                return super().__new__(cls, 'tests\example.xlsx')

        cls.connection_mocked = Connection_mocked

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

    def test_can_create_connection(self):
        connection = self.connection_mocked()
        self.assertIsNotNone(connection)
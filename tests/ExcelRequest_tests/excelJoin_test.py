import unittest

from ExcelSQL.ExcelRequest.excelJoin import JoinRequest

class RequestJoinTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        class JoinRequest_mocked(JoinRequest):
            pass

            def get_protected_ON(self):
                return self._on

            def get_protected_COLUMNS(self):
                return self._columns

            def get_protected_WHERE(self):
                return self._where

        cls.joinRequest = JoinRequest_mocked

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

    def test_can_get_join_request(self):
        bands_sheet = '[bands$]'
        musicians_sheet = '[musicians$]'
        select = f"SELECT {bands_sheet}.band, {musicians_sheet}.name "
        from_ = f"FROM {bands_sheet} "
        how = f"INNER JOIN {musicians_sheet} "
        on = f"ON {bands_sheet}.id = {musicians_sheet}.band_id"
        awaited = select + from_ + how + on

        result = self.joinRequest('[bands$]', '[musicians$]')
        result.set_columns(('band',),('name',))
        result.inner()
        result.join_on(('id',), ('band_id',))

        self.assertEqual(awaited, str(result))

    def test_can_get_join_request_of_three_and_more_sheets(self):
        pass

    def test_can_join_on_many_cols(self):
        awaited = 'ON [Sheet1$].id = [Sheet2$].ref, [Sheet1$].name_id = [Sheet2$].name, [Sheet1$].total_id = [Sheet2$].total'

        result = self.joinRequest('[Sheet1$]', '[Sheet2$]')
        result.join_on(
            ('id', 'name_id', 'total_id'),
            ('ref', 'name', 'total')
        )

        self.assertEqual(awaited, result.get_protected_ON())

    def test_can_set_columns(self):
        awaited = '[bands$].band, [bands$].location, [bands$].number_of_candys, [musicians$].name'
        result = self.joinRequest('[bands$]', '[musicians$]')
        result.set_columns(('band', 'location', 'number_of_candys'), ('name',))
        self.assertEqual(awaited, result.get_protected_COLUMNS())

        result.reset_columns()
        self.assertEqual('*', result.get_protected_COLUMNS())

    def test_can_join_where(self):
        awaited = 'WHERE [Sheet1$].id = ? AND [Sheet2$].name_id = ?'

        result = self.joinRequest('[Sheet1$]', '[Sheet2$]')
        result.join_on(
            ('id', 'name_id', 'total_id'),
            ('ref', 'name', 'total')
        )
        result.where('[Sheet1$].id = ? AND [Sheet2$].name_id = ?')

        self.assertEqual(awaited, result.get_protected_WHERE())
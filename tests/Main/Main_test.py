import unittest
from datetime import datetime

from ExcelSQL.Main import Connection
from ExcelSQL.Main import ExcelController
from ExcelSQL.Main import ModelIdentification, ExcelModel
from ExcelSQL.Main import ModelSheet
from ExcelSQL.Main import ExcelColumn, IdColumn, DatetimeColumn

# if True skips excel inserting/updating
DENIED_DB_MODIFICATION = True

# @unittest.skip("Excel file modification")
class Main(unittest.TestCase):
    """
    Example how this module should work
    """

    @classmethod
    def setUpClass(cls):
        ### NOTHING IS MOCKED!!!
              
        class ExampleExcelFileController(ExcelController):
            def __init__(self) -> None:
                self.db = Connection('tests/example.xlsx')

        class bandsSheet(ModelSheet):
            def __init__(self) -> None:
                self.idi = IdColumn(self, 'id', int)
                self.band = ExcelColumn(self, 'band', str)
                self.genre = ExcelColumn(self, 'genre', str)
                self.origin = ExcelColumn(self, 'origin', str)
                self.year_of_foundation = ExcelColumn(self, 'year_of_foundation', int)
                self.status = ExcelColumn(self, 'status', int)
                super().__init__(ExampleExcelFileController())

            def get_model(self, kvp:dict) -> 'ExcelModel':
                return Band(
                    id = kvp.get('id'),
                    band = kvp.get('band'),
                    genre = kvp.get('genre'),
                    origin = kvp.get('origin'),
                    status = kvp.get('status'),
                    year_of_foundation = kvp.get('year_of_foundation'),                    
                )

        class albumsSheet(ModelSheet):
            def __init__(self) -> None:
                self.idi = IdColumn(self, "id", int)
                self.band_id = ExcelColumn(self, "band_id", int)
                self.discography = ExcelColumn(self, "discography", str)
                self.release = ExcelColumn(self, "release", int)
                super().__init__(ExampleExcelFileController())

            def get_model(self, kvp:dict) -> 'ExcelModel':
                return Album(**kvp)

        class musiciansSheet(ModelSheet):
            def __init__(self) -> None:
                self.idi = IdColumn(self, "id", int)
                self.band_id = ExcelColumn(self, "band_id", int)
                self.name = ExcelColumn(self, "name", str)
                self.musical_instrument = ExcelColumn(self, "musical_instrument", str)
                self.vocal = ExcelColumn(self, "vocal", str)
                self.status = ExcelColumn(self, "status", int)
                super().__init__(ExampleExcelFileController())

            def get_model(self, kvp:dict) -> 'ExcelModel':
                return Musician(**kvp)

        class Band(ExcelModel):
            _alias = {'year':'year_of_foundation'}

            def __init__(self, id:int, band:str, genre:str, origin:str, year_of_foundation:int, status:bool) -> None:
                self._sheet = bandsSheet()
                
                self.idi = ModelIdentification('id', id)
                self.band = band
                self.genre = genre
                self.origin = origin
                self.year = int(year_of_foundation)
                self.status = bool(status)

            def __str__(self) -> str:
                return str(self.band)

        class Album(ExcelModel):
            _alias = {'band':'band_id'}

            def __init__(self, id:int, band_id:int, discography:str, release:int) -> None:
                self._sheet = albumsSheet()
                
                self.idi = ModelIdentification('id', id)
                self.band = bandsSheet().find_model_by_id(band_id)
                self.discography = discography
                self.release = int(release)

        class Musician(ExcelModel):
            _alias = {'band':'band_id', 'instrument':'musical_instrument'}

            def __init__(self, id:int, band_id:int, name:str, musical_instrument:str, vocal:str, status:bool) -> None:
                self._sheet = musiciansSheet()
                
                self.idi = ModelIdentification('id', id)
                self.band = bandsSheet().find_model_by_id(band_id)
                self.name = name
                self.instrument = musical_instrument
                self.vocal = vocal
                self.status = bool(status)

        cls.band = Band
        cls.album = Album
        cls.musician = Musician

        cls.BandsSheet = bandsSheet
        cls.AlbumsSheet = albumsSheet
        cls.MusiciansSheet = musiciansSheet

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

    def test_can_select_band(self):
        awaited_ArchEnemy = (1, 'arch enemy', 'melodic death metal', 'Halmstad, Sweden', 1995, True)

        ArchEnemy = self.BandsSheet().find_model_by_id(1)

        ArchEnemy_tupled = tuple(dict(ArchEnemy).values())
        self.assertTupleEqual(awaited_ArchEnemy, ArchEnemy_tupled)
    
    def test_can_select_album(self):
        awaited_GodHatesUsAll = (27, 3, 'God Hates Us All', 2001)
        awaited_band = 'slayer'

        GodHatesUsAll = self.AlbumsSheet().find_model_by_id(27)
        Slayer = GodHatesUsAll.band

        GodHatesUsAll_tupled = tuple(dict(GodHatesUsAll).values())
        self.assertTupleEqual(awaited_GodHatesUsAll, GodHatesUsAll_tupled)
        self.assertEqual(awaited_band, str(Slayer))

    def test_can_select_musician(self):
        awaited_Alissa = (4, 1, 'Alissa White-Gluz', None, 'lead', True)
        awaited_band = 'arch enemy'

        AlissaWhiteGluz = self.MusiciansSheet().find_model_by_id(4)
        ArchEnemy = AlissaWhiteGluz.band

        Alissa_tupled = tuple(dict(AlissaWhiteGluz).values())
        self.assertTupleEqual(awaited_Alissa, Alissa_tupled)
        self.assertEqual(awaited_band, str(ArchEnemy))

    ### insert
    def test_can_insert_band(self):
        awaited_request = 'INSERT INTO [bands$] (id, band, genre, origin, year_of_foundation, status) VALUES (?, ?, ?, ?, ?, ?)'
        awaited_params = (5, 'anthrax', 'thrash metal', 'New York City, US', 1981, 1)

        class bandsSheet(self.BandsSheet):
            FAKE_request = None
            FAKE_params = None

            def _run_db_modification(self, request:str, params:list):
                """Mocked
                Original method db modif by inserting new row, mocked method sets two FAKE attrs that can be checked
                """
                self.FAKE_request = request
                self.FAKE_params = tuple(params)

        class mocked_Band(self.band):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
                self._sheet = bandsSheet()
                
            def check_db_modification(self):
                return self._sheet.FAKE_request, self._sheet.FAKE_params

        band = mocked_Band(None, "anthrax", "thrash metal", "New York City, US", 1981, True)
        band.save()

        result_request, result_params = band.check_db_modification()

        self.assertEqual(awaited_request, str(result_request))
        self.assertTupleEqual(awaited_params, tuple(result_params))

    def test_can_insert_album(self):
        awaited_request = 'INSERT INTO [albums$] (id, band_id, discography, release) VALUES (?, ?, ?, ?)'
        awaited_params = (46, 1, 'Wacken 2016 life', 2016)

        class albumsSheet(self.AlbumsSheet):
            FAKE_request = None
            FAKE_params = None

            def _run_db_modification(self, request:str, params:list):
                """Mocked
                Original method db modif by inserting new row, mocked method sets two FAKE attrs that can be checked
                """
                self.FAKE_request = request
                self.FAKE_params = tuple(params)

        class mocked_Album(self.album):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
                self._sheet = albumsSheet()
                
            def check_db_modification(self):
                return self._sheet.FAKE_request, self._sheet.FAKE_params

        album = mocked_Album(None, 1, "Wacken 2016 life", 2016)
        album.save()

        result_request, result_params = album.check_db_modification()

        self.assertEqual(awaited_request, str(result_request))
        self.assertTupleEqual(awaited_params, tuple(result_params))

    def test_can_insert_musician(self):
        awaited_request = 'INSERT INTO [musicians$] (id, band_id, name, musical_instrument, vocal, status) VALUES (?, ?, ?, ?, ?, ?)'
        awaited_params = (19, 1, 'Mick Gordon', 'guitar', None, 1)

        class musiciansSheet(self.MusiciansSheet):
            FAKE_request = None
            FAKE_params = None

            def _run_db_modification(self, request:str, params:list):
                """Mocked
                Original method db modif by inserting new row, mocked method sets two FAKE attrs that can be checked
                """
                self.FAKE_request = request
                self.FAKE_params = tuple(params)

        class mocked_Musician(self.musician):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
                self._sheet = musiciansSheet()
                
            def check_db_modification(self):
                return self._sheet.FAKE_request, self._sheet.FAKE_params

        musician = mocked_Musician(None, 1, "Mick Gordon", "guitar", None, True)
        musician.save()

        result_request, result_params = musician.check_db_modification()

        self.assertEqual(awaited_request, str(result_request))
        self.assertTupleEqual(awaited_params, tuple(result_params))

    ### update
    def test_can_update_band(self):
        awaited_request = 'UPDATE [bands$] SET id = ?, band = ?, genre = ?, origin = ?, year_of_foundation = ?, status = ? WHERE id = ?'
        awaited_params = (3, 'slayer', 'speed metal', 'Huntington Park, California, US', 1981, 1, 3)

        class bands_mockedSheet(self.BandsSheet):
            FAKE_request = None
            FAKE_params = None

            def __str__(self) -> str:
                return '[bands$]'

            def _run_db_modification(self, request:str, params:list):
                """Mocked
                Original method db modif by inserting new row, mocked method sets two FAKE attrs that can be checked
                """
                self.FAKE_request = request
                self.FAKE_params = tuple(params)

            def get_model(self, kvp:dict):
                return mocked_Band(**kvp)

        class mocked_Band(self.band):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
                self._sheet = bands_mockedSheet()
                
            def check_db_modification(self):
                return self._sheet.FAKE_request, self._sheet.FAKE_params

        Slayer = bands_mockedSheet().find_model_by_id(3)
        Slayer.status = True
        Slayer.genre = "speed metal"
        Slayer.update()

        result_request, result_params = Slayer.check_db_modification()

        self.assertEqual(awaited_request, str(result_request))
        self.assertTupleEqual(awaited_params, tuple(result_params))

    def test_can_update_album(self):
        awaited_request = 'UPDATE [albums$] SET id = ?, band_id = ?, discography = ?, release = ? WHERE id = ?'
        awaited_params = (27, 3, 'God Hates Us All remaster', 2020, 27)

        class albums_mockedSheet(self.AlbumsSheet):
            FAKE_request = None
            FAKE_params = None

            def __str__(self) -> str:
                return '[albums$]'

            def _run_db_modification(self, request:str, params:list):
                """Mocked
                Original method db modif by inserting new row, mocked method sets two FAKE attrs that can be checked
                """
                self.FAKE_request = request
                self.FAKE_params = tuple(params)

            def get_model(self, kvp:dict):
                return mocked_Album(**kvp)

        class mocked_Album(self.album):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
                self._sheet = albums_mockedSheet()
                
            def check_db_modification(self):
                return self._sheet.FAKE_request, self._sheet.FAKE_params

        GodHatesUsAll = albums_mockedSheet().find_model_by_id(27)
        GodHatesUsAll.discography = 'God Hates Us All remaster'
        GodHatesUsAll.release = 2020
        GodHatesUsAll.update()

        result_request, result_params = GodHatesUsAll.check_db_modification()

        self.assertEqual(awaited_request, str(result_request))
        self.assertTupleEqual(awaited_params, tuple(result_params))

    def test_can_update_musician(self):
        awaited_request = 'UPDATE [musicians$] SET id = ?, band_id = ?, name = ?, musical_instrument = ?, vocal = ?, status = ? WHERE id = ?'
        awaited_params = (4, 1, 'Alissa White-Gluz', 'violin', 'lead', 1, 4)

        class musicians_mockedSheet(self.MusiciansSheet):
            FAKE_request = None
            FAKE_params = None

            def __str__(self) -> str:
                return '[musicians$]'

            def _run_db_modification(self, request:str, params:list):
                """Mocked
                Original method db modif by inserting new row, mocked method sets two FAKE attrs that can be checked
                """
                self.FAKE_request = request
                self.FAKE_params = tuple(params)

            def get_model(self, kvp:dict):
                return mocked_Musician(**kvp)

        class mocked_Musician(self.musician):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
                self._sheet = musicians_mockedSheet()
                
            def check_db_modification(self):
                return self._sheet.FAKE_request, self._sheet.FAKE_params

        AlissaWhiteGluz = musicians_mockedSheet().find_model_by_id(4)
        AlissaWhiteGluz.instrument = 'violin'
        AlissaWhiteGluz.update()

        result_request, result_params = AlissaWhiteGluz.check_db_modification()

        self.assertEqual(awaited_request, str(result_request))
        self.assertTupleEqual(awaited_params, tuple(result_params))

    def test_can_delete_band(self):
        awaited_request = "UPDATE [bands$] SET id = NULL, band = NULL, genre = NULL, origin = NULL, year_of_foundation = NULL, status = NULL WHERE id = ?"
        awaited_params = (3, )

        class bands_mockedSheet(self.BandsSheet):
            FAKE_request = None
            FAKE_params = None

            def __str__(self) -> str:
                return '[bands$]'

            def _run_db_modification(self, request:str, params:list):
                """Mocked
                Original method db modif by inserting new row, mocked method sets two FAKE attrs that can be checked
                """
                self.FAKE_request = request
                self.FAKE_params = tuple(params)

            def get_model(self, kvp:dict):
                return mocked_Band(**kvp)

        class mocked_Band(self.band):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
                self._sheet = bands_mockedSheet()
                
            def check_db_modification(self):
                return self._sheet.FAKE_request, self._sheet.FAKE_params

        Slayer = bands_mockedSheet().find_model_by_id(3)
        Slayer.delete()
        result_request, params = Slayer.check_db_modification()

        self.assertEqual(awaited_request, str(result_request))
        self.assertTupleEqual(awaited_params, params)

    def test_can_find_band_model_by_expression(self):
        awaited_Slayer = (3, 'slayer', 'thrash metal', 'Huntington Park, California, US', 1981, False)
        Slayer = self.BandsSheet().find_model_by_expression(('genre', 'status'), ('thrash metal', 0))
        tupled_Slayer = tuple(dict(Slayer).values())
        self.assertTupleEqual(awaited_Slayer, tupled_Slayer)

    def test_can_find_album_model_by_expression(self):
        awaited_GodHatesUsAll = (27, 3, 'God Hates Us All', 2001)
        GodHatesUsAll = self.AlbumsSheet().find_model_by_expression(('discography', 'release'), ('God Hates Us All', 2001))
        tupled_GodHatesUsAll = tuple(dict(GodHatesUsAll).values())
        self.assertTupleEqual(awaited_GodHatesUsAll, tupled_GodHatesUsAll)

    def test_can_find_musician_by_expression(self):
        awaited_TomAraya = (12, 3, 'Tom Araya', 'bass', 'lead', False)
        musicianSheet = self.MusiciansSheet()
        TomAraya = musicianSheet.find_model_by_expression(
            columns=(
                musicianSheet.musical_instrument,
                musicianSheet.vocal
            ),
            values=("bass", "lead")
        )
        tupled_TomAraya = tuple(dict(TomAraya).values())
        self.assertTupleEqual(awaited_TomAraya, tupled_TomAraya)

    ### modification of excel file. 
    # To reset have to restore backup or copypaste values from RESERVE_SHEET
    # Or, before running test, open example.xlsx and then run tests. When tests are finished and modifications appeared, just close file without saving.
    @unittest.skipIf(DENIED_DB_MODIFICATION, 'Mod of excel file is not allowed')
    def test_can_delete_record_IN_EXCEL_band(self):
        AtTheGates = self.band(2, 'at the gates', 'melodic death metal', 'Gothenburg, Sweden', 1990, 1)
        Kreator = self.BandsSheet().find_model_by_id(4)
        AtTheGates.delete()
        Kreator.delete()
    
    ### insert
    @unittest.skipIf(DENIED_DB_MODIFICATION, 'Mod of excel file is not allowed')
    def test_can_insert_TO_EXCEL_band(self):
        band = self.band(None, "anthrax", "thrash metal", "New York City, US", 1981, True)
        band.save()


    @unittest.skipIf(DENIED_DB_MODIFICATION, 'Mod of excel file is not allowed')
    def test_can_insert_TO_EXCEL_album(self):
        album = self.album(None, 1, "Wacken 2016 life", 2016)
        album.save()


    @unittest.skipIf(DENIED_DB_MODIFICATION, 'Mod of excel file is not allowed')
    def test_can_insert_TO_EXCEL_musician(self):
        musician = self.musician(None, 1, "Mick Gordon", "guitar", None, True)
        musician.save()


    ### update
    @unittest.skipIf(DENIED_DB_MODIFICATION, 'Mod of excel file is not allowed')
    def test_can_update_IN_EXCEL_band(self):
        Slayer = self.BandsSheet().find_model_by_id(3)
        Slayer.status = True
        Slayer.genre = "speed metal"
        Slayer.update()

    @unittest.skipIf(DENIED_DB_MODIFICATION, 'Mod of excel file is not allowed')
    def test_can_update_IN_EXCEL_album(self):
        GodHatesUsAll = self.AlbumsSheet().find_model_by_id(27)
        GodHatesUsAll.discography = 'God Hates Us All remaster'
        GodHatesUsAll.release = 2020
        GodHatesUsAll.update()

    @unittest.skipIf(DENIED_DB_MODIFICATION, 'Mod of excel file is not allowed')
    def test_can_update_IN_EXCEL_musician(self):
        AlissaWhiteGluz = self.MusiciansSheet().find_model_by_id(4)
        AlissaWhiteGluz.instrument = 'violin'
        AlissaWhiteGluz.update()

class DatetimeColumnTest(unittest.TestCase):
    """Testcases for read/write datetime in excel formats"""
    @classmethod
    def setUpClass(cls):
        ### NOTHING IS MOCKED!!!
              
        class ExampleExcelFileController(ExcelController):
            def __init__(self) -> None:
                self.db = Connection('tests/example.xlsx')

        class festivalsSheet(ModelSheet):
            def __init__(self) -> None:
                self.identification = IdColumn(self, 'id', int)
                self.title = ExcelColumn(self, 'title', str)
                self.location = ExcelColumn(self, 'location', str)
                self.period = DatetimeColumn(self, 'period', ('%d/%m/%Y', '%d/%m/%Y %H:%M'))
                super().__init__(ExampleExcelFileController())

            def get_model(self, kvp:dict) -> 'ExcelModel':
                return Festival(**kvp)

        class Festival(ExcelModel):
            _alias = {'name':'title'}
            def __init__(self, id:int, title:str, location:str, period) -> None:
                self._sheet = festivalsSheet()
                
                self.idf = ModelIdentification('id', id)
                self.name = title
                self.location = location
                self.period = period

            def __str__(self) -> str:
                return str(self.name)

        cls.festivalssheet = festivalsSheet
        cls.festival = Festival


    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_can_read_festival(self):
        awaited = '2023-07-31 00:00:00'
        wacken = self.festivalssheet().find_model_by_id(1)
        self.assertEqual(awaited, str(wacken.period))
        self.assertIsInstance(wacken.period, datetime)

    def test_can_insert_new_festival(self):
        awaited_request = "INSERT INTO [festivals$] (id, title, location, period) VALUES (?, ?, ?, ?)"
        awaited_params = (5, 'tons of metal', 'Miami, US', datetime(2023, 6, 1, 0, 0))

        class festSheet_mocked(self.festivalssheet):
            FAKE_request = None
            FAKE_params = None

            def __str__(self) -> str:
                return '[festivals$]'

            def _run_db_modification(self, request:str, params:list):
                """Mocked
                Original method db modif by inserting new row, mocked method sets two FAKE attrs that can be checked
                """
                self.FAKE_request = request
                self.FAKE_params = tuple(params)

            def get_model(self, kvp:dict):
                return mocked_festival(**kvp)

        class mocked_festival(self.festival):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
                self._sheet = festSheet_mocked()
                
            def check_db_modification(self):
                return self._sheet.FAKE_request, self._sheet.FAKE_params

        TonsOfMetal = mocked_festival(None, 'tons of metal', 'Miami, US', '01/06/2023')
        TonsOfMetal.save()
        result_request, params = TonsOfMetal.check_db_modification()

        self.assertEqual(awaited_request, str(result_request))
        self.assertTupleEqual(awaited_params, params)

    def test_can_update_period(self):
        awaited_request = "UPDATE [festivals$] SET id = ?, title = ?, location = ?, period = ? WHERE id = ?"
        awaited_params = (5, 'tons of metal', 'Miami, US', datetime(2023, 9, 1, 0, 0), 5)

        class festSheet_mocked(self.festivalssheet):
            FAKE_request = None
            FAKE_params = None

            def __str__(self) -> str:
                return '[festivals$]'

            def _run_db_modification(self, request:str, params:list):
                """Mocked
                Original method db modif by inserting new row, mocked method sets two FAKE attrs that can be checked
                """
                self.FAKE_request = request
                self.FAKE_params = tuple(params)

            def get_model(self, kvp:dict):
                return mocked_festival(**kvp)

        class mocked_festival(self.festival):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
                self._sheet = festSheet_mocked()
                
            def check_db_modification(self):
                return self._sheet.FAKE_request, self._sheet.FAKE_params

        TonsOfMetal = mocked_festival(5, 'tons of metal', 'Miami, US', '01/06/2023')
        TonsOfMetal.period = '01/09/2023'
        TonsOfMetal.update()
        result_request, params = TonsOfMetal.check_db_modification()

        self.assertEqual(awaited_request, str(result_request))
        self.assertTupleEqual(awaited_params, params)        

    @unittest.skipIf(DENIED_DB_MODIFICATION, 'Mod of excel file is not allowed')
    def test_can_insert_TO_EXCEL_new_festival(self):
        TonsOfMetal = self.festival(None, 'tons of metal', 'Miami, US', '01/06/2023')
        TonsOfMetal.save()

    @unittest.skipIf(DENIED_DB_MODIFICATION, 'Mod of excel file is not allowed')
    def test_can_insert_TO_EXCEL_new_festival_with_datetime(self):
        TonsOfMetal = self.festival(None, 'tons of metal', 'Miami, US', '01/10/2023 16:30')
        TonsOfMetal.save()
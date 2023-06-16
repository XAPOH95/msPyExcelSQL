import unittest

from src.ExcelModel.model import ExcelModel, iSingleModel, iModelFabric, ModelIdentification

from src.ExcelSheet.excelcolumn import BasicColumn
from src.ExcelSheet.modelsheet import ModelSheet

class ModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        class FakeExcelColumnContainer:
            def __init__(self, idi:str, fk:str) -> None:
                self.idi = idi
                self.fk = fk

            def get_id_column(self):
                return self.idi

            def get_fk_column(self):
                return self.fk

        class FakeExcelController:
            musicians = [
                (1,   1,      "Michael Amott",        "guitar",   "back",     1), 
                (2,   1,      "Daniel Erlandsson",    "drums",    None,       1), 
                (3,   1,      "Sharlee D'Angelo",     "bass",     None,       1), 
                (4,   1,      "Alissa White-Gluz",    None,       "lead",     1), 
                (5,   1,      "Jeff Loomis",          "guitar",   "back",     1), 
                (6,   2,      "Tomas Lindberg",       None,       "lead",     1), 
                (7,   2,      "Adrian Erlandsson",    "drums",    None,       1), 
                (8,   2,      "Anders Bjorler",       "guitar",   None,       1), 
                (9,   2,      "Jonas Bjorler",        "bass",     None,       1), 
                (10,  2,      "Martin Larsson",       "guitar",   None,       1), 
                (11,  3,      "Kerry King",           "guitar",   None,       0), 
                (12,  3,      "Tom Araya",            "bass",     "lead",     0), 
                (13,  3,      "Paul Bostaph",         "drums",    None,       0), 
                (14,  3,      "Gary Holt",            "guitar",   None,       0), 
                (15,  4,      "Miland Mille Petrozza","guitar",  "lead",     1), 
                (16,  4,      "Jurgen Ventor Reil",   "drums",    None,       1), 
                (17,  4,      "Sami Yli-Sirnio",      "guitar",   "back",     1), 
                (18,  4,      "Frederic Leclercq",    "bass",     "back",     1), 
            ]

            bands = [
            (1, "arch enemy", "melodic death metal", "Halmstad, Sweden", 1995, 1),
            (2, "at the gates", "melodic death metal", "Gothenburg, Sweden", 1990, 1),
            (3, "slayer", "thrash metal", "Huntington Park, California, US", 1981, 0),
            (4, "kreator", "thrash metal", "Essen, Germany", 1982, 1)]

            def run(self, request:int):
                if request == 1:
                    return self.bands
                return self.musicians

        class ModelExcelSheet_mocked(ModelSheet):
            def __init__(self) -> None:
                pass
            ### general model interface implementation

            ### overwritten to test
            def find_model_by_id(self, index: int) -> ExcelModel:
                request = self._find(index - 1)
                response = request
                keys = self.model_keys
                kvp = {keys[i]:response[i] for i in range(len(response))}
                return self.get_model()(**kvp)                

            def _format_records(self, values:list):
                formatted_values = list()
                for i in range(len(self.fake_formats)):
                    if values[i] is None:
                        formatted_values.append(values[i])
                    else:
                        formatted_values.append(self.fake_formats[i](values[i]))
                return formatted_values

            def _delete(self, records):
                pass

            def delete_model(self, model: 'ExcelModel'):
                self._delete(int(model.get_id()))

        class musiciansSheet(ModelExcelSheet_mocked):
            _controller = FakeExcelController()
            model_keys = ("id", "band_id", "name",    "musical_instrument", "vocal", "status")
            fake_formats = (int, int, str, str, str, int)
            colcontainer = FakeExcelColumnContainer('id', 'band_id')

            ### columns in "excel database"
            _id = BasicColumn('id', int)
            band_id = BasicColumn('band_id', int)
            name = BasicColumn('name', str)
            musical_instrument = BasicColumn('musical_instrument', str)
            vocal = BasicColumn('vocal', str)
            status = BasicColumn('status', int)


            ### test_of_ExcelModel inheritance
            def find_model_by_id(self, index:int) -> ExcelModel:
                response = self._find(index - 1)
                keys = self.model_keys
                kvp = {keys[i]:response[i] for i in range(len(response))}
                return self.get_model(index -1)(**kvp)
            ### test_of_ExcelModel inheritance
            def get_model(self, index:int) -> 'ExcelModel':
                """For example, method can return different classes"""
                if index == 3:
                    return AlissaWhiteGluz
                return Musician

            ### model interface implementation
            def find_model_by_expression(self, columns: tuple, values: tuple):
                keys_index = self._find_keys_indexes(columns)
                response = self._find_by_expression(keys_index, values)
                keys = self.model_keys
                kvp = {keys[i]:response[i] for i in range(len(response))}
                return self.get_model(0)(**kvp)

            ### excelSheet commands
            def _find_keys_indexes(self, columns: tuple):
                keys = list()
                for column in columns:
                    for key in self.model_keys:
                        if column == key:
                            keys.append(self.model_keys.index(column))
                            break
                return keys

            def _find_by_expression(self, keys_index:tuple, values:tuple):
                match = len(keys_index)
                for record in self._controller.musicians:
                    counter = 0
                    for key in keys_index:
                        if record[key] in values:
                            counter += 1
                    if counter == match:
                        return record
                raise Exception('Record not found!')

            def _find(self, expression):
                return self._controller.run(0)[expression]

            def _insert(self, values:list):
                formatted_values = self._format_records(values)
                self._controller.run(0).append(tuple(formatted_values))

            def _update(self, values:list, index:int = None):
                index -= 1
                self._controller.run(0)[index] = self._format_records(values)           

            def records(self):
                return len(self._controller.run(0))

        class bandsSheet(ModelExcelSheet_mocked):
            _controller = FakeExcelController()
            model_keys = ("id", "band", "genre", "origin", "year_of_foundation", "status")
            fake_formats = (int, str, str, str, int, int)
            colcontainer = FakeExcelColumnContainer('id', '')

            ### columns in "excel database"
            _id = BasicColumn('id', int)
            band = BasicColumn('band', str)
            genre = BasicColumn('genre', str)
            origin = BasicColumn("origin", str)
            year = BasicColumn("year_of_foundation", int)
            status = BasicColumn("status", int)

            ### model interface implementation
            def get_model(self):
                return Band

            ### excelSheet commands
            def _find(self, expression):
                return self._controller.run(1)[expression]

            def _insert(self, values:tuple):
                formatted_values = list()
                for i in range(len(self.fake_formats)):
                    formatted_values.append(self.fake_formats[i](values[i]))
                self._controller.run(1).append(tuple(formatted_values))

            def _update(self, values:list, index:int = None):
                index -= 1
                self._controller.run(1)[index] = self._format_records(values)   

            def _delete(self, index:int):
                index -= 1
                del self._controller.run(1)[index]

            def records(self):
                return len(self._controller.run(1))

        class ExcelModel_mocked(ExcelModel):
            pass

        class Musician(ExcelModel_mocked):
            _alias = {'band':'band_id', 'instrument':'musical_instrument'}
            _sheet = musiciansSheet()

            def __init__(self, id:int, band_id:int, name:str, musical_instrument:str, vocal:str, status:bool) -> None:
                self.idi = ModelIdentification('id', id)
                self.band = bandsSheet().find_model_by_id(band_id)
                self.name = str(name)
                self.instrument = musical_instrument
                self.vocal = vocal
                self.status = bool(status)

            def __str__(self) -> str:
                return str(self.name)

            def introduce(self):
                phrase = f"I'm {self.name} from {str(self.band).capitalize()}!\n"
                vocal = f"I do {self.vocal} vocal\n" if self.vocal else ''
                instr = f'I play on {self.instrument}\n' if self.instrument else ''
                return phrase + vocal + instr

        class AlissaWhiteGluz(Musician):
            def rise_fist_in_air(self):
                print(self, "rises fist in air")

            def one_for_all(self):
                print(self, "says: 'one for all.... all for ONE!'")

            def yell_in_microphone(self):
                print(self, "yells: 'NE-ME-SIS'")

            def bang_hair(self):
                print(self, "shakes hair")

            def swing_hair(self):
                print(self, "swings hair")

            def rotate_hair(self):
                print(self, "rotates hair")

        class Band(ExcelModel_mocked):
            _alias = {'title':'band', 'year':'year_of_foundation'}
            _sheet = bandsSheet()

            def __init__(self, id:int, band:str, genre:str, origin:str, year_of_foundation:int, status:bool) -> None:
                self.idi = ModelIdentification('id', id)
                self.title = band
                self.genre = str(genre)
                self.origin = str(origin)
                self.year = year_of_foundation
                self.status = bool(status)

            def __str__(self) -> str:
                return str(self.title)

            def __repr__(self):
                return repr(self.title)

            def __int__(self):
                return self.idi.get_idf()

        cls.excelModel = ExcelModel_mocked
        cls.bandsExcelSheet = bandsSheet
        cls.band = Band
        cls.musician = Musician
        cls.musicianExcelSheet = musiciansSheet
        cls.controller = FakeExcelController


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


    def test_can_create_object_from_excel_sheet_record(self):
        awaited = (3, 'slayer', 'thrash metal', 'Huntington Park, California, US', 1981, 0)
        excel = self.bandsExcelSheet()
        band = excel.find_model_by_id(3)
        self.assertTupleEqual(awaited, tuple(dict(band).values()))

    def test_can_insert_model_to_book(self):
        awaited_megadeth = (5, 'megadeth', 'thrash metal', 'Los-Angeles, California, US', 1983, 1)
        awaited_metallica = (6, 'metallica', 'heavy metal', 'Los-Angeles, California, US', 1981, 1)
        awaited_anthrax = (7, 'anthrax', 'thrash metal', 'New York City, US', 1981, 1)

        excel = self.bandsExcelSheet()
        megadeth = self.band(0, "megadeth", "thrash metal", "Los-Angeles, California, US", 1983, 1)
        metallica = self.band(0, "metallica", "heavy metal", "Los-Angeles, California, US", 1981, 1)
        anthrax = self.band(0, "anthrax", "thrash metal", "New York City, US", 1981, 1)
        excel.insert_model(megadeth)        # we can ask excel to insert new model
        excel.insert_model(metallica)
        anthrax.save()                      # or we can ask model to save itself to excel file
        self.assertEqual(7, excel.records())

        tupled_megadeth = tuple(dict(excel.find_model_by_id(5)).values())
        tupled_metallica = tuple(dict(excel.find_model_by_id(6)).values())
        tupled_anthrax = tuple(dict(excel.find_model_by_id(7)).values())

        self.assertTupleEqual(awaited_megadeth, tupled_megadeth)
        self.assertTupleEqual(awaited_metallica, tupled_metallica)
        self.assertTupleEqual(awaited_anthrax, tupled_anthrax)

    def test_can_update_model_in_book(self):
        awaited = ('BFG Division', 'heavy metal', 'UAC, Mars', 2016, True)
        awaited_2 = ('BFG Division', 'argent metal', 'UAC, Mars', 2016, True)

        excel = self.bandsExcelSheet()
        BFG_division = self.band(None, "BFG Division", "heavy metal", "UAC, Mars", 2016, 1)
        BFG_division.save() # asking model to save itself to database
        bfg_one = tuple(dict(excel.find_model_by_id(int(BFG_division.get_id()))).values())

        self.assertTupleEqual(awaited, bfg_one[1:])

        BFG_division.genre = "argent metal" # assigning new genre for band
        BFG_division.update()               # asking band to update itself in database
        
        bfg_two = tuple(dict(excel.find_model_by_id(int(BFG_division.get_id()))).values())
        self.assertTupleEqual(awaited_2, bfg_two[1:])
        pass

    def test_can_init_musician_from_kvp(self):
        awaited_MickGordon = (None, 3, 'Mick Gordon', 'guitar', None, True)
        
        kvp = {"id":None, "band_id":3, "name":"Mick Gordon", "musical_instrument":"guitar","vocal":None,"status":True}
        MickGordon = self.musician(**kvp)
        tupled_MickGordon =  tuple(dict(MickGordon).values())
        self.assertTupleEqual(awaited_MickGordon, tupled_MickGordon)

    def test_can_init_musician(self):
        awaited_Alissa = (4, 1, 'Alissa White-Gluz', 'violin', 'lead', 1)
        awaited_Mick_Gordon = (19, 1, 'Mick Gordon', 'guitar', None, 1)

        excel = self.musicianExcelSheet()
        Alissa = excel.find_model_by_id(4)
        Mick_Gordon = self.musician(0, 1, 'Mick Gordon', 'guitar', None, True)
        excel.insert_model(Mick_Gordon)
        Alissa.instrument = 'violin'
        excel.update_model(Alissa)
        
        tupled_Alissa = [i for i in dict(excel.find_model_by_id(4)).values()]
        tupled_Mick_Gordon = [i for i in dict(excel.find_model_by_id(19)).values()]

        tupled_Alissa[-1] = int(tupled_Alissa[-1])

        self.assertTupleEqual(awaited_Alissa, tuple(tupled_Alissa))
        self.assertTupleEqual(awaited_Mick_Gordon, tuple(tupled_Mick_Gordon))

    def test_excelmodel_can_have_unique_behavior(self):
        Alissa = self.musicianExcelSheet().find_model_by_id(4)
        print()
        print(Alissa.introduce())
        Alissa.rise_fist_in_air()
        Alissa.one_for_all()
        Alissa.yell_in_microphone()
        Alissa.bang_hair()
        Alissa.swing_hair()
        Alissa.rotate_hair()
        print()

    def test_model_can_save_itself_to_db(self):
        awaited_Necrophagist = ('necrophagist', 'technical death metal', 'Gaggenau, Germany', 1992, False)
        awaited_MuhammedSuicmez = (5, 'Muhammed Suicmez', 'guitar', 'lead', False)
        awaited_StephanFimmers = (5, 'Stephan Fimmers', 'bass', None, False)
        awaited_SamiRaatikainen = (5, 'Sami Raatikainen', 'guitar', None, False)
        awaited_RomainGoulon = (5, 'Romain Goulon', 'drums', None, False)

        bands = self.bandsExcelSheet()
        musicians = self.musicianExcelSheet()

        Necrophagist = self.band(None, "necrophagist", "technical death metal", "Gaggenau, Germany", 1992, False)
        Necrophagist.save()
        id_of_Necrophagist = int(Necrophagist.get_id())
        
        MuhammedSuicmez = self.musician(0, id_of_Necrophagist, 'Muhammed Suicmez', "guitar", "lead", False)
        StephanFimmers = self.musician(0, id_of_Necrophagist, "Stephan Fimmers", "bass", None, False)
        SamiRaatikainen = self.musician(0, id_of_Necrophagist, "Sami Raatikainen", "guitar", None, False)
        RomainGoulon = self.musician(0, id_of_Necrophagist, "Romain Goulon", "drums", None, False)

        MuhammedSuicmez.save()
        StephanFimmers.save()
        SamiRaatikainen.save()
        RomainGoulon.save()

        Necrophagist_tupled = tuple(dict(Necrophagist).values())
        MuhammedSuicmez_tupled = tuple(dict(MuhammedSuicmez).values())
        StephanFimmers_tupled = tuple(dict(StephanFimmers).values())
        SamiRaatikainen_tupled = tuple(dict(SamiRaatikainen).values())
        RomainGoulon_tupled = tuple(dict(RomainGoulon).values())

        # have to slice id of band and musician
        # lazy to reinit FakeDB after each test
        self.assertTupleEqual(awaited_Necrophagist, Necrophagist_tupled[1:])
        self.assertTupleEqual(awaited_MuhammedSuicmez[1:], MuhammedSuicmez_tupled[2:])
        self.assertTupleEqual(awaited_StephanFimmers[1:], StephanFimmers_tupled[2:])
        self.assertTupleEqual(awaited_SamiRaatikainen[1:], SamiRaatikainen_tupled[2:])
        self.assertTupleEqual(awaited_RomainGoulon[1:], RomainGoulon_tupled[2:])

    @unittest.skip('unskip to delete check that its works')
    def test_model_can_delete_record(self):
        band = self.bandsExcelSheet().find_model_by_id(2)
        band.delete()
        
    def test_can_find_model_by_expression(self):
        awaited = (3, 'Tom Araya', 'bass', 'lead', False)
        band = 'slayer'
        TomAraya = self.musicianExcelSheet().find_model_by_expression(('musical_instrument', 'vocal'), ('bass', 'lead'))
        slayer = TomAraya.band
        self.assertTupleEqual(awaited, tuple(dict(TomAraya).values())[1:])
        self.assertEqual(band, str(slayer))
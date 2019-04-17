import sitchlib
import os

this_file_dirpath = os.path.dirname(os.path.abspath(__file__))
project_basepath = os.path.join(this_file_dirpath, "../../")
fixtures_path = os.path.join(this_file_dirpath, "../fixtures/")
csv_fixture_file = os.path.join(fixtures_path, "testdata.csv.gz")


class TestFccCsv:
    def fcc_csv_create(self):
        csv_obj = sitchlib.FccCsv(csv_fixture_file)
        return csv_obj

    def test_instantiate_fcc_csv(self):
        csv_obj = self.fcc_csv_create()
        assert csv_obj

    def test_get_fields(self):
        csv_obj = self.fcc_csv_create()
        assert len(csv_obj.fields) == 84

    def test_iterator(self):
        csv_obj = self.fcc_csv_create()
        i = 0
        for x in csv_obj:
            i = i + 1
        assert i == 20

    def test_fields_in_list(self):
        csv_obj = self.fcc_csv_create()
        assert isinstance(csv_obj.fields, list)

import sitchlib
import os

this_file_dirpath = os.path.dirname(os.path.abspath(__file__))
project_basepath = os.path.join(this_file_dirpath, "../../")
fixtures_path = os.path.join(this_file_dirpath, "../fixtures/")
csv_fixture_file = os.path.join(fixtures_path, "opencellid_test.csv.gz")


class TestFccCsv:
    def ocid_csv_create(self):
        csv_obj = sitchlib.OcidCsv(csv_fixture_file)
        return csv_obj

    def test_instantiate_fcc_csv(self):
        csv_obj = self.ocid_csv_create()
        assert csv_obj

    def test_iter_all(self):
        csv_obj = self.ocid_csv_create()
        for row in csv_obj:
            assert isinstance(row, dict)

    def test_mcc_list(self):
        csv_obj = self.ocid_csv_create()
        mcc_list = csv_obj.get_mcc_list()
        assert isinstance(mcc_list, list)

    def test_get_all_for_mcc(self):
        csv_obj = self.ocid_csv_create()
        mcc_list = csv_obj.get_mcc_list()
        print(mcc_list)
        all_for_mcc = csv_obj.get_all_for_mcc("GSM", mcc_list[0])
        assert isinstance(all_for_mcc, list)

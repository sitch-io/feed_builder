import sitchlib
import os

this_file_dirpath = os.path.dirname(os.path.abspath(__file__))
project_basepath = os.path.join(this_file_dirpath, "../../")
fixtures_path = os.path.join(this_file_dirpath, "../fixtures/")
csv_fixture_file = os.path.join(fixtures_path, "testdata.csv.gz")


class TestArfcnFromFeed:
    def fcc_csv_create(self):
        csv_obj = sitchlib.FccCsv(csv_fixture_file)
        return csv_obj

    def comparator_create(self):
        comparator = sitchlib.ArfcnComparator()
        return comparator

    def test_arfcn_for_downlink_range(self):
        csv = self.fcc_csv_create()
        comparator = self.comparator_create()
        for x in csv:
            f_min = x["FREQUENCY_ASSIGNED"]
            f_max = x["FREQUENCY_UPPER_BAND"]
            arfcn_list = comparator.arfcn_from_downlink_range(f_min, f_max)
            print(arfcn_list)
            assert isinstance(arfcn_list, list)

    def test_arfcn_for_uplink_range(self):
        csv = self.fcc_csv_create()
        comparator = self.comparator_create()
        for x in csv:
            f_min = x["FREQUENCY_ASSIGNED"]
            f_max = x["FREQUENCY_UPPER_BAND"]
            arfcn_list = comparator.arfcn_from_uplink_range(f_min, f_max)
            print(arfcn_list)
            assert isinstance(arfcn_list, list)

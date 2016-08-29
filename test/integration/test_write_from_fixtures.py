import imp
import os
from random import choice
from string import ascii_uppercase

run_id = (''.join(choice(ascii_uppercase) for i in range(8)))
temp_path = "/tmp/sitch_integration/%s" % run_id

modulename = 'sitchlib'
this_file_dirpath = os.path.dirname(os.path.abspath(__file__))
project_basepath = os.path.join(this_file_dirpath, "../../")
fixtures_path = os.path.join(this_file_dirpath, "../fixtures/")
file, pathname, description = imp.find_module(modulename, [project_basepath])
sitchlib = imp.load_module(modulename, file, pathname, description)

csv_fixture_file = os.path.join(fixtures_path, "testdata.csv.gz")


class TestWriteFromFixtures:
    def fcc_csv_create(self):
        csv_obj = sitchlib.FccCsv(csv_fixture_file)
        return csv_obj

    def comparator_create(self):
        comparator = sitchlib.ArfcnComparator()
        return comparator

    def outfile_handler_create(self, columns):
        of_handler = sitchlib.OutfileHandler(temp_path, columns)
        return of_handler

    def test_run_complete(self):
        csv = self.fcc_csv_create()
        comparator = self.comparator_create()
        columns = csv.fields
        of_handler = self.outfile_handler_create(columns)
        record_list = []
        print columns
        for row in csv:
            f_min = row["FREQUENCY_ASSIGNED"]
            f_max = row["FREQUENCY_UPPER_BAND"]
            state = row["LOC_STATE"]
            arfcns = comparator.arfcn_from_downlink_range(f_min, f_max)
            for arfcn in arfcns:
                record_id = "%s-%s" % (state, str(arfcn))
                if record_id not in record_list:
                    of_handler.start_feed_file(arfcn, row)
                else:
                    of_handler.append_feed_file(arfcn, row)

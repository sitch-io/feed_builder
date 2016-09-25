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

fcc_fields = ["LICENSE_ID", "SOURCE_SYSTEM", "CALLSIGN", "FACILITY_ID", "FRN",
              "LIC_NAME", "COMMON_NAME", "RADIO_SERVICE_CODE",
              "RADIO_SERVICE_DESC", "ROLLUP_CATEGORY_CODE",
              "ROLLUP_CATEGORY_DESC", "GRANT_DATE", "EXPIRED_DATE",
              "CANCELLATION_DATE", "LAST_ACTION_DATE", "LIC_STATUS_CODE",
              "LIC_STATUS_DESC", "ROLLUP_STATUS_CODE", "ROLLUP_STATUS_DESC",
              "ENTITY_TYPE_CODE", "ENTITY_TYPE_DESC", "ROLLUP_ENTITY_CODE",
              "ROLLUP_ENTITY_DESC", "LIC_ADDRESS", "LIC_CITY", "LIC_STATE",
              "LIC_ZIP_CODE", "CONTACT_COMPANY", "CONTACT_EMAIL",
              "MARKET_CODE", "MARKET_DESC", "CHANNEL_BLOCK", "LOC_TYPE_CODE",
              "LOC_TYPE_DESC", "LOC_CITY", "LOC_COUNTY_CODE",
              "LOC_COUNTY_NAME", "LOC_STATE", "LOC_RADIUS_OP", "LOC_SEQ_ID",
              "LOC_LAT_DEG", "LOC_LAT_MIN", "LOC_LAT_SEC", "LOC_LAT_DIR",
              "LOC_LONG_DEG", "LOC_LONG_MIN", "LOC_LONG_SEC", "LOC_LONG_DIR",
              "HGT_STRUCTURE", "ASR_NUM", "ANTENNA_ID", "ANT_SEQ_ID",
              "ANT_MAKE", "ANT_MODEL", "ANT_TYPE_CODE", "ANT_TYPE_DESC",
              "AZIMUTH", "BEAMWIDTH", "POLARIZATION_CODE", "FREQUENCY_ID",
              "FREQ_SEQ_ID", "FREQ_CLASS_STATION_CODE",
              "FREQ_CLASS_STATION_DESC", "POWER_ERP", "POWER_OUTPUT",
              "FREQUENCY_ASSIGNED", "FREQUENCY_UPPER_BAND", "UNIT_OF_MEASURE",
              "GROUND_ELEVATION", "ARFCN"]

ocid_fields = ["radio", "mcc", "net", "area", "cell", "unit", "lon",
               "lat", "range", "samples", "changeable", "created",
               "updated", "averageSignal", "carrier"]


class TestWriteFromFixtures:
    def fcc_csv_create(self):
        csv_obj = sitchlib.FccCsv(csv_fixture_file)
        return csv_obj

    def comparator_create(self):
        comparator = sitchlib.ArfcnComparator()
        return comparator

    def outfile_handler_create(self):
        of_handler = sitchlib.OutfileHandler(temp_path, fcc_fields,
                                             ocid_fields)
        return of_handler

    def test_run_complete(self):
        csv = self.fcc_csv_create()
        comparator = self.comparator_create()
        of_handler = self.outfile_handler_create()
        for gross_row in csv:
            f_min = gross_row["FREQUENCY_ASSIGNED"]
            f_max = gross_row["FREQUENCY_UPPER_BAND"]
            arfcns = comparator.arfcn_from_downlink_range(f_min, f_max)
            net_row = {}
            for column in fcc_fields:
                try:
                    net_row[column] = gross_row[column]
                except KeyError:
                    pass
            for arfcn in arfcns:
                net_row["ARFCN"] = arfcn
                of_handler.write_fcc_record(net_row)

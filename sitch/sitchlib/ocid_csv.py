import csv
import gzip


class OcidCsv(object):
    """ This wraps the OpenCellID CSV dataset. """
    def __init__(self, data_bundle):
        self.data_bundle = data_bundle

    def __iter__(self):
        with gzip.open(self.data_bundle, 'r') as bolus:
            consumer = csv.DictReader(bolus)
            for row in consumer:
                yield row

    def get_mcc_list(self):
        mcc_list = []
        with gzip.open(self.data_bundle, 'r') as bolus:
            consumer = csv.DictReader(bolus)
            for row in consumer:
                if row["mcc"] not in mcc_list:
                    mcc_list.append(row["mcc"])
        return mcc_list

    def get_all_for_mcc(self, radio, mcc):
        results = []
        with gzip.open(self.data_bundle, 'r') as bolus:
            consumer = csv.DictReader(bolus)
            for row in consumer:
                if (row["mcc"] == mcc and row["radio"] == radio):
                    results.append(row)
        return results

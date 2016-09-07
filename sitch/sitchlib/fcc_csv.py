import csv
import gzip


class FccCsv(object):
    """ This object wraps the FCC license CSV dataset.
    Currently, we're only looking for CL type licenses."""
    def __init__(self, csv_gzfile):
        self.csv_gzfile = csv_gzfile
        self.fields = self.get_fields()
        self.radio_service_code = "CL"

    def __iter__(self):
        with gzip.open(self.csv_gzfile) as gz_feed:
            feed = csv.DictReader(gz_feed, fieldnames=self.fields)
            for row in feed:
                if row["RADIO_SERVICE_CODE"] == self.radio_service_code:
                    yield row

    def get_fields(self):
        with gzip.open(self.csv_gzfile) as gz_feed:
            topline = gz_feed.readline()
            fields = self.get_fields_from_topline(topline)
            return fields

    def get_fields_from_topline(self, topline):
        cleaned_up = topline.replace('#', '', 1).replace('\n', '')
        fields = cleaned_up.split(',')
        return fields

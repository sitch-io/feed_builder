import gzip
import os
import requests
from zipfile import ZipFile


class FeedCollector(object):
    """This class handles obtaining the feed files from OpenCellID and the FCC.

    Only one argument, and that's an object that contains the runtime
    configuration.  See sitchlib.ConfigHelper for details.

    """

    def __init__(self, config):
        self.ocid_key = config.ocid_key
        self.ocid_feed_prefix = "http://opencellid.org/downloads/?"
        self.ocid_feed_file = "cell_towers.csv.gz"
        self.ocid_url = "%sapiKey=%s&filename=%s" % (self.ocid_feed_prefix,
                                                     self.ocid_key,
                                                     self.ocid_feed_file)
        self.ocid_outfile = config.ocid_destination_file
        self.fcc_feed_base = "http://data.fcc.gov/download/license-view/"
        self.fcc_feed_file = "fcc-license-view-data-csv-format.zip"
        self.fcc_url = "%s%s" % (self.fcc_feed_base, self.fcc_feed_file)
        self.fcc_outfile = config.fcc_destination_file
        self.fcc_tempfile = "%s%s" % (self.fcc_outfile, "tempfile")

    def write_ocid_feed_file(self):
        """ Calling this method will cause the retrieval of the
        OpenCellID data feed. """
        payload = {"key": self.ocid_key}
        response = requests.post(self.ocid_url, data=payload, stream=True)
        print "Getting OCID feed file.  This will take a while..."
        with open(self.ocid_outfile, 'wb') as feed_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    feed_file.write(chunk)
        print "OCID feed file written to %s" % self.ocid_outfile

    def write_fcc_feed_file(self):
        """ Calling this method will result in the retrieval of the
        FCC license database.

        """

        response = requests.get(self.fcc_url, stream=True)
        print "Downloading FCC license database.  This will take a while."
        with open(self.fcc_tempfile, 'wb') as feed_temp_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    feed_temp_file.write(chunk)
        print "Converting FCC license from zip to gzip"
        with ZipFile.open(self.fcc_tempfile, 'wb') as src_file:
            with gzip.open(self.fcc_outfile, 'wb') as dest_file:
                dest_file.write(src_file.read())
        os.remove(self.fcc_tempfile)
        print "FCC license database written to %s" % self.fcc_outfile

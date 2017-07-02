import gzip
import os
import requests
import shutil
from zipfile import ZipFile


class FeedConsumer(object):
    """This class handles obtaining the feed files from OpenCellID and the FCC.

    Only one argument, and that's an object that contains the runtime
    configuration.  See sitchlib.ConfigHelper for details.

    """

    def __init__(self, config):
        self.fcc_feed_base = "http://data.fcc.gov/download/license-view/"
        self.fcc_feed_file = "fcc-license-view-data-csv-format.zip"
        self.fcc_url = "%s%s" % (self.fcc_feed_base, self.fcc_feed_file)
        self.fcc_outfile = config.fcc_destination_file
        self.fcc_tempfile = "%s%s" % (self.fcc_outfile, "tempfile")
        self.fcc_enclosed_file = config.fcc_enclosed_file
        self.chunk_size = None

    def write_fcc_feed_file(self):
        """ Calling this method will result in the retrieval of the
        FCC license database. """
        response = requests.get(self.fcc_url, stream=True)
        print "Downloading FCC license database.  This will take a while."
        with open(self.fcc_tempfile, 'wb') as feed_temp_file:
            # status = 0
            for chunk in response.iter_content(chunk_size=self.chunk_size):
                if chunk:
                    # status += self.chunk_size
                    # print("Downloaded %s for FCC Feed" % str(status))
                    feed_temp_file.write(chunk)
        print "Converting FCC license from zip to gzip"
        with ZipFile(self.fcc_tempfile, 'r') as src_file:
            src_file.extract(self.fcc_enclosed_file, "/var/")
        print("Extracted contents from zip...")
        os.remove(self.fcc_tempfile)
        raw_fcc_file = "/var/%s" % self.fcc_enclosed_file
        with open(raw_fcc_file, 'rb') as file_in:
            with gzip.open(self.fcc_outfile, 'wb') as dest_file:
                shutil.copyfileobj(file_in, dest_file)
        os.remove(raw_fcc_file)
        print "FCC license database written to %s" % self.fcc_outfile

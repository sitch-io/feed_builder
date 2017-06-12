import gzip
import os
import re
import requests
import shutil
from zipfile import ZipFile


class FeedConsumer(object):
    """This class handles obtaining the feed files from OpenCellID and the FCC.

    Only one argument, and that's an object that contains the runtime
    configuration.  See sitchlib.ConfigHelper for details.

    """

    def __init__(self, config):
        # self.ocid_key = config.ocid_key
        # self.ocid_feed_prefix = "http://opencellid.org/downloads/?"
        # self.ocid_feed_prefix = "https://download.unwiredlabs.com/ocid/downloads/?"  # NOQA
        # self.ocid_feed_file = "cell_towers.csv.gz"
        self.ocid_url = self.pick_ocid_url_from_list(
                            self.get_ocid_urls_from_mls_page())
        # self.ocid_url = "%stoken=%s&file=%s" % (self.ocid_feed_prefix,
        #                                        self.ocid_key,
        #                                        self.ocid_feed_file)
        # self.ocid_url = "%sapiKey=%s&filename=%s" % (self.ocid_feed_prefix,
        #                                             self.ocid_key,
        #                                              self.ocid_feed_file)
        self.ocid_outfile = config.ocid_destination_file
        self.fcc_feed_base = "http://data.fcc.gov/download/license-view/"
        self.fcc_feed_file = "fcc-license-view-data-csv-format.zip"
        self.fcc_url = "%s%s" % (self.fcc_feed_base, self.fcc_feed_file)
        self.fcc_outfile = config.fcc_destination_file
        self.fcc_tempfile = "%s%s" % (self.fcc_outfile, "tempfile")
        self.fcc_enclosed_file = config.fcc_enclosed_file
        # self.chunk_size = 104857600  # 100MB
        self.chunk_size = None

    @classmethod
    def get_ocid_urls_from_mls_page(cls):
        """Extracts OCID urls from MLS downloads page"""
        mls_downloads_page = "https://location.services.mozilla.com/downloads"
        dl_page_contents = requests.get(mls_downloads_page).text
        targets = []
        rxmatch = r'https://[A-Za-z0-9]+\.cloudfront\.net/export/MLS-full-cell-export-\d{4}-\d{2}-\d{2}T\d+\.csv.gz'  # NOQA
        for line in dl_page_contents.splitlines():
            matches = re.findall(rxmatch, line)
            if matches:
                targets.extend(matches)
        return targets

    @classmethod
    def pick_ocid_url_from_list(cls, url_list):
        """Gets the link to the most recent MLS download"""
        date_struct = {}
        date_list = []
        for url in url_list:
            d = re.findall(r'\d{4}-\d{2}-\d{2}T\d+', url)[0]
            date_struct[d] = url
            date_list.append(d)
        target = sorted(date_list)[-1]
        return date_struct[target]

    def write_ocid_feed_file(self):
        """ Calling this method will cause the retrieval of the
        OpenCellID data feed. """
        # payload = {"key": self.ocid_key}
        # response = requests.post(self.ocid_url, data=payload, stream=True)
        response = requests.get(self.ocid_url, stream=True)
        print "Getting OCID feed file.  This will take a while..."
        with open(self.ocid_outfile, 'wb') as feed_file:
            # status = 0
            for chunk in response.iter_content(chunk_size=self.chunk_size):
                if chunk:
                    # status += self.chunk_size
                    # print("Downloaded %s for OpenCellID" % str(status))
                    feed_file.write(chunk)
        print "OCID feed file written to %s" % self.ocid_outfile

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

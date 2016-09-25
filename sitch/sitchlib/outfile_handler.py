import csv
import os
import time


class OutfileHandler(object):
    def __init__(self, base_path, fcc_columns, ocid_columns):
        self.base_path = base_path
        self.ensure_path_exists(self.base_path)
        self.fcc_columns = fcc_columns
        self.ocid_columns = ocid_columns
        self.feed_files = []

    def write_fcc_record(self, data):
        dir_name = self.base_path
        state = data["LOC_STATE"]
        file_name = "%s.csv" % state
        file_path = os.path.join(dir_name, file_name)
        if file_path in self.feed_files:
            self.append_feed_file(file_path, self.fcc_columns, data)
        else:
            self.start_feed_file(file_path, self.fcc_columns, data)
            self.feed_files.append(file_path)

    def write_ocid_record(self, data):
        dir_name = self.base_path
        mcc = data["mcc"]
        file_name = "%s.csv" % mcc
        file_path = os.path.join(dir_name, file_name)
        if file_path in self.feed_files:
            self.append_feed_file(file_path, self.ocid_columns, data)
        else:
            self.start_feed_file(file_path, self.ocid_columns, data)
            self.feed_files.append(file_path)

    def start_feed_file(self, file_path, columns, data):
        print "Starting a new feed file: %s" % file_path
        with open(file_path, 'w') as outfile:
            producer = csv.DictWriter(outfile, fieldnames=columns)
            producer.writeheader()
            producer.writerow(data)
        return

    def append_feed_file(self, file_path, columns, data):
        with open(file_path, 'a') as outfile:
            producer = csv.DictWriter(outfile, fieldnames=columns)
            try:
                producer.writerow(data)
            except ValueError as e:
                print "ValueError!"
                print repr(e)
                print str(data)
        return

    @classmethod
    def ensure_path_exists(cls, dirpath):
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
            time.sleep(1)

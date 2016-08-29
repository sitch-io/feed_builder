import csv
import os
import time


class OutfileHandler(object):
    def __init__(self, base_path, columns):
        self.base_path = base_path
        self.ensure_path_exists(self.base_path)
        self.columns = columns

    def start_feed_file(self, arfcn, data):
        dir_name = self.base_path
        file_name = "%s-%s.csv" % (data["LOC_STATE"], arfcn)
        file_path = os.path.join(dir_name, file_name)
        self.ensure_path_exists(dir_name)
        print "Starting a new feed file: %s" % file_name
        with open(file_path, 'w') as outfile:
            producer = csv.DictWriter(outfile, fieldnames=self.columns)
            producer.writeheader()
            producer.writerow(data)
        return file_name

    def append_feed_file(self, state, arfcn, data):
        dir_name = self.base_path
        file_name = "%s-%s.csv" % (state, arfcn)
        file_path = os.path.join(dir_name, file_name)
        self.ensure_path_exists(dir_name)
        with open(file_path, 'a') as outfile:
            producer = csv.DictWriter(outfile, fieldnames=self.columns)
            try:
                producer.writerow(data)
            except ValueError as e:
                print "ValueError!"
                print repr(e)
                print str(data)
        return file_name

    @classmethod
    def ensure_path_exists(cls, dirpath):
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
            time.sleep(1)

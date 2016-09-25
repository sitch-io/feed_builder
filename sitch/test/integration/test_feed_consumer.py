import imp
import os

modulename = 'sitchlib'
this_file_dirpath = os.path.dirname(os.path.abspath(__file__))
project_basepath = os.path.join(this_file_dirpath, "../../")
fixtures_path = os.path.join(this_file_dirpath, "../fixtures/")
file, pathname, description = imp.find_module(modulename, [project_basepath])
sitchlib = imp.load_module(modulename, file, pathname, description)
csv_fixture_file = os.path.join(fixtures_path, "testdata.csv.gz")


class TestFeedConsumer:
    def create_config_object(self):
        os.environ['OCID_KEY'] = '123456'
        os.environ['TWILIO_SID'] = 'asdf3456'
        os.environ['TWILIO_TOKEN'] = 'asdflnasgin'
        config_obj = sitchlib.ConfigHelper()
        return config_obj

    def test_instantiate_feed_consumer_object(self):
        config_obj = self.create_config_object()
        feed_consumer = sitchlib.FeedConsumer(config_obj)
        assert feed_consumer

import pytest
import sitchlib
import os

this_file_dirpath = os.path.dirname(os.path.abspath(__file__))
project_basepath = os.path.join(this_file_dirpath, "../../")
fixtures_path = os.path.join(this_file_dirpath, "../fixtures/")
csv_fixture_file = os.path.join(fixtures_path, "testdata.csv.gz")


class TestIntegrationConfigHelper:
    def test_create_config_object(self):
        os.environ['OCID_KEY'] = '123456'
        os.environ['TWILIO_SID'] = 'asdf3456'
        os.environ['TWILIO_TOKEN'] = 'asdflnasgin'
        config_obj = sitchlib.ConfigHelper()
        assert config_obj.ocid_key == '123456'
        assert config_obj.twilio_sid == 'asdf3456'
        assert config_obj.twilio_token == 'asdflnasgin'

    def test_get_from_env_fail(self):
        with pytest.raises(KeyError) as excinfo:
            sitchlib.ConfigHelper.get_from_env('nonexist')
        assert excinfo

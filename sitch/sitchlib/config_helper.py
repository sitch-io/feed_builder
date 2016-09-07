import os


class ConfigHelper:
    def __init__(self):
        self.aws_key = ConfigHelper.get_from_env("AWS_KEY")
        self.aws_secret = ConfigHelper.get_from_env("AWS_SECRET")
        self.ocid_key = ConfigHelper.get_from_env("OCID_KEY")
        self.bucket_name = ConfigHelper.get_from_env("BUCKET_NAME")
        self.base_path = ConfigHelper.get_from_env("BASE_PATH")
        self.iso_country = ConfigHelper.get_from_env("ISO_COUNTRY")
        self.twilio_sid = ConfigHelper.get_from_env("TWILIO_SID")
        self.twilio_token = ConfigHelper.get_from_env("TWILIO_TOKEN")
        self.ocid_destination_file = "/tmp/ocid.csv.gz"
        self.fcc_tempfile = "/tmp/fcc.tmp.zip"
        self.fcc_destination_file = "/tmp/fcc.csv.gz"
        self.target_radio = "GSM"
        return

    @classmethod
    def get_from_env(cls, k):
        retval = os.getenv(k)
        if retval is None:
            print "Required config variable not set: %s" % k
            # print "Unable to continue.  Exiting."
            # sys.exit(2)
        return retval

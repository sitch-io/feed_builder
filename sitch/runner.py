#!/usr/bin/python
import datetime
import gzip
import os
import psutil
import sitchlib
import shutil
import threading
import time

""" Outputs files like state.csv.gz.  These contain CSV data from the
FCC license database.  Use for determining GPS distance from tower.  Also
useful for correlating ARFCN/MCC/MNC for sanity and correct BTS ownership and
licensing representation."""

fcc_fields = ["LICENSE_ID", "SOURCE_SYSTEM", "CALLSIGN", "FACILITY_ID", "FRN",
              "LIC_NAME", "COMMON_NAME", "RADIO_SERVICE_CODE",
              "RADIO_SERVICE_DESC", "ROLLUP_CATEGORY_CODE",
              "ROLLUP_CATEGORY_DESC", "GRANT_DATE", "EXPIRED_DATE",
              "CANCELLATION_DATE", "LAST_ACTION_DATE", "LIC_STATUS_CODE",
              "LIC_STATUS_DESC", "ROLLUP_STATUS_CODE", "ROLLUP_STATUS_DESC",
              "ENTITY_TYPE_CODE", "ENTITY_TYPE_DESC", "ROLLUP_ENTITY_CODE",
              "ROLLUP_ENTITY_DESC", "LIC_ADDRESS", "LIC_CITY", "LIC_STATE",
              "LIC_ZIP_CODE", "CONTACT_COMPANY", "CONTACT_EMAIL",
              "MARKET_CODE", "MARKET_DESC", "CHANNEL_BLOCK", "LOC_TYPE_CODE",
              "LOC_TYPE_DESC", "LOC_CITY", "LOC_COUNTY_CODE",
              "LOC_COUNTY_NAME", "LOC_STATE", "LOC_RADIUS_OP", "LOC_SEQ_ID",
              "LOC_LAT_DEG", "LOC_LAT_MIN", "LOC_LAT_SEC", "LOC_LAT_DIR",
              "LOC_LONG_DEG", "LOC_LONG_MIN", "LOC_LONG_SEC", "LOC_LONG_DIR",
              "HGT_STRUCTURE", "ASR_NUM", "ANTENNA_ID", "ANT_SEQ_ID",
              "ANT_MAKE", "ANT_MODEL", "ANT_TYPE_CODE", "ANT_TYPE_DESC",
              "AZIMUTH", "BEAMWIDTH", "POLARIZATION_CODE", "FREQUENCY_ID",
              "FREQ_SEQ_ID", "FREQ_CLASS_STATION_CODE",
              "FREQ_CLASS_STATION_DESC", "POWER_ERP", "POWER_OUTPUT",
              "FREQUENCY_ASSIGNED", "FREQUENCY_UPPER_BAND", "UNIT_OF_MEASURE",
              "GROUND_ELEVATION", "ARFCN"]

ocid_fields = ["radio", "mcc", "net", "area", "cell", "unit", "lon",
               "lat", "range", "samples", "changeable", "created",
               "updated", "averageSignal", "carrier"]

feed_directory = "/var/production/"  # This is where the finished feed goes


def compress_and_remove_original(infiles):
    for uncompressed in infiles:
        infile = uncompressed
        outfile = "%s.gz" % infile
        with open(infile, 'rb') as f_in, gzip.open(outfile, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        print "Written: %s" % outfile
        os.remove(infile)
        print "Removed: %s" % infile


def get_now_string():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return now


def write_statusfile(file_path):
    datestring = get_now_string()
    str_1 = "# SITCH Sensor Feed"
    str_2 = "## Processed: %s" % datestring
    str_3 = "Derived from:"
    str_4 = "* The OpenCellID DB http://opencellid.org\n  * CGI DB\n  * CC by SA 3.0 https://creativecommons.org/licenses/by-sa/3.0/"  # NOQA
    str_5 = "* The FCC License DB http://data.fcc.gov\n  * ARFCN DB"
    str_6 = "* Twilio's API: https://twilio.com\n  * CGI to provider correlation"  # NOQA
    master_str = "\n".join([str_1, str_2, str_3, str_4, str_5, str_6])
    with open(file_path, 'w') as out_file:
        out_file.write(master_str)
    return


def travis_its_going_to_be_ok():
    sleep_val = 120
    sleep_total = 0
    while True:
        print("Still running...%s/3000 until job timeout!" % sleep_total)
        vmem = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        cpu = psutil.cpu_times().user
        iowait = psutil.cpu_times().iowait
        print("Memory: %s\tDisk: %s\tUser: %s\tIO Wait: %s" % (vmem, disk,
                                                               cpu, iowait))
        sleep_total += sleep_val
        time.sleep(sleep_val)
    return


def main():
    travis_placation = threading.Thread(target=travis_its_going_to_be_ok,
                                        name="needy_travis")
    travis_placation.daemon = True
    travis_placation.start()
    sitchlib.OutfileHandler.ensure_path_exists(feed_directory)
    arfcn_comparator = sitchlib.ArfcnComparator()
    config = sitchlib.ConfigHelper()
    feed_manager = sitchlib.FeedConsumer(config)
    fileout = sitchlib.OutfileHandler(config.base_path,
                                      fcc_fields, ocid_fields)
    # Getting carrier reference from Twilio
    twilio_c = sitchlib.TwilioCarriers(config.twilio_sid,
                                       config.twilio_token)
    mcc_mnc_carriers = twilio_c.get_providers_for_country(config.iso_country)
    carrier_enricher = sitchlib.CarrierEnricher(mcc_mnc_carriers)
    print "Downloading FCC license information"
    feed_manager.write_fcc_feed_file()
    fcc_feed_obj = sitchlib.FccCsv(config.fcc_destination_file)
    print "Splitting FCC license file into feed files..."
    for row in fcc_feed_obj:
        f_min = row["FREQUENCY_ASSIGNED"]
        f_max = row["FREQUENCY_UPPER_BAND"]
        arfcns = arfcn_comparator.arfcn_from_downlink_range(f_min, f_max)
        net_row = {}
        for column in fcc_fields:
            try:
                net_row[column] = row[column]
            except KeyError:
                pass
        for arfcn in arfcns:
            net_row["ARFCN"] = arfcn
            fileout.write_fcc_record(net_row)
    print "Compressing FCC feed files"
    compress_and_remove_original(fileout.feed_files)
    fileout = None
    fileout = sitchlib.OutfileHandler(config.base_path,
                                      fcc_fields, ocid_fields)
    print "Downloading feed from OpenCellID"
    feed_manager.write_ocid_feed_file()
    ocid_feed_obj = sitchlib.OcidCsv(config.ocid_destination_file)
    print "Splitting OpenCellID feed into MCC files..."
    for row in ocid_feed_obj:
        if row["radio"] != config.target_radio:
            continue
        row["carrier"] = carrier_enricher.get_carrier(row["mcc"], row["net"])
        fileout.write_ocid_record(row)
    print "Compressing OpenCellID feed files"
    compress_and_remove_original(fileout.feed_files)
    print "Moving to drop directory..."
    staged_files = os.listdir(config.base_path)
    for staged_file in staged_files:
        full_src_file_name = os.path.join(config.base_path, staged_file)
        full_dst_file_name = os.path.join(feed_directory, staged_file)
        if (os.path.isfile(full_src_file_name)):
            shutil.copy(full_src_file_name, full_dst_file_name)
    write_statusfile(os.path.join(config.base_path, "README.md"))
    travis_placation.stop()
    print "ALL DONE!!!"

if __name__ == "__main__":
    main()

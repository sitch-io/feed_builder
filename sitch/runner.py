#!/usr/bin/python
"""Create SITCH feed files."""
import datetime
import gzip
import os
import shutil

from dateutil.parser import parse as dt_parse

import sitchlib


""" Outputs files like state.csv.gz.  These contain CSV data from the
FCC license database.  Use for determining GPS distance from tower.  Also
useful for correlating ARFCN/MCC/MNC for sanity and correct BTS ownership and
licensing representation."""

FCC_FIELDS = ["LICENSE_ID", "SOURCE_SYSTEM", "CALLSIGN", "FACILITY_ID", "FRN",
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

OCID_FIELDS = ["radio", "mcc", "net", "area", "cell", "unit", "lon",
               "lat", "range", "samples", "changeable", "created",
               "updated", "averageSignal", "carrier"]

FEED_DIRECTORY = "/var/production/"  # This is where the finished feed goes


def compress_and_remove_original(infiles):
    """Compress files, remove originals."""
    for uncompressed in list(infiles):
        infile = uncompressed
        outfile = "{}.gz".format(infile)
        with open(infile, 'rb') as f_in, gzip.open(outfile, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        print("Written: {}".format(outfile))
        os.remove(infile)
        print("Removed: {}".format(infile))


def get_now_string():
    """Get ISO string for NOW."""
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return now


def write_statusfile(file_path, fcc_date, ocid_date):
    """Write status to file."""
    datestring = get_now_string()
    body = []
    body.append("# SITCH Sensor Feed\n")
    body.append("## Processed: {}\n".format(datestring))
    body.append("Derived from:\n")
    body.append("* The OpenCellID DB http://opencellid.org")
    body.append("  * Newest record: {}".format(epoch_to_iso8601(ocid_date)))
    body.append("  * CGI DB")
    body.append("  * CC by SA 3.0 https://creativecommons.org/licenses/by-sa/3.0/")  # NOQA
    body.append("* The FCC License DB http://data.fcc.gov")
    body.append("  * Newest record: {}".format(epoch_to_iso8601(fcc_date)))
    body.append("  * ARFCN DB")
    body.append("* Twilio's API: https://twilio.com")
    body.append("  * CGI to provider correlation")
    master_str = "\n".join(body)
    with open(file_path, 'w') as out_file:
        out_file.write(master_str)


def epoch_to_iso8601(unix_time):
    """Transform epoch time to ISO8601 format."""
    cleaned = float(unix_time)
    return datetime.datetime.utcfromtimestamp(cleaned).isoformat()


def iso8601_to_epoch(iso_time):
    """Transform iso time into a unix timestamp."""
    return int((dt_parse(iso_time) -
                datetime.datetime(1970, 1, 1)).total_seconds())


def process_fcc_feed(base_path, fcc_destination_file):
    """Process FCC feed, return newest record timestamp."""
    fcc_feed_obj = sitchlib.FccCsv(fcc_destination_file)
    arfcn_comparator = sitchlib.ArfcnComparator()
    fileout = sitchlib.OutfileHandler(base_path, FCC_FIELDS, OCID_FIELDS)
    newest_fcc_record = 0
    print("Splitting FCC license file into feed files...")
    for row in fcc_feed_obj:
        f_min = row["FREQUENCY_ASSIGNED"]
        f_max = row["FREQUENCY_UPPER_BAND"]
        arfcns = arfcn_comparator.arfcn_from_downlink_range(f_min, f_max)
        net_row = {}
        for column in FCC_FIELDS:
            try:
                net_row[column] = row[column]
            except KeyError:
                pass
        for arfcn in arfcns:
            net_row["ARFCN"] = arfcn
            fileout.write_fcc_record(net_row)
        if iso8601_to_epoch(row["LAST_ACTION_DATE"]) > newest_fcc_record:
            newest_fcc_record = iso8601_to_epoch(row["LAST_ACTION_DATE"])
    print("Compressing FCC feed files")
    compress_and_remove_original(fileout.feed_files)
    return newest_fcc_record


def main():
    """Wrap all top-level logic."""
    sitchlib.OutfileHandler.ensure_path_exists(FEED_DIRECTORY)
    config = sitchlib.ConfigHelper()
    twilio_c = sitchlib.TwilioCarriers(config.twilio_sid,
                                       config.twilio_token)
    mcc_mnc_carriers = twilio_c.get_providers_for_country(config.iso_country)
    carrier_enricher = sitchlib.CarrierEnricher(mcc_mnc_carriers)
    newest_ocid_record = 0
    print("Splitting FCC license file into feed files...")
    newest_fcc_record = process_fcc_feed(config.base_path,
                                         config.fcc_destination_file)
    fileout = sitchlib.OutfileHandler(config.base_path,
                                      FCC_FIELDS, OCID_FIELDS)
    print("Setup OpenCellID feed from {}".format(config.ocid_destination_file))
    ocid_feed_obj = sitchlib.OcidCsv(config.ocid_destination_file)
    print("Splitting OpenCellID feed into MCC files...")
    for row in ocid_feed_obj:
        if row["radio"] != config.target_radio:
            continue
        row["carrier"] = carrier_enricher.get_carrier(row["mcc"], row["net"])
        if int(row["updated"]) > int(newest_ocid_record):
            newest_ocid_record = int(row["updated"])
        fileout.write_ocid_record(row)
    print("Compressing OpenCellID feed files")
    compress_and_remove_original(fileout.feed_files)
    print("Moving to drop directory...")
    staged_files = os.listdir(config.base_path)
    for staged_file in staged_files:
        full_src_file_name = os.path.join(config.base_path, staged_file)
        full_dst_file_name = os.path.join(FEED_DIRECTORY, staged_file)
        if os.path.isfile(full_src_file_name):
            shutil.copy(full_src_file_name, full_dst_file_name)
    write_statusfile("/opt/README.md", newest_fcc_record, newest_ocid_record)
    print("ALL DONE!!!")


if __name__ == "__main__":
    main()

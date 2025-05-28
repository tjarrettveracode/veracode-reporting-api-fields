import time
import sys
import argparse
import logging
import json
import datetime

import anticrlf
from veracode_api_py import Analytics, Applications, APICredentials

log = logging.getLogger(__name__)

def setup_logger():
    handler = logging.FileHandler('reportingapi_fields.log', encoding='utf8')
    handler.setFormatter(anticrlf.LogFormatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'))
    logging.basicConfig(level=logging.INFO, handlers=[handler])

def creds_expire_days_warning():
    creds = APICredentials().get_self()
    exp = datetime.datetime.strptime(creds['expiration_ts'], "%Y-%m-%dT%H:%M:%S.%f%z")
    delta = exp - datetime.datetime.now().astimezone() #we get a datetime with timezone...
    if (delta.days < 7):
        print('These API credentials expire ', creds['expiration_ts'])

def generate_report(start_time: datetime, end_time: datetime = None):

    wait_seconds = 15

    print('Retrieving findings report...')
    theguid = Analytics().create_report(report_type='findings',last_updated_start_date=start_time, last_updated_end_date=end_time)

    print('Checking status for report {}...'.format(theguid))
    thestatus,thefindings=Analytics().get(theguid)

    while thestatus != 'COMPLETED':
        print('Waiting {} seconds before we try again...'.format(wait_seconds))
        time.sleep(wait_seconds)
        print('Checking status for report {}...'.format(theguid))
        thestatus,thefindings=Analytics().get(theguid)

    recordcount = len(thefindings)

    print('Retrieved {} findings'.format(recordcount))

    return thefindings

def enrich_findings(findings,start_date=None):

    print('Retrieving reference application profile data...')

    theapps = Applications().get_all()

    for app in theapps:
        appfields = {}
        ref_custom_fields = []

        appfindings = [x for x in findings if int(x["app_id"]) == app["id"]]
        custom_fields = app["profile"]["custom_fields"]
        if (len(appfindings) == 0) or (custom_fields is None):
            continue
        
        for af in appfindings:
            for cf in custom_fields:
                af[cf['name']] = cf['value']

    return findings

def write_report(thefindings):
    recordcount = len(thefindings)

    if recordcount > 0:
        now = datetime.datetime.now().astimezone()
        filename = 'report-{}'.format(now)
        with open('{}.json'.format(filename), 'w') as outfile:
            json.dump(thefindings,outfile)
            outfile.close()

        print('Wrote {} findings to {}.json'.format(recordcount,filename))

def main():
    parser = argparse.ArgumentParser(
        description='This script retrieves findings for the date range specified and enriches the records with additional custom field information.')
    parser.add_argument('-s', '--start_datetime', help='Date (and time) from which to begin the report.')
    parser.add_argument('-e', '--end_datetime', help='If specified, end of date-time range for which to pull findings.')
    args = parser.parse_args()

    # CHECK FOR CREDENTIALS EXPIRATION
    creds_expire_days_warning()

    # set up args

    start_time = args.start_datetime
    end_time = args.end_datetime

    thefindings = generate_report(start_time=start_time, end_time=end_time)

    thefindings = enrich_findings(findings=thefindings,start_date=start_time)

    write_report(thefindings=thefindings)

if __name__ == '__main__':
    setup_logger()
    main()
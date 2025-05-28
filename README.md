# Veracode Reporting API Enricher

Fetches findings from Veracode and enriches the finding records with additional information from application profile custom fields.

Not an official Veracode product. 

## Setup

Clone this repository:

    git clone https://github.com/tjarrettveracode/veracode-reporting-api-fields

Install dependencies:

    cd veracode-reporting-api-fields
    pip install -r requirements.txt


### Authenticating 

Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

## Run

If you have saved credentials as above you can run:

    python reportingapi_fields.py (arguments)

Otherwise you will need to set environment variables before running `reportingapi_fields.py`:

    export VERACODE_API_KEY_ID=<YOUR_API_KEY_ID>
    export VERACODE_API_KEY_SECRET=<YOUR_API_KEY_SECRET>
    python reportingapi_fields.py (arguments)

## Arguments

    1. -s, --start_datetime  # Date (and time) from which to begin the report (e.g. "2025-01-01")
    2. -e, --end_datetime   # If specified, end of date-time range for which to pull findings (e.g. "2025-01-31 23:59:59").

## Notes

- To run this script, your user must have a role that can view application profile information like Submitter, Reviewer, or Security Lead (or custom role equivalent), as well as run the Reporting API ([see the docs for full details](https://docs.veracode.com/r/Reporting_REST_API#permissions-and-authentication)).


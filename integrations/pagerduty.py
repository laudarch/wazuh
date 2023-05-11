# Copyright (C) 2015, Wazuh Inc.
#
# This program is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License (version 2) as published by the FSF - Free Software
# Foundation.

import json
import os
import sys
import time

# Exit error codes
ERR_NO_REQUEST_MODULE   = 1
ERR_BAD_ARGUMENTS       = 2
ERR_FILE_NOT_FOUND      = 6
ERR_INVALID_JSON        = 7

try:
    import requests
    from requests.auth import HTTPBasicAuth
except Exception as e:
    print("No module 'requests' found. Install: pip install requests")
    sys.exit(ERR_NO_REQUEST_MODULE)

# ossec.conf configuration structure
# <integration>
#   <name>pagerduty</name>
#   <api_key>API_KEY</api_key> <!-- Replace with your PagerDuty API key -->
#   <options>JSON</options> <!-- Replace with your custom JSON object -->
# </integration>

# Global vars
debug_enabled   = False
pwd             = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
json_alert      = {}
json_options    = {}
now             = time.strftime("%a %b %d %H:%M:%S %Z %Y")

# Log path
LOG_FILE        = f'{pwd}/logs/integrations.log'

# Constants
ALERT_INDEX     = 1
APIKEY_INDEX    = 2


def main(args: list[str]):
    global debug_enabled
    try:
        # Read arguments
        bad_arguments: bool = False
        if len(args) >= 4:
            msg = '{0} {1} {2} {3} {4} {5}'.format(
                now,
                args[1],
                args[2],
                args[3],
                args[4] if len(args) > 4 else '',
                args[5] if len(args) > 5 else ''
            )
            debug_enabled = (len(args) > 4 and args[4] == 'debug')
        else:
            msg = '{0} Wrong arguments'.format(now)
            bad_arguments = True

        # Logging the call
        with open(LOG_FILE, "a") as f:
            f.write(msg + '\n')

        if bad_arguments:
            debug("# Exiting: Bad arguments. Inputted: %s" % args)
            sys.exit(ERR_BAD_ARGUMENTS)

        # Core function
        process_args(args)

    except Exception as e:
        debug(str(e))
        raise

def process_args(args: list[str]) -> None:
    """
        This is the core function, creates a message with all valid fields
        and overwrite or add with the optional fields

        Parameters
        ----------
        args : list[str]
            The argument list from main call
    """
    debug("# Starting")

    # Read args
    alert_file_location: str     = args[ALERT_INDEX]
    apikey: str                  = args[APIKEY_INDEX]
    options_file_location: str   = ''

    # Look for options file location
    for idx in range(4, len(args)):
        if(args[idx][-7:] == "options"):
            options_file_location = args[idx]
            break

    debug("# Options file location")
    debug(options_file_location)

    # Load options. Parse JSON object.
    json_options = get_json_file(options_file_location)

    debug("# Processing options")
    debug(json_options)

    debug("# Alert file location")
    debug(alert_file_location)

    # Load alert. Parse JSON object.
    json_alert = get_json_file(alert_file_location)

    debug("# Processing alert")
    debug(json_alert)

    debug("# Generating message")
    msg: any = generate_msg(json_alert, json_options,apikey)

    if not len(msg):
        debug("# ERR - Empty message")
        raise Exception
    debug(msg)

    debug("# Sending message")
    send_msg(msg)

def debug(msg: str) -> None:
    """
        Log the message in the log file with the timestamp, if debug flag
        is enabled

        Parameters
        ----------
        msg : str
            The message to be logged.
    """
    if debug_enabled:
        msg = "{0}: {1}\n".format(now, msg)
        print(msg)
        with open(LOG_FILE, "a") as f:
            f.write(msg)


def generate_msg(alert: any, options: any, apikey: str) -> str:
    """
        Generate the JSON object with the message to be send

        Parameters
        ----------
        alert : any
            JSON alert object.
        options: any
            JSON options object.

        Returns
        -------
        msg: str
            The JSON message to send
    """
    managed_security_url    = 'https://wazuh.com'
    level                   = alert['rule']['level']

    severity = 'info'
    if level >= 7:
        severity = 'warning'
    elif level >= 10:
        severity = 'error'
    elif level >= 13:
        severity = 'critical'

    groups = ', '.join(alert['rule']['groups'])

    msg = {
        'routing_key':  apikey,
        'event_action': 'trigger',
        'payload': {
            "summary": alert['rule']['description'] if 'description' in alert['rule'] else "N/A",
            "timestamp": alert['timestamp'],
            "source": alert['agent']['location'],
            "severity": severity,
            "group": groups,
            "custom_details": alert
        },
        "client": "Wazuh Monitoring Service",
        "client_url": managed_security_url
    }

    if(options):
        msg.update(options)

    return json.dumps(msg)

def send_msg(msg: any) -> None:
    """
        Send the message to the API

        Parameters
        ----------
        msg : str
            JSON message.
        url: str
            URL of the API.
    """

    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    url     = 'https://events.pagerduty.com/v2/enqueue'
    res     = requests.post(url, data=msg, headers=headers)
    debug("# Response received: %s" % res)

def get_json_file(file_location: str) -> any:
    """
        Read the JSON object from alert file

        Parameters
        ----------
        file_location : str
            Path to file alert location.

        Returns
        -------
        {}: any
            The JSON object read it.

        Raises
        ------
        FileNotFoundError
            If no alert file is not present.
        JSONDecodeError
            If no valid JSON file are used
    """
    try:
        with open(file_location) as alert_file:
            return json.load(alert_file)
    except FileNotFoundError:
        debug("# JSON file %s doesn't exist" % file_location)
        sys.exit(ERR_FILE_NOT_FOUND)
    except json.decoder.JSONDecodeError as e:
        debug("Failed getting json_alert %s" % e)
        sys.exit(ERR_INVALID_JSON)

if __name__ == "__main__":
    main(sys.argv)

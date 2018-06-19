#!/usr/bin/env python

'''
This script is to monitor if the head block time of a EOS blockchain is up to date. In the case of
head_block_time is more than 60 seconds older than current utc timestamp, we will trigger an email 
alert assuming something bad is happening, either the local blockchain is not full synced with global 
blockchain, or the global blockchain is halted for whatever reason.

'''
import argparse
import json
import requests
import os
import sys
from datetime import datetime, timedelta


def alert_head_block_freshness(http_endpoint, alert_email):
    """
    Keyword arguments:
    http_endpoint -- http endpoint of a blockchain node (full node or producer node)
    alert_email -- email address to send an alert in case of stale chain
    """

    print "\n\n**********************************"
    print "current time = ", datetime.utcnow()
    print "\nhttps_endpoint =", http_endpoint
    print "alert_email =", alert_email

    r = None
    try:
        r = requests.get(http_endpoint)
    except:
        print('An error occured when connect to http/s endpoint.')

    # send email alert if the http call is not successful
    if r is None or r.status_code != 200:
        print "\nRPC call to http/s endpoint failed, sending alert..."
        os.system('echo "Failed RPC call to http/s endpoint = {http_endpoint}" | mail -s "Alert: HTTP/S endpoint call is failing!" {email}'
		.format(http_endpoint=http_endpoint, email=alert_email))
        return

    obj = json.loads(r.content)
    print "response content =", json.dumps(obj)

    head_block_time_obj = datetime.strptime(obj['head_block_time'][0:19], '%Y-%m-%dT%H:%M:%S')
    print "\nhead_block_time =", head_block_time_obj.strftime('%Y-%m-%dT%H:%M:%S')
    current_utc_time_obj = datetime.utcnow()
    print "current_utc_time =", current_utc_time_obj.strftime('%Y-%m-%dT%H:%M:%S')

    time_diff = current_utc_time_obj - head_block_time_obj
    time_diff_in_seconds = time_diff.total_seconds()

    # send email alert if the time delta is no less than 60 seconds
    if time_diff_in_seconds >= 60:
        print "\nhead_block_lagged_by", time_diff_in_seconds, "seconds"
        os.system('echo "Out of sync BP node behind endpoint = {endpoint}" | mail -s "Alert: EOS blockchain is outdated!" {email}'
		.format(endpoint=http_endpoint, email=alert_email))
        sys.exit(1)


if __name__== "__main__":
    parser = argparse.ArgumentParser(description='Check data freshness of a given blockchain based on http/s call')
    parser.add_argument('-he', '--http_endpoint', help='http endpoint to check against', default='http://127.0.0.1:80/v1/chain/get_info')
    requiredArg = parser.add_argument_group('required arguments')
    requiredArg.add_argument('-ae', '--alert_email', help='email address to send alert to', required=True)
    
    args = parser.parse_args()
    options = vars(args)
    alert_head_block_freshness(options.get('http_endpoint'), options.get('alert_email'))




# 1. alert_head_block_freshness.py

## Purpose
This script is to monitor if head_block_time of a given EOS blockchain is up to date. In the case of
head_block_time is X seconds older than current utc timestamp, this script would trigger an email 
alert assuming something bad is happening, either the local blockchain is not full synced with global 
blockchain, or the global blockchain is halted for whatever reason.

## How to use it:
$ python alert_head_block_freshness.py -h

usage: alert_head_block_freshness.py [-h] [-he HTTP_ENDPOINT] -ae ALERT_EMAIL

Check data freshness of a given blockchain based on http/s call

optional arguments:

  -h, --help            show this help message and exit
  
  
  -he HTTP_ENDPOINT, --http_endpoint HTTP_ENDPOINT
                        http endpoint to check against


required arguments:

  -ae ALERT_EMAIL, --alert_email ALERT_EMAIL
                        email address to send alert to


## Alert example:
$ python alert_head_block_freshness.py --alert_email sanford.young@gmail.com

**********************************
current time =  2018-06-19 06:52:41.307859
https_endpoint = http://127.0.0.1:80/v1/chain/get_info
alert_email = sanford.young@gmail.com


response content = {"head_block_time": "2018-06-09T12:13:13.000", "block_cpu_limit": 99999900, "head_block_id": "00000708ddccd6168804a00c74bbac2779bbf76c5c8c90629313a6635af9ba15", "head_block_producer": "eosio", "chain_id": "aca376f206b8fc25a6ed44dbdc66547c36c6c33e3a119ffbeaef943642f0e906", "virtual_block_cpu_limit": 394987232, "virtual_block_net_limit": 6340393, "last_irreversible_block_id": "00000707595111b5a38351c9f2b9dbd2a5adf1bee20855f3744232315c087f82", "block_net_limit": 1048576, "last_irreversible_block_num": 1799, "server_version": "c9b7a247", "head_block_num": 1800}


head_block_time = 2018-06-09T12:13:13

current_utc_time = 2018-06-19T06:52:41


head_block_lagged_by 844768.357811 seconds, sending alert...

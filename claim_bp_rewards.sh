# /bin/bash -e

if [ "$#" -ne 2 ]; then
    echo "ERROR: exact 2 parameters (wallet name & password) are not specified, exit 1" >&2
    exit 1
fi

WALLET_NAME=$1
WALLET_PASSWORD=$2
DAY_IN_SECONDS=86400
HOME_DIR="/home/ubuntu/bp-monitor"
ALERT_EMAIL="fn-https@eossv.pagerduty.com"

# read last successful claim epochtime
last_claimed_epochtime=$(head -n 1 $HOME_DIR/logs/last_claimed_epochtime.log)
echo "last successful claim epochtime=$last_claimed_epochtime"

current_epochtime=`date +%s`
echo "current_epochtime=$current_epochtime"

time_diff=$((current_epochtime-last_claimed_epochtime))
echo "time_diff=$time_diff"

if [ "$time_diff" -le $DAY_IN_SECONDS ]; then
    echo "last successful claim time is less than 1 day ago, skipping claiming now...."
    exit 0
fi

echo "starting reward claiming..."
echo "unlcoking wallet..."
docker exec nodeos-bios cleos wallet lock -n $WALLET_NAME # lock wallet in case it's unlocked 
docker exec nodeos-bios cleos wallet unlock -n $WALLET_NAME --password $WALLET_PASSWORD

echo "claiming bp rewards..."
docker exec nodeos-bios cleos system claimrewards eossv12eossv > $HOME_DIR/logs/claim_bp_rewards.log 2>&1

EXITCODE=$?
if [ $EXITCODE -ne 0 ];then
   echo "ERROR: docker claimrewards failed!"
else
   echo ""
fi

count=$(grep -i "ERROR" -c $HOME_DIR/logs/claim_bp_rewards.log)
if [ "$count" -ne 0  ]; then
	echo "something wrong when claiming rewards...sending alert..."
        cat $HOME_DIR/logs/claim_bp_rewards.log | mail -s "ERROR: Claiming BP rewards failed...." $ALERT_EMAIL	
else
	echo "claiming rewards successfully...now updating last claimed epochtime..."
	echo "$current_epochtime" > $HOME_DIR/logs/last_claimed_epochtime.log
        cat $HOME_DIR/logs/claim_bp_rewards.log | mail -s "BINGO: Claiming BP rewards successfuly...." "sanford.young@gmail.com"
fi

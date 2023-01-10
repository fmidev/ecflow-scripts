#!/bin/bash
#
# Store start or finish time of a query to database
# partio 20140108

user=$INFRADB_USER
pass=$INFRADB_PASSWORD
host=$INFRADB_HOST
port=5432
dbname=process_meters

if [ $# -ne 5 ]; then
	echo "Usage: $0 pathname task operation date atime";
	exit 0
fi

# huruakka query path name
pathname=$1

# sms task name
task=$2

# 'start' or 'stop'
operation=$3

# %SMSDATE%, ie date
fcdate=$4

# analysis time, if applicable
atime=$5

time=$(date +%Y%m%d%H%M%S)
hour=$(date +%H)

sql=""
is_forecast=""

if [ $(echo $pathname | grep -c "forecast2smartmet") -eq 1 ] || [ $(echo $pathname | grep -c "forecast2brainstorm") -eq 1 ]; then
	is_forecast=1
elif [ $(echo $pathname | grep -ic "obs2laps") -eq 1 ] || [ $(echo $pathname | grep -ic "obs2smartmet") -eq 1 ]; then
	is_forecast=0
else
	# unsupported sms family
	exit 0
fi


if [ $is_forecast -eq 1 ]; then

	# check that atime is a number
	
	if [[ $atime == *[!0-9]* ]]; then
		# not a number, exit
		exit 0
	fi

	# check if clock is on the next day
	
	if [ $atime -ge 18 ] && [ $hour -lt 5 ]; then 
		fcdate=$(date +%Y%m%d -d '-1 day')
	fi

	sql="INSERT INTO fctimes (fcdate, fcatime, pathname, task, operation, datetime) VALUES (to_date('$fcdate', 'yyyymmdd'), $atime, '$pathname','$task','$operation',to_timestamp('$time', 'yyyymmddHH24MISS'))"

else
	# For observations we have to generate a unique identifier for each operation
	# In forecasts this is done by fdate and fcatime

	sql="INSERT INTO obstimes (pathname, task, operation, datetime) VALUES ('$pathname','$task','$operation',to_timestamp('$time', 'yyyymmddHH24MISS'))"
fi

echo $sql | PGPASSWORD=$pass psql -h $host -p $port -d $dbname -U $user > /dev/null 2>&1

exit 0

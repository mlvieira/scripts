#!/bin/env sh

# script to transfer photos taken by camera via rsync

date_format=$(date +'%d-%m-%Y')
IP='192.168.0.231'
user='rotten'
source_dir='/sdcard/DCIM/'
target_dir='~/Pictures/Personal-Photos/'
sanity_check(){
	nmap -p 22 "$IP" | grep open > /dev/null
}

while true; do
sanity_check
if [ "$?" -eq 0 ]; then
	echo "Connecting to SSH..."
	rsync -ravHP "$source_dir" "$user"@"$IP":"$target_dir""$date_format" --log-file="$date_format".txt
	exit
else
	echo "SSH is not available... Trying again in 5 seconds"
 	sleep 5
 	sanity_check
fi
done

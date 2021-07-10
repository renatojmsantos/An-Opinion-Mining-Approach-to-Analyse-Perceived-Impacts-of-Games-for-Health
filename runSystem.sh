#!/bin/bash

echo now=$(date +"%m_%d_%Y_%H:%M:%S")
while true
do
	if [ $(date "+%H") -gt 1 ] && [ $(date "+%H") -lt 5 ]; 
	then
	    python3 YouTube_Extractor.py 2009-09-17 4300 3600 True 'random' 1 5
	else
		sleep 21h
	fi
done


#python3 YouTube_Extractor.py 2009-09-17 7 2 True 'random'
#python3 YouTube_Extractor.py 2009-09-17 4200 2 True 'random'


#while [ $(date "+%H-%M") -lt $(date "+14:02")]; do
#    echo "test"
#    sleep 1
#done

#!/bin/bash

runtime="5 minute"
endtime=$(date -ud "$runtime" +%s)

while [[ $(date -u +%s) -le $endtime ]]
do
    echo "Time Now: `date +%H:%M:%S`"
    echo "Sleeping for 10 seconds"
    sleep 1m
done
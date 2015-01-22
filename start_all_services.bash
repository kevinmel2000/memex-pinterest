#!/bin/bash

cat /etc/hosts
netstat -a
nmap -p 27017 sourcepin-mongodb 
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR
bash start_crawl_services.bash | true
#mongod &
#echo "sleeping"
#sleep 60
cd ui/mongoutils
python memex_mongo_utils.py
cd ../../
export PYTHONPATH=`pwd`
cd ui
python server.py

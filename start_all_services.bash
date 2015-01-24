#!/bin/bash

cat /etc/hosts
netstat -a
nmap -p 27017 mongodb 
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR
bash start_crawl_services.bash | true
cd ui/mongoutils

#needs to be moved out or db will reset everytime application is started
#probably should change entry point so user instantiates database by themselves
if [ ! -f /sourcepin_inst ]; then
    echo "Instantiating the database..."
    sleep 30
    python memex_mongo_utils.py
    touch /sourcepin_inst
fi

cd ../../
export PYTHONPATH=`pwd`
cd ui
python server.py

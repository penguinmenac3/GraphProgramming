#!/bin/bash

sudo apt-get install -y python python-dev python-pip
sudo pip install autobahn[twisted]
sudo pip install futures

# Absolute path to this script. /home/user/bin/foo.sh
SCRIPT=$(readlink -f $0)
# Absolute path this script is in. /home/user/bin
SCRIPTPATH=`dirname $SCRIPT`

cd $SCRIPTPATH/grapheditor/electron
npm install

#!/bin/bash

echo "Installing python dependencies..."

echo "Installing virutalenv"
pip3 install virtualenvwrapper
source `which virtualenvwrapper.sh`
mkvirtualenv password
workon password

pip3 install --upgrade -r requirements.txt
deactivate

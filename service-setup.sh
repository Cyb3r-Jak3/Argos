#!/usr/bin/env bash

git clone https://github.com/cowrie/cowrie

sqlite3 cowrie.db < cowrie/docs/sql/sqlite3.sql

cd cowrie || exit

virtualenv --python=python3 cowrie-env 

source cowrie-env/bin/activate

pip install --upgrade pip

pip install --upgrade -r requirements.txt mysqlclient

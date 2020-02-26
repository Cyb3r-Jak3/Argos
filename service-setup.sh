#!/usr/bin/env bash

echo "0 0 */10 * * /home/cowrie/data_report.sh" >> mycron
crontab mycron
rm -f mycron

git clone https://github.com/cowrie/cowrie

sqlite3 cowrie.db < cowrie/docs/sql/sqlite3.sql

cd cowrie || exit

virtualenv --python=python3 cowrie-env 

# shellcheck disable=SC1091
source cowrie-env/bin/activate

pip install --upgrade pip

pip install --upgrade -r requirements.txt --quiet

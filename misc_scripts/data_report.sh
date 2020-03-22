#!/usr/bin/env bash

# shellcheck disable=SC1091
source /home/cowrie/cowrie/cowrie-env/bin/activate

timestamp=$(python3 query.py)
python3 report.py "$timestamp"

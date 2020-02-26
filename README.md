# Argos

## Under development

Argos is a honeypot system that will setup cowrie on a system.

## Setup

**It is recommended to create a gmail account specifically for this reporter.**

```bash
curl https://gitlab.com/Cyb3r-Jak3/Argos/-/raw/master/setup.sh -o setup.sh
curl https://gitlab.com/Cyb3r-Jak3/Argos/-/raw/master/report.dist.ini -o report.dist.ini # Leave the dist
# Edit report.dist.ini with smtp creds

chmod +x ./setup
./setup

```

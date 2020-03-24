# Argos

[![Maintainability](https://api.codeclimate.com/v1/badges/1aa3366ef6bd2ae7892f/maintainability)](https://codeclimate.com/github/Cyb3r-Jak3/Argos/maintainability)

## Beta

Argos is a honeypot system that sets up [cowrie](https://github.com/cowrie/cowrie) on a system.

## Setup

**It is *highly* recommended to create an email account with smtp access specifically for this reporter.**

```bash
curl https://gitlab.com/Cyb3r-Jak3/Argos/-/raw/master/setup.sh -o setup.sh
curl https://gitlab.com/Cyb3r-Jak3/Argos/-/raw/master/report.dist.ini -o report.dist.ini # Leave the dist
# Edit report.dist.ini with smtp creds

chmod +x ./setup
./setup
```

After the setup script has completed then you will have an `output.txt` file which will list the new SSH port and the password for cowrie user.  
**Make sure that you are able to connect with SSH before you continue.**

And cowrie is running you can attempt to login to your server using `ssh root@<server>`.

### Customization

If desired there is the ability to customize the cowrie configuration to your liking where you want in [cowrie.cfg](misc_scripts/cowrie.cfg).  
There are some options that should not be changed and they are:

- sqlite3 logging module
- listen_endpoints.

If you want to make changes then after pulling the setup script run with the argument `--setup` and it will pull all the files needed for setup without setting anything up.

#!/usr/bin/env bash

if [[ ! -e ./user-setup.sh ]]; then
    echo "Pulling user setup script from gitlab."
    curl https://gitlab.com/Cyb3r-Jak3/argos/-/raw/master/service-setup.sh -o user-setup.sh
fi

if [[ ! -e ./cowrie.cfg ]]; then
    echo "Pulling cowrie config from gitlab"
    curl https://gitlab.com/Cyb3r-Jak3/argos/-/raw/master/cowrie.cfg -o cowrie.cfg
fi

chmod +x user-setup.sh

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   read -n 1 -sr -p $"Press any key to continue using sudo."
   clear
   exec sudo "$0" "$@"
fi

function password_gen() {
	local pass
	pass=$(head /dev/urandom | tr -dc 'A-Za-z0-9~!@#$^*' | head -c"$1")
	echo "$pass"
}

apt-get install authbind build-essential curl default-libmysqlclient-dev git libffi-dev libpython3-dev libssl-dev openssl python3 python3-pip python-virtualenv sqlite3 virtualenv -qq

random_password=$(password_gen 15)

useradd --password "$( echo "$random_password" | openssl passwd -crypt -stdin )" --create-home --shell /bin/bash  cowrie || exit

sudo -i -u cowrie /home/setup/user-setup.sh

cp cowrie.cfg /home/cowrie/cowrie/etc/cowire.cfg
chown cowrie:cowrie /home/cowrie/cowrie/etc/cowire.cfg

echo "$random_password"

#!/usr/bin/env bash

if [[ $EUID -ne 0 ]]; then
    touch output.txt
    clear
    echo "This script must be run as root" 
    echo "Press any key to continue using sudo."
    read -n 1 -sr
    exec sudo "$0" "$@"
fi

function password_gen() {
	local pass
	pass=$(head /dev/urandom | tr -dc 'A-Za-z0-9~!@#$^*' | head -c"$1")
	echo "$pass"
}

function package_update() {
    # shellcheck disable=SC1090
    . /etc/*release
    if [[ "$ID" = "debian" ]] || [[ "$ID" = "ubuntu" ]]; then
        echo "Installing $ID distro packages"
        apt-get update && apt-get -qq upgrade > /dev/null
        apt-get -qq install authbind build-essential curl default-libmysqlclient-dev git libffi-dev libpython3-dev libssl-dev openssl python3 python3-pip python-virtualenv sqlite3 virtualenv > /dev/null
    elif [[ "$ID" = "centos" ]]; then
        echo "Install $ID distro packages"
        yum update -y > /dev/null
        yum install -y authbind build-essential curl default-libmysqlclient-dev git libffi-dev libpython3-dev libssl-dev openssl python3 python3-pip python-virtualenv sqlite3 virtualenv > /dev/null
    fi
}

function file_pull() {
    for script in "cowrie.cfg" "data_report.sh" "query.py" "report.py" "report.dist.ini" "cowrie.service" "cowrie.socket" "userdb.txt"; do
        if [[ ! -e ./$script ]]; then
            echo "Pulling $script from GitLab"
            curl -s -S https://gitlab.com/Cyb3r-Jak3/Argos/-/raw/master/misc_scripts/$script -o $script
        else
            echo "Using local $script."
        fi
        echo "Scripts loaded"
    done
}

function service_setup() {
    echo "Starting service setup"

    random_password=$(password_gen 15)
    useradd --password "$( echo "$random_password" | openssl passwd -crypt -stdin )" --create-home --shell /bin/bash  cowrie || exit


    sudo -i -u cowrie <<EOF
        echo "0 0 */10 * * /home/cowrie/data_report.sh" > mycron
        crontab mycron
        rm -f mycron

        git clone https://github.com/cowrie/cowrie &> /dev/null

        sqlite3 cowrie.db < cowrie/docs/sql/sqlite3.sql

        cd cowrie || exit 3

        virtualenv --python=python3 cowrie-env &> /dev/null

        # shellcheck disable=SC1091
        source cowrie-env/bin/activate

        pip install --upgrade pip --quiet

        pip install --upgrade -r requirements.txt --quiet
EOF

    cp {cowrie.cfg,userdb.txt} /home/cowrie/cowrie/etc/
    cp {data_report.sh,report.py,query.py} /home/cowrie/
    cp report.dist.ini /home/cowrie/report.ini
    chmod +x /home/cowrie/data_report.sh
    chown cowrie:cowrie /home/cowrie/{data_report.sh,query.py,report.py,report.ini}
    chown cowrie:cowrie /home/cowrie/cowrie/etc/{cowrie.cfg,userdb.txt}
    rm {cowrie.cfg,userdb.txt,data_report.sh,report.py,query.py,report.dist.ini}

    echo "cowrie: $random_password" >> output.txt
}

function harden() {
    random_port=$(( RANDOM % 3000 + 50000))
    sed -i -e 's/#Port/Port/' -e "/^Port\s/s/22/$random_port/" /etc/ssh/sshd_config
    sed -i[old] -e 's/^#PermitRootLogin\sprohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config
    echo "port: $random_port" >> output.txt
    systemctl restart sshd

}
function uid_check() {
    uid=$(cut -f 3 -d: /etc/passwd | sort -n | tail -n 2 | head -1)
    if [[ $uid -gt 1000 ]]; then
        echo "Warning High UID has been detected: $uid"
        echo "This is a usally a sign that there are more than the recommend amount of active users."
        echo "It is recommended that are only two non-default users"
        echo "By default Argo will cancel and remove all the setup work it has done."
        echo "To continue anyway. Enter \"accept\" to acknowledge the risks"
        read -r acknowledge
        if [[ $acknowledge = "accept" ]]; then
            echo -e "\e[1mYou have acknowledged the risk.\e[0m"
            echo "Argos will continue"
            sleep 5
        else
            echo "Argos is exiting"
            exit
        fi

    fi
}

function cowrie_authbind() {
    touch /etc/authbind/byport/22
    chown cowrie:cowrie /etc/authbind/byport/22
    chmod 770 /etc/authbind/byport/22
}

function systemd() {
    cp cowrie.service /etc/systemd/system/
    cp cowrie.socket /etc/systemd/system/

    cp /home/cowrie/cowrie/docs/systemd/etc/rsyslog.d/cowrie.conf /etc/rsyslog.d/
    cp /home/cowrie/cowrie/docs/systemd/etc/logrotate.d/cowrie /etc/logrotate.d/

    systemctl daemon-reload
    systemctl enable cowrie.service
}

uid_check
package_update
file_pull
harden
service_setup
cowrie_authbind
systemd

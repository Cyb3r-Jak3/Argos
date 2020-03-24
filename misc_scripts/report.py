import smtplib
import ssl
import configparser
import sys
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

timestamp = sys.argv[1]

config = configparser.ConfigParser()
config.read("report.ini")
config = config["DEFAULT"]


smtpserver = config["smtp_server"]
semail = config["sender_email"]
remail = config["receiver_email"]
password = config["password"]
if semail == "dummyemail@example.com":
    sys.exit(1)


message = MIMEMultipart()
message["From"] = semail
message["To"] = remail
message["Subject"] = f"Argos Report: {timestamp}"
body = "The reports are attached"
message.attach(MIMEText(body, "plain"))


for report in os.listdir(f"reports-{timestamp}"):
    report = f"reports-{timestamp}/" + report
    try:
        part = MIMEBase('application', 'ocetet-stream')
        part.set_payload(open(report, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment',
                        filename=report.split("/")[-1])
        message.attach(part)
    except Exception as e:
        print(f"Error with file: {report}\n{e}")


if config.getboolean('include_db'):
    try:
        part = MIMEBase('application', 'ocetet-stream')
        part.set_payload(open("cowrie.db", "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment',
                        filename="cowrie.db")
        message.attach(part)
    except Exception as e:
        print(f"Error with cowrie.db\n{e}")

if config.getboolean('raw_log'):
    try:
        part = MIMEBase('application', 'ocetet-stream')
        part.set_payload(open("cowrie/var/log/cowrie/cowrie.json",
                              "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment',
                        filename="cowrie.json")
        message.attach(part)
    except Exception as e:
        print(f"Error with cowrie.json\n{e}")


context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtpserver, port=465, context=context) as server:
    server.login(semail, password)
    server.sendmail(semail, remail, message.as_string())
    server.close()

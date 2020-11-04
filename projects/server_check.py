'''
    Requirements:
	1. Fetch complete status of five services("passport_url","space_url", "dashboard_url", "federated_url", "cos_url") for six releasese(16x, 17x, 18x, 19x, 20x, 21x). 
	2. Write a consolidated mail for all servers if-
	    a. Any service is down(Response Status is bad 4xx or 5xx).
	    b. Cos is shutdown.
	3. Send this consolidated mail to users(Users are different for different time).
	4. Mail should consist following information for each service and each release:
		Release: R423,
		Service Type: passport_url,
		URL: https://vdevpril207am.ux.dsone.3ds.com:453/iam/
		Status code: 503,
		    Status Message: KO
	 5. Create a batch file to run this python file and pass required parameters from it(releases, users).
	 6. Run this batch file using Jenkins after each 30 mins.
	 7. Create single log file for comlete day and put it on shared location.
'''

import subprocess
import os
import sys
import re
import logging
import smtplib
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import time
import textwrap
import xml.etree.ElementTree as ET
import urllib.request as ur


class ServerCheck:
    def __init__(self, release_level, notify_users):
        self.now = datetime.datetime.now()
        self.user = os.environ.get("USER")
        if self.user is None:
            self.user = "svc_simindus"
        self.usage_string = """
        USAGE: server_check -h for options
        """
        self.os_name = os.name
        self.host_name = self.hostname()
        self.success_code = ["200", "302"]
        self.failure_code = ["400", "401", "403", "404", "500", "503"]
        self.local = os.environ.get("LOCALAPPDATA")
        self.log_path = os.path.join(
            "\\\\filer2sim",
            "p",
            "inet",
            "groups",
            "pd",
            "rm",
            "content",
            "QC",
            "server_check_log",
        )
        self.path_wget_exe = os.path.join(self.local, "simqatools", "bin", "wget.exe")
        self.notify_users = notify_users
        self.release_level = release_level
        self.server_release_dict = {
            "R418": "453",
            "R419": "466",
            "R420": "925",
            "R421": "507",
            "R422": "540",
            "R423": "207",
        }
        self.url_types = {
            "passport_url": "453/iam/",
            "space_url": "443/3DSpace/",
            "dashboard_url": "444/3DDashboard/",
            "federated_url": "443/federated/",
            "cos_url": "446/SMAExeServer-REST/admin/",
        }

    def usage(self):
        formatted_usage = textwrap.dedent(self.usage_string).strip()
        print(formatted_usage)

    def hostname(self):
        if self.os_name == "posix":
            return os.environ.get("HOSTNAME")
        else:
            return os.environ.get("COMPUTERNAME")

    def time_stamp(self):
        timestamp = "_".join(
            str(i)
            for i in [self.now.year, "%02d" % self.now.month, "%02d" % self.now.day]
        )
        return timestamp

    def log_name(self):
        log = self.time_stamp() + ".log"
        return log

    def create_log(self):
        log_file = os.path.join(self.log_path, self.log_name())
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s --> %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    def send_email(self, to_address, subject, text=""):
        from_address = "{}@3ds.com".format(self.user)
        format_address = to_address.split(",")
        send_to = ",".join(format_address)

        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = send_to
        msg["Subject"] = subject

        body = text
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("gimli.ux.dsone.3ds.com")
        email_text = msg.as_string()
        server.sendmail(from_address, format_address, email_text)

    def url(self, release, url_type):
        complete_url = (
            "https://vdevpril"
            + self.server_release_dict.get(release)
            + "am.ux.dsone.3ds.com:"
            + self.url_types.get(url_type)
        )
        return complete_url

    def url_to_check_cos_station(self, release, url_type):
        http_url = (
            self.url(release, url_type)
            + "station/query?ActiveOnly=false&DRMMode=fiper&name=vdevpril"
            + self.server_release_dict.get(release)
            + "am"
        )
        print("HTTP URL to check cos station: {}".format(http_url))
        logging.info("HTTP URL to check cos station: {}".format(http_url))
        return http_url

    def get_attributes(self, xml):
        attributes = []
        for child in xml:
            if len(child.attrib) != 0:
                attributes.append(child.attrib)
            self.get_attributes(child)
        return attributes

    def status_of_cos_service(self, release, url_type):
        url_cos_station = self.url_to_check_cos_station(release, url_type)
        url = None
        try:
            url = ur.urlopen(url_cos_station)
        except:
            print(
                "Not able to fetch COS station status. Reason could be server status(503: Not Available)"
            )
            logging.error(
                "Not able to fetch COS station status. Reason could be server status(503: Not Available)"
            )
        if url:
            data = url.readline()
            xml_str = data.decode("ascii").strip()
            xml = ET.fromstring(xml_str)
            attributes = self.get_attributes(xml)
            for att_list in attributes:
                if (
                    att_list.get("name")
                    == "vdevpril" + self.server_release_dict.get(release) + "am"
                ):
                    if att_list.get("status") == "Shutdown":
                        print("COS Station is {}".format(att_list.get("status")))
                        logging.error(
                            "COS Station is {}".format(att_list.get("status"))
                        )
                        return """
                    Release: {},
                    Service Type: {},
                    URL for COS Station: {},
                    Status of COS Station: {}
                    """.format(
                            release, url_type, url_cos_station, att_list.get("status")
                        )
                    else:
                        print("COS Station is {}".format(att_list.get("status")))
                        logging.info("COS Station is {}".format(att_list.get("status")))

    def command_to_run(self, url):
        command = [
            self.path_wget_exe,
            "--no-check-certificate",
            "--spider",
            "--server-response",
        ]
        command.insert(1, url)
        return command

    def server_response(self, release, url, url_type):
        url_type_info = """
                Release: {},
                Service Type: {},
                URL: {}
                """.format(
            release, url_type, url
        )
        command_to_run = self.command_to_run(url)
        cmd = " ".join(command_to_run)
        data = subprocess.Popen(
            command_to_run, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        while data.poll() is None:
            data_out = data.stdout.readline()

            final_data = data_out.decode("ascii").strip()
            http_present = re.search(r"^HTTP[/][0-9][.][0-9]", final_data)
            if http_present:
                all_status_code = self.success_code + self.failure_code
                for status in all_status_code:
                    if status in final_data:
                        if status == "302":
                            flag = True
                            while flag:
                                data_out = data.stdout.readline()
                                final_data = data_out.decode("ascii").strip()
                                location_present = re.search(
                                    r"^Location[:]", final_data
                                )
                                if location_present:
                                    logging.info(
                                        "Getting {} status code for {}: {}.".format(
                                            status, url_type, url
                                        )
                                    )
                                    print(
                                        "Getting {} status code for {}: {}.".format(
                                            status, url_type, url
                                        )
                                    )
                                    logging.info(
                                        "So, Redirected URL is: {}".format(
                                            final_data[10:]
                                        )
                                    )
                                    print(
                                        "So, Redirected URL is: {}".format(
                                            final_data[10:]
                                        )
                                    )
                                    url = final_data[10:]
                                    flag = False
                                    url_type_info = (
                                        url_type_info
                                        + """Status code: {},\n\t New URL: {}\n\t""".format(
                                            status, url
                                        )
                                    )
                                    break
                        elif status in self.failure_code:
                            status_message = "KO"
                            logging.error("Status: {}".format(status))
                            logging.error("Status Message: {}".format(status_message))
                            print("Status: {}".format(status))
                            print("Status Message: {}".format(status_message))
                            logging.error("Server response is bad.")
                            print("Server response is bad.")
                            url_type_info = (
                                url_type_info
                                + "Status code: {},\n\t  Status Message: {}\n\n".format(
                                    status, status_message
                                )
                            )
                            return url_type_info

                        elif status in self.success_code:
                            logging.info("Status: {}".format(status))
                            print("Status: {}".format(status))

    def send_email_according_time(self, all_server_complete_info):
        if self.notify_users:
            pass
        else:
            tme = ".".join(str(i) for i in [self.now.hour, self.now.minute])
            tme = float(tme)
            if 0 <= tme and tme <= 8:
                self.notify_users = "msi26@3ds.com,j92@3ds.com,vus@3ds.com,bsu@3ds.com,r6e@3ds.com,h93@3ds.com"
            if 8 <= tme and tme <= 18:
                self.notify_users = (
                    "msi26@3ds.com,j92@3ds.com,vus@3ds.com,p6j@3ds.com,vuq@3ds.com,"
                    + "rst1@3ds.com,aaa18@3ds.com"
                )
            if 18 <= tme and tme <= 24:
                self.notify_users = "msi26@3ds.com,vus@3ds.com"
        self.send_email(
            to_address=self.notify_users,
            subject="Server check",
            text=self.mail_msg(all_server_complete_info),
        )
        print("Email sent to: {}".format(self.notify_users))
        logging.info("Email sent to: {}".format(self.notify_users))

    def mail_msg(self, all_server_complete_info):
        if all_server_complete_info:
            msg = """
            Hello,

            Following servers have bad response:
            {}
            Thanks.
            """.format(
                all_server_complete_info
            )
            return msg

    def setup(self):
        if sys.argv[1:] == []:
            self.usage()
            sys.exit(0)
        self.create_log()
        link = "https://inet/groups/pd/rm/content/QC/server_check_log"
        logging.info("Please check log file on link: {}".format(link))
        print("Please check log file on link: {}".format(link))
        logging.info("MACHINE: {}".format(self.host_name))

    def run(self):
        url_types = [
            "passport_url",
            "space_url",
            "dashboard_url",
            "federated_url",
            "cos_url",
        ]
        all_server_complete_info = ""
        if self.release_level:
            self.release_level = self.release_level.split(",")
            for release in self.release_level:
                if release in self.server_release_dict.keys():
                    release_header = (
                        "****************************"
                        + str(release)
                        + "****************************"
                    )
                    print(release_header)
                    logging.info(release_header)
                    for url_type in url_types:
                        url_type_cos_info = None
                        url = self.url(release, url_type)
                        print("URL: {}".format(url))
                        logging.info("URL: {}".format(url))
                        print("Service Type: {}".format(url_type))
                        logging.info("Service Type: {}".format(url_type))
                        url_type_info = self.server_response(release, url, url_type)
                        if url_type == "cos_url":
                            url_type_cos_info = self.status_of_cos_service(
                                release, url_type
                            )
                        if url_type_cos_info:
                            all_server_complete_info = (
                                all_server_complete_info + url_type_cos_info
                            )
                        if url_type_info:
                            all_server_complete_info = (
                                all_server_complete_info + url_type_info
                            )
                        else:
                            logging.info("Server response is good.")
                else:
                    logging.error(
                        "Please mention Release level from: {}.".format(
                            self.server_release_dict.keys()
                        )
                    )
                    sys.exit(1)
        else:
            logging.error("Please mention Release level in the format 'R4XX'.")
            sys.exit(1)

        if all_server_complete_info:
            self.send_email_according_time(all_server_complete_info)


if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-release_level",
        "--release_level",
        help="provide release level to fetch response. \
                        Ex: -release_level R421 for single release or \
                        -release_level R421,R422,R423 for multiple releases",
    )

    parser.add_argument(
        "-notify",
        "--notify",
        help="provide email to send notifications, if user is not present in below list. \
                        user = j92, vus, p6j, vuq, rst1, aaa18, bsu, msi26 \
                        Ex: -notify msi26@3ds.com for single notification or \
                        -notify msi26@3ds.com,vwj@3ds.com for multiple notifications",
    )

    args = parser.parse_args()
    release_level = args.release_level
    notify = args.notify
    server_check = ServerCheck(release_level=release_level, notify_users=notify)
    server_check.setup()
    server_check.run()

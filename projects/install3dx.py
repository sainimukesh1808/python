#!/usr/bin/env python

import argparse
import ctypes
import datetime
import os
import logging
import re
import smtplib
import subprocess
import sys
import textwrap
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class PreProcessing:

    def __init__(self):
        self.now = datetime.datetime.now()
        self.usage_string = '''
        USAGE: python install3DXClient.py -h for options
        '''
        self.os_name = os.name
        self.user = os.environ.get('USER')
        self.host_name = self.hostname()
        self.TMPDIR = os.path.join(os.environ.get('TMPDIR'), self.user)

    def time_stamp(self):
        timestamp = '_'.join(str(i) for i in [self.now.year, self.now.month, self.now.day,
                                              self.now.hour, self.now.minute, self.now.second])
        return timestamp

    def usage(self):
        formatted_usage = textwrap.dedent(self.usage_string).strip()
        print(formatted_usage)

    def log_name(self):
        log = '_'.join(['install', self.time_stamp()]) + '.log'
        return log

    def hostname(self):
        if self.os_name == 'posix':
            return os.environ.get('HOSTNAME')
        else:
            return os.environ.get('COMPUTERNAME')

    def create_log(self):
        if not os.path.exists(self.TMPDIR):
            os.makedirs(self.TMPDIR, 0o777)
        log_file = os.path.join(self.TMPDIR, self.log_name())
        logging.basicConfig(filename=log_file, level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s --> %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        print("FOR MORE INFORMATION -- {}:{}".format(self.host_name, log_file))

    def setup(self):
        if sys.argv[1:] == []:
            self.usage()
            sys.exit(0)
        self.create_log()
        logging.info("Start logging.")
        logging.info("PLATFORM: {}".format(self.os_name))
        logging.info("USER: {}".format(self.user))
        logging.info("MACHINE: {}".format(self.host_name))


class InstallClient(PreProcessing):

    def __init__(self, copy, src, dst, extract, config, rollback_path,
                 uninstall_path, media_selection, notify_users,
                 include_build_id):
        self.copy = copy
        self.src = src
        self.dst = dst
        self.extract = extract
        self.config = config
        self.rollback_path = rollback_path
        self.uninstall_path = uninstall_path
        self.media_selection = media_selection
        self.notify_users = notify_users
        self.include_build_id = include_build_id

        PreProcessing.__init__(self)

        self.VALID_EXTENSIONS = ['.iso', '.tar.gz', '.zip']
        self.REG_LOCATION = {'R417': 'B417',
                             'R418': 'B418',
                             'R419': 'B419',
                             'R420': 'B420',
                             'R421': 'B421',
                             'R422': 'B422',
                             'R423': 'B423'}
        self.VERSION = {'R417': 'R2015x',
                        'R418': 'R2016x',
                        'R419': 'R2017x',
                        'R420': 'R2018x',
                        'R421': '2019x',
                        'R422': '2020x',
                        'R423': '2021x'}
        self.INSTALL_LOCATION = {'R417': os.path.join('D:\\', 'wdir', 'do_not_delete',
                                                      'R2015xPHYAPPS'),
                                 'R418': os.path.join('D:\\', 'wdir', 'do_not_delete',
                                                      'R2016xPHYAPPS'),
                                 'R419': os.path.join('D:\\', 'wdir', 'do_not_delete',
                                                      'R2017xPHYAPPS'),
                                 'R420': os.path.join('D:\\', 'wdir', 'do_not_delete',
                                                      'R2018xPHYAPPS'),
                                 'R421': os.path.join('D:\\', 'wdir', 'do_not_delete',
                                                      'R2019xPHYAPPS'),
                                 'R422': os.path.join('D:\\', 'wdir', 'do_not_delete',
                                                      'R2020xPHYAPPS'),
                                 'R423': os.path.join('D:\\', 'wdir', 'do_not_delete',
                                                      'R2021xPHYAPPS')
                                 }

    def prechecks(self):
        if self.src and not self.config:
            logging.error("-config is mandatory with -install and vice-versa.")
            print("ERROR: -install and -config are mutually necessary.")
            sys.exit(1)

    def elevatedPrompt(self):
        admin = ctypes.windll.shell32.IsUserAnAdmin()
        if admin == 0:
            print("ERROR: Run this script with an elevated command prompt.")
            print(
                "INFO: Right click on 'Command Prompt' to select 'Run as administrator'.")
            logging.error("Not an admin prompt.")
            sys.exit(0)
        else:
            logging.info("Running from 'admin' prompt.")

    def copy_package(self):
        if not os.path.exists(self.src):
            print("ERROR: {} not found.".format(self.src))
            sys.exit(1)

        self.dst = os.path.join(self.dst, 'LATEST_PACKAGE_COPY_' + self.include_build_id)

        if self.os_name == 'posix':
            copy_cmd = ['rsync', '-avz', '--delete', self.src, self.dst]
        else:
            copy_cmd = ['robocopy', self.src, self.dst, '/MIR']

        logging.info("Copying from {} to {}".format(self.src, self.dst))
        logging.info("Copy Command: {}".format(' '.join(copy_cmd)))
        status = subprocess.call(copy_cmd)
        if status == 0:
            logging.info("No errors occurred and no files were copied. Copy command is skipped. Exit Code: {}".format(status))
        elif status == 1:
            logging.info("All files were copied successfully. Exit Code: {}".format(status))
        elif status == 2:
            logging.info("Some files copied and Additional files were present in source file. "
                            + "Exit Code: {}".format(status))
        elif status == 4:
            logging.info("Mismatched files or directories were detected. Exit Code: {}".format(status))
        elif status == 8:
            logging.info("Some files or directories could not be copied and the retry limit was exceeded. "
                            + "Exit Code: {}".format(status))
            sys.exit(1)
        elif status > 8:
            logging.info("Robocopy did not copy any files. Check the command line parameters and "
                            +"verify that Robocopy has enough rights to write to the destination folder. "
                            + "Exit Code: {}".format(status))
            sys.exit(1)
        else:
            logging.info("Copy command exited with status: {}".format(status))
        return self.dst

    def find_valid_extensions(self, directory):
        media_path = directory
        logging.debug("Content in media path: {}".format(
            os.listdir(media_path)))
        logging.info("Check for valid extensions in {}".format(media_path))
        media_files = []
        regex_ext = '|'.join([i + '$' for i in self.VALID_EXTENSIONS])
        logging.debug("CONSTRUCTED REGEX: {}".format(regex_ext))
        logging.debug("Current media path: {}".format(media_path))
        for root, dirs, files, in os.walk(media_path):
            for name in files:
                if re.search(r'%s' % regex_ext, name):
                    media_files.append(os.path.join(root, name))
        logging.debug(
            "Found these files to be extracted: {}".format(media_files))
        return media_files

    def reg_query(self, keyname, filename, keyvalue=None):
        name, ext = os.path.splitext(filename)
        outname = name + '_OUT' + ext
        errname = name + '_ERR' + ext
        try:
            out_obj = open(outname, 'w')
            err_obj = open(errname, 'w')
        except:
            print("ERROR: Unable to write to {}".format(filename))
            sys.exit(1)
        if keyvalue:
            command = ['reg', 'query', keyname, '/v', keyvalue]
        else:
            command = ['reg', 'query', keyname]
        logging.info("REG COMMAND: {}".format(" ".join(command)))
        proc = subprocess.Popen(command, stdout=out_obj, stderr=err_obj)
        while proc.poll() is None:
            time.sleep(0.5)
        out_obj.close()
        err_obj.close()
        status = proc.returncode
        if status == 0:
            logging.info("Reg command is successful and exited with status: {}".format(status))
        else:
            logging.error("Reg command is failed and exited with status: {}".format(status))
        return status, outname, errname

    def extract_files(self, file_list):
        file_path, file_name = os.path.split(file_list[0])
        extract_path = os.path.join(file_path, 'EXTRACTED')
        if os.path.exists(extract_path):
            logging.info(
                "Path to extract already exists: {}".format(extract_path))
            logging.debug("Contents in {}: {}".format(
                extract_path, os.listdir(extract_path)))
            logging.info("Removing {}".format(extract_path))
            remove_cmd = ['rm', '-rf', extract_path]
            status = subprocess.call(remove_cmd)
            logging.info("REMOVE COMMAND: {}".format(' '.join(remove_cmd)))
            logging.info("REMOVE COMMAND STATUS CODE: {}".format(status))
            if status == 0:
                logging.info("Successfully removed {}".format(extract_path))
                os.makedirs(extract_path, 0o777)
                logging.info(
                    "Now {} is created for extracting.".format(extract_path))
            else:
                print("ERROR: Removing {}".format(extract_path))
                sys.exit(1)
        else:
            logging.info(
                "Extract path: {} will be created.".format(extract_path))
            os.makedirs(extract_path, 0o777)
            logging.debug("Content in {}: {}".format(
                extract_path, os.listdir(extract_path)))
        if self.os_name == 'posix':
            count = 0
            for compressed_file in file_list:
                zip_command = ['tar', '-xvzf',
                               compressed_file, '-C', extract_path]
                count += 1
                logging.info(
                    "COMMAND TO EXTRACT -- {}: {}".format(count, ' '.join(zip_command)))
                status = subprocess.call(zip_command)
                if status == 0:
                    logging.info("Extract command is successful.")
                    logging.info(
                        "Command to extract -- {} exited with status: {}".format(count, status))
                else:
                    logging.info("Extract command is failed and exited with status: {}".format(status))

        else:
            # logic to find out 7z path from registry
            zip_status, file_out, file_err = self.reg_query(
                keyname=r'HKEY_LOCAL_MACHINE\SOFTWARE\7-Zip', keyvalue='Path',
                filename='zip_install_path.txt')
            if zip_status == 1:
                zip_status, file_out, file_err = self.reg_query(
                    keyname=r'HKEY_CURRENT_USER\SOFTWARE\7-Zip', keyvalue='Path',
                    filename='zip_install_path.txt')
            if zip_status == 0:
                try:
                    read_out = open(file_out, 'r')
                    read_err = open(file_err, 'r')
                except:
                    print("ERROR: Unable to write to {}".format(filename))
                    sys.exit(1)
                else:
                    logging.info(
                        "REG COMMAND OUTPUT written to {}".format(file_out))
                    logging.info(
                        "REG COMMAND ERROR written to {}".format(file_err))
                    contents_out = read_out.readlines()
                    contents_err = read_err.readlines()
                    read_out.close()
                    read_err.close()
                    logging.debug("Contents of {}: {}".format(
                        file_out, contents_out))
                    logging.debug("Contents of {}: {}".format(
                        file_err, contents_err))

                if contents_err != []:
                    print("ERROR: {} file is not empty.".format(file_err))
                    sys.exit(1)
                if contents_out == []:
                    print("ERROR: {} file is empty.".format(file_out))
                    sys.exit(1)
                for line in contents_out:
                    if re.search(r'Path', line):
                        found_path = line
                if found_path.strip() == '':
                    print("ERROR: 7z path not found.")
                    sys.exit(1)
                processed_path = found_path.strip('\n').replace(
                    'Path', '').replace('REG_SZ', '').strip()
                os.remove(file_out)
                os.remove(file_err)
                zip_exe = os.path.join(r'%s' % processed_path, '7z.exe')
                logging.info("ZIP EXECUTABLE: {}".format(zip_exe))

                count = 0
                for compressed_file in file_list:
                    zip_command = [zip_exe, 'x', compressed_file,
                                   '-y', '-o%s' % extract_path]
                    count += 1
                    logging.info(
                        "COMMAND TO EXTRACT -- {}: {}".format(count, ' '.join(zip_command)))
                    status = subprocess.call(zip_command)
                    if status == 0:
                        logging.info("Extract command is successful.")
                        logging.info(
                            "Command to extract -- {} exited with status: {}".format(count, status))
                    else:
                        logging.info("Extract command is failed and exited with status: {}".format(status))
            else:
                print("ERROR: registry command to find 7z path failed.")
                sys.exit(1)
        return extract_path

    def find_silent_installer(self, root_dir, win_exe='StartTUI.exe', lnx_exe='StartTUI.sh'):
        if self.media_selection == 'cos':
            root_dir = os.path.join(
                root_dir, '3DEXPERIENCE_3DOrchestrateServices')
        if self.media_selection == 'res':
            root_dir = os.path.join(
                root_dir, '3DEXPERIENCE_PhysicsResultsServices')
        if self.media_selection == 'sim':
            root_dir = os.path.join(
                root_dir, '3DEXPERIENCE_SimulationServices')

        # validate path existence
        if not os.path.exists(root_dir):
            logging.error("Directory does not exist: {}".format(root_dir))
            print("ERROR: Cannot find {}".format(root_dir))
            sys.exit(1)

        if self.os_name == 'posix':
            exe_name = lnx_exe
            regex_pattern = re.compile(r'^%s$' % exe_name)
        else:
            exe_name = win_exe
            regex_pattern = re.compile(r'^%s$' % exe_name)
        logging.info("Look for {} in {}".format(exe_name, root_dir))

        for root, dirs, files in os.walk(root_dir):
            for name in files:
                if re.search(regex_pattern, name):
                    exe_full = os.path.join(root, name)
                    logging.info("Found installer: {}".format(exe_full))
                    return exe_full

    def send_email(self, to_address, subject, text=''):
        from_address = '{}@3ds.com'.format(self.user)
        format_address = to_address.split(',')
        send_to = ','.join(format_address)

        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = send_to
        msg['Subject'] = subject

        body = text
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('gimli.ux.dsone.3ds.com')
        email_text = msg.as_string()
        server.sendmail(from_address, format_address, email_text)
        logging.debug("Email sent to {} from {}".format(
            format_address, from_address))

    def extract_build_from_install_dir(self, install_dir):
        """find the build id for the installed build and return it"""
        log_dir = os.path.join(install_dir, 'InstallData', 'log')
        logs = []
        if os.path.exists(log_dir):
            for root, _, files in os.walk(log_dir):
                for name in files:
                    if name == 'Everything.log':
                        logs.append(os.path.join(root, name))
            if len(logs) == 0:
                return "Not found."
            summary_file = max(logs, key=os.path.getmtime)
            if os.path.exists(summary_file):
                with open(summary_file, 'r') as summary_obj:
                    for line in summary_obj:
                        if re.search(r'JS0GROUP build id:', line):
                            build_line = line
                            build_id = build_line.split(':')[-1].strip()
                            return "-".join([build_id[4:6], build_id[6:8], build_id[0:4]])
        return "Not found."

    def install(self, installer):
        if not self.config:
            print("ERROR: -config is mandatory to perform silent install.")
            sys.exit(1)
        command = [installer, '--silent', self.config]
        logging.info("INSTALL COMMAND: {}".format(' '.join(command)))
        status = subprocess.call(command)
        build_number = 'Skipped by user {} or by program itself.'.format(
            self.user)
        if self.include_build_id and self.os_name != 'posix':
            build_number = self.extract_build_from_install_dir(
                                self.INSTALL_LOCATION[self.include_build_id])
            version_name = self.VERSION[self.include_build_id]
        if self.notify_users:
            if status == 0:
                msg = '''
                Hello,

                Install completed successfully on {}.\n
                Version: {}\n
                Command: {}\n
                Current Build: {}

                Thanks.
                '''.format(self.host_name, version_name, ' '.join(command), build_number)
                dedented_msg = textwrap.dedent(msg).strip()
                self.send_email(to_address=self.notify_users,
                                subject='{}: Install Success on {}'.format(
                                    version_name, self.host_name),
                                text=dedented_msg)
            else:
                msg = '''
                Hello,

                Install failed on {}.\n
                Version: {}\n
                Command: {}\n
                Current Build: {}

                Thanks.
                '''.format(self.host_name, version_name, ' '.join(command), build_number)
                dedented_msg = textwrap.dedent(msg).strip()
                self.send_email(to_address=self.notify_users,
                                subject='ERROR: {}: Install failed on {}'.format(version_name,
                                                                                 self.host_name),
                                text=dedented_msg)
        if status == 0:
            logging.info(
                "Installation command is successful and exited with status: {}".format(status))
        else:
            logging.info(
                "Installation command is failed with exited with status: {}".format(status))
            sys.exit(1)

    def rollback_HF(self):
        installer = self.find_silent_installer(self.rollback_path)
        if installer is None:
            print("ERROR: Unable to find Rollback executable in {}".format(
                self.rollback_path))
            sys.exit(1)
        logging.info("Found installer to rollback: {}".format(installer))
        command = [installer, '-SoftMgt', '-Rollback']
        logging.info("ROLLBACK COMMAND: {}".format(' '.join(command)))
        status = subprocess.call(command)
        build_number = 'Skipped by user: {}'.format(self.user)
        if self.include_build_id and self.os_name != 'posix':
            version_name = self.VERSION[self.include_build_id]
        if self.notify_users:
            if status == 0:
                msg = '''
                Hello,

                Rollback completed successfully on {}.\n
                Version: {}\n
                Command: {}\n

                Thanks.
                '''.format(self.host_name, version_name, ' '.join(command))
                dedented_msg = textwrap.dedent(msg).strip()
                self.send_email(to_address=self.notify_users,
                                subject='{}: Rollback Success on {}'.format(version_name,
                                                                            self.host_name),
                                text=dedented_msg)
            else:
                msg = '''
                Hello,

                Rollback failed on {}.\n
                Version: {}\n
                Command: {}\n

                Thanks.
                '''.format(self.host_name, version_name, ' '.join(command))
                dedented_msg = textwrap.dedent(msg).strip()
                self.send_email(to_address=self.notify_users,
                                subject='ERROR: {}: Rollback failed on {}'.format(version_name,
                                                                                  self.host_name),
                                text=dedented_msg)
        if status == 0:
            logging.info(
                "Installation command is successful and exited with status: {}".format(status))
        else:
            logging.info(
                "Installation command is failed with exited with status: {}".format(status))
            sys.exit(1)

    def uninstall(self):
        installer = self.find_silent_installer(
            self.uninstall_path, 'Uninstall.bat', 'Uninstall.sh')
        if installer is None:
            print("ERROR: Unable to find Uninstall executable in {}".format(
                self.uninstall_path))
            sys.exit(1)
        logging.info("Found uninstall executable: {}".format(installer))
        command = [installer, '-quiet']
        logging.info("UNINSTALL COMMAND: {}".format(' '.join(command)))
        status = subprocess.call(command)
        if status == 0:
            logging.info("Uninstall command is successful and exited with status: {}".format(status))
        else:
            logging.info("Uninstall command is exited with status: {}".format(status))


    def rm(self, directory):
        command = ['rm', '-rf', directory]
        logging.info("CLEANUP COMMAND: {}".format(' '.join(command)))
        status = subprocess.call(command)
        if status == 0:
            logging.info("Cleanup command is successful and  exited with status: {}".format(status))
        else:
            logging.info("Cleanup command exited with status: {}".format(status))

    def cleanup(self):
        if self.uninstall_path:
            self.rm(self.uninstall_path)

    def run(self):
        self.prechecks()
        work_directory = self.src
        if self.os_name != 'posix':
            self.elevatedPrompt()
        if self.copy:
            work_directory = self.copy_package()
        if self.extract:
            files_to_extract = self.find_valid_extensions(work_directory)
            if len(files_to_extract) > 0:
                work_directory = self.extract_files(files_to_extract)
            else:
                print("ERROR: No files found to extract.")
                sys.exit(1)
        if self.src:
            if self.rollback_path:
                self.rollback_HF()
            installer = self.find_silent_installer(work_directory)
            if not installer:
                print("ERROR: Installer not found in {}".format(work_directory))
                sys.exit(1)
            self.install(installer)
        if self.uninstall_path:
            self.uninstall()
            self.cleanup()


if __name__ == '__main__':

    pre = PreProcessing()
    pre.setup()

    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-install', '--install', nargs='+',
                        help='provide media to install')
    parser.add_argument('-uninstall', '--uninstall', nargs='+',
                        help='provide installed media path to uninstall')
    parser.add_argument('-rollback', '--rollback', nargs='+',
                        help='provide the installed media path to rollback.')
    parser.add_argument('-copy', '--copy',
                        help='option for copying media source to destination triggered',
                        action='store_true')
    parser.add_argument('-extract', '--extract',
                        help='option for extracting source or target media triggered.',
                        action='store_true')
    parser.add_argument('-destination', '--destination', nargs='+',
                        help='provide the destination directory where installation package should be copied.',
                        default=pre.TMPDIR)
    parser.add_argument('-config', '--config', nargs='+',
                        help='provide user intentions xml file needed for silent install.')
    parser.add_argument('-select', '--select',
                        help='provide appropriately for updating 3DOrchestrateServices (cos), \
                        PhysicsResultsServices (res), SimulationServices(sim). \
                        VALID OPTIONS: cos|res|sim')
    parser.add_argument('-showbuild', '--showbuild',
                        help='this includes the build id installed to the notification. \
                        VALID OPTIONS: R417|R418|R419|R420|R421 \
                        Ex: -showbuild R419')
    parser.add_argument('-notify', '--notify',
                        help='provide email to send notifications. \
                        Ex: -notify abc@xyz.com for single notification or \
                        -notify abc@xyz.com,def@xyz.com for multiple users')

    args = parser.parse_args()

    install = args.install
    if isinstance(install, list):
        install = ' '.join(install)
    logging.debug("-install: {}".format(install))
    uninstall = args.uninstall
    if isinstance(uninstall, list):
        uninstall = ' '.join(uninstall)
    logging.debug("-uninstall: {}".format(uninstall))
    rollback = args.rollback
    if isinstance(rollback, list):
        rollback = ' '.join(rollback)
    logging.debug("-rollback: {}".format(rollback))
    isCopy = args.copy
    logging.debug("-copy: {}".format(isCopy))
    isExtract = args.extract
    logging.debug("-extract: {}".format(isExtract))
    destination_path = args.destination
    if isinstance(destination_path, list):
        destination_path = ' '.join(destination_path)
    logging.debug("-destination: {}".format(destination_path))
    config_file = args.config
    if isinstance(config_file, list):
        config_file = ' '.join(config_file)
    logging.debug("-config: {}".format(config_file))
    select_media = args.select
    logging.debug("-select: {}".format(select_media))
    showbuild = args.showbuild
    logging.debug("-showbuild: {}".format(showbuild))
    notify = args.notify
    logging.debug("-notify: {}".format(notify))
    if notify and not showbuild:
        logging.error("'-showbuild <version>' is needed when '-notify' is used.")
        sys.exit(0)
    install = InstallClient(copy=isCopy, src=install,
                            dst=destination_path, extract=isExtract,
                            config=config_file, rollback_path=rollback,
                            uninstall_path=uninstall, media_selection=select_media,
                            notify_users=notify, include_build_id=showbuild)
    install.run()

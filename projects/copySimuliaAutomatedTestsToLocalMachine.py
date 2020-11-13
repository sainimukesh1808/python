#!/usr/bin/env python
"""
Valid level names:
    R418
    R419
    R420
    R421
    R422
    R420FD03
    R420FD04
"""

import os
import sys
import argparse
import subprocess
import datetime


def find_latest_snapshot_to_copy(tag_level, dir_name):
    """Determines the latest snapshot available in the filer to copy from"""
    all_snapshots = [i for i in os.listdir(dir_name) if
                     i.startswith(tag_level)]
    max_snap = str(max([int(i.split('_')[-1]) for
                        i in all_snapshots]))
    latest_snap = tag_level + '_' + max_snap
    return os.path.join(dir_name, latest_snap), latest_snap


if __name__ == '__main__':
    # Enforce to run only on windows
    if os.name != 'nt':
        print("ERROR: {} should be run only on windows.".format(sys.argv[0]))
        sys.exit(1)

    # Important Constants
    LEVELS_COPY_TO = {'R418': '2016x_SCM',
                      'R419': '2017x_SCM',
                      'R420': '2018x_SCM',
                      'R421': '2019x_SCM',
                      'R422': '2020x_SCM',
                      'R421OC': '2019x_SCM_OC',
                      'R420FD03': '2018x_SCM_FD03',
                      'R420FD04': '2018x_SCM_FD04'}

    LEVELS_COPY_FROM = {'R418': 'SIMUIAUTO418',
                        'R419': 'SIMUIAUTO419',
                        'R420': 'SIMUIAUTO420',
                        'R421': 'SIMUIAUTO421',
                        'R422': 'SIMUIAUTO422',
                        'R421OC': 'SIMUIAUTO421OC',
                        'R420FD03': 'SIMUIAUTO420FD03',
                        'R420FD04': 'SIMUIAUTO420FD04'}

    MAIN_SNAPSHOT_PATH = os.path.join('\\\\filer2sim', 'v', 'ws', 'win_b64')

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--level",
                        help="provide the tag name for incrementing snapshot. \
                              Ex: R419",
                        required=True)
    parser.add_argument("-d", "--directory",
                        help="provide the destination directory.")
    parser.add_argument("-f", "--framework",
                        help="provide the framework to copy be copied. \
                              valid arguments: sikuli|sahi|jmeter",
                        default="sikuli")
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity", action='store_true')
    args = parser.parse_args()

    # Init args
    tag_name = args.level
    destination_directory = args.directory
    framework = args.framework

    if not (framework.lower() == "sikuli" or framework.lower() == "sahi" or
            framework.lower() == "jmeter"):
        print("ERROR: Invalid string given with '-f' or '--framework'")
        sys.exit(1)

    # Set defaults and exceptions
    if tag_name is None:
        print("ERROR: Need --level e.g. R417 or R418 to proceed.")
        sys.exit(1)

    if args.verbose:
        print("INFO: --level {} used.".format(tag_name))

    if tag_name not in LEVELS_COPY_TO.keys():
        print("ERROR: given --level is not predefined.")
        sys.exit(1)

    # Figure out dirs to copy to and from / precheck
    if destination_directory is None:
        copy_to = os.path.join('D:\\', 'AutomaticTests',
                               LEVELS_COPY_TO[tag_name])
    else:
        copy_to = destination_directory

    try:
        scm_level = LEVELS_COPY_FROM[tag_name]
    except KeyError as why:
        print "ERROR: {} is invalid."
        sys.exit(1)
    # Find the location to copy from
    initial_path, snapshot = find_latest_snapshot_to_copy(
        tag_level=scm_level, dir_name=MAIN_SNAPSHOT_PATH)

    if framework.lower() == "sikuli":
        final_path = os.path.join(initial_path, scm_level,
                                  '{}_db'.format(
                                      scm_level),
                                      'SMASikUI.tst', 'FunctionTests',
                                      'InputData')

    if framework.lower() == "sahi":
        final_path = os.path.join(initial_path, scm_level,
                                  '{}_db'.format(
                                      scm_level), 'SMASahUI.tst',
                                      'FunctionTests',
                                      'InputData')

    if framework.lower() == "jmeter":
        final_path = os.path.join(initial_path, scm_level,
                                  '{}_db'.format(
                                      scm_level), 'SMAJmeter.tst',
                                      'FunctionTests',
                                      'InputData')
    if args.verbose:
        print("INFO: Code will be copied from {} to {}".format(final_path,
                                                               copy_to))

    # Prep before Copying
    now = datetime.datetime.now()
    robocopy_log = 'robocopy_' + tag_name + '_' + '_'.join(str(i) for
                                                           i in [now.month,
                                                                 now.day,
                                                                 now.hour,
                                                                 now.minute,
                                                                 now.second])
    command = ['robocopy', final_path, copy_to, '/MIR',
               '/LOG:{}.log'.format(os.path.join(os.environ.get('TMPDIR'),
               robocopy_log))]
    if args.verbose:
        print("INFO: Starting to copy the contents from {} to {}".format(
            final_path, copy_to))
        print("INFO: ROBOCOPY COMMAND: {}".format(' '.join(command)))

    # Copy Operations
    try:
        status = subprocess.call(command, shell=True)
        print("INFO: ROBOCOPY Exit Code: {}".format(str(status)))
        print("INFO: Robocopy Completed Successfully.")
        try:
            fname = os.path.join(copy_to, 'copy_successful.txt')
            fh = open(fname, 'w')
            fh.write("{}\n".format(snapshot))
            fh.close()
        except IOError, why:
            print("Unable to finalize the copy.")
            sys.exit()
    except WindowsError, err:
        print("ERROR: While copying from {} to {}: {}".format(
              final_path, copy_to, err))

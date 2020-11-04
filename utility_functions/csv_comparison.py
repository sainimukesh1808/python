import os
import csv
import sys
from datetime import datetime
import time


def csv_comparison(base_csv, new_csv, difference_csv_path, base_csv_path=None, new_csv_path=None):
    """This function compare two csv files.
    Args:
            base_csv (str) : name of reference csv file.
            new_csv (str) : name of new csv file.
            difference_csv_path : path for difference csv.
            base_csv_path : path of base csv file.
            new_csv_path ; path of new csv file.
    Returns:
            A csv file with differneces from both csv files.

    Example:
            csv_comparison('reference','new')"""

    try:
        with open(os.path.join(base_csv_path, base_csv + ".csv"), "r") as original:
            with open(os.path.join(new_csv_path, new_csv + ".csv"), "r") as new:
                fileone = original.readlines()
                filetwo = new.readlines()
                print("INFO: [" + time.strftime("%H:%M:%S") + "] Name of Reference csv file: " + base_csv)
                print("INFO: [" + time.strftime("%H:%M:%S") + "] Path of Reference csv file: " + base_csv_path)

                print("INFO: [" + time.strftime("%H:%M:%S") + "] Name of new csv file: " + new_csv)
                print("INFO: [" + time.strftime("%H:%M:%S") + "] Path of new csv file: " + new_csv_path)
    except Exception as e:
        print(e)

    tdate1 = datetime.today().strftime("%Y-%m-%d")
    tdate2 = time.time()
    tdate = str(tdate1) + str(tdate2)
    diff_csv = str(tdate) + ".csv"

    try:
        with open(os.path.join(difference_csv_path, diff_csv), "w") as outFile:
            print("INFO: [" + time.strftime("%H:%M:%S") + "] Name of difference csv file: " + diff_csv)
            print("INFO: [" + time.strftime("%H:%M:%S") + "] Path of difference csv file: " + difference_csv_path)
            for line in filetwo:
                if line not in fileone:
                    outFile.write(line)
    except Exception as e:
        print(e)

    with open(os.path.join(difference_csv_path, diff_csv), "r") as csvfile:
        csv_dict = [row for row in csv.DictReader(csvfile)]
        if len(csv_dict) == 0:
            print(
                "INFO: ["
                + time.strftime("%H:%M:%S")
                + "] CSV Comparison: Both CSV Files are same. Difference csv file is empty."
            )
            return True
        else:
            print("INFO: [" + time.strftime("%H:%M:%S") + "] CSV Comparison: Both CSV Files are different.")
            return False


def csv_comparison_on_specific_column(
    base_csv,
    new_csv,
    name_of_columns_to_compare,
    difference_csv_path,
    base_csv_path=None,
    new_csv_path=None,
):
    """This function compare two csv files.
    Args:
            base_csv (str) : name of reference csv file.
            new_csv (str) : name of new csv file.
            name_of_columns_to_compare(list) : list of columns to be compared
            difference_csv_path : path for difference csv.
            base_csv_path : path of base csv file.
            new_csv_path : path of new csv file.
    Returns:
            A csv file with differneces from both csv files.
    Example:
            csv_comparison_specific_column('reference','new',['column1','column2'])"""
    odt_path = systemPath.getLastBundlePath()
    tdate1 = datetime.today().strftime("%Y-%m-%d")
    tdate2 = time.time()
    tdate = str(tdate1) + str(tdate2)
    diff_csv = str(tdate) + ".csv"
    try:
        with open(os.path.join(base_csv_path, base_csv + ".csv"), "r") as original:
            with open(os.path.join(new_csv_path, new_csv + ".csv"), "r") as new:
                with open(os.path.join(difference_csv_path, name), "w") as difference:
                    print("INFO: [" + time.strftime("%H:%M:%S") + "] Name of Reference csv file: " + base_csv)
                    print("INFO: [" + time.strftime("%H:%M:%S") + "] Path of Reference csv file: " + base_csv_path)

                    print("INFO: [" + time.strftime("%H:%M:%S") + "] Name of Exported csv file: " + new_csv)
                    print("INFO: [" + time.strftime("%H:%M:%S") + "] Path of Reference csv file: " + new_csv_path)
                    for column in name_of_columns_to_compare:
                        original.seek(0)
                        new.seek(0)
                        header1 = next(original)
                        header2 = next(new)
                        if header1 == "sep=,\n":
                            csvObj1 = csv.DictReader(original)
                        else:
                            original.seek(0)
                            csvObj1 = csv.DictReader(original)
                        if header2 == "sep=,\n":
                            csvObj2 = csv.DictReader(new)
                        else:
                            new.seek(0)
                            csvObj2 = csv.DictReader(new)
                        for original_csv_line in csvObj1:
                            row1 = original_csv_line
                            val1 = original_csv_line[column]
                            for new_csv_line in csvObj2:
                                row2 = new_csv_line
                                val2 = new_csv_line[column]
                                break

                            if val1 != val2:
                                print(row2)
                                difference.write(val2 + "," + "\n")
                        difference.write(",")
    except Exception as e:
        print(e)

    with open(os.path.join(difference_csv_path, diff_csv), "r") as csvfile:
        csv_dict = [row for row in csv.DictReader(csvfile)]
        print("INFO: [" + time.strftime("%H:%M:%S") + "] Name of difference csv file: " + diff_csv)
        print("INFO: [" + time.strftime("%H:%M:%S") + "] Path of difference csv file: " + difference_csv_path)
        if len(csv_dict) == 0:
            print("INFO: [" + time.strftime("%H:%M:%S") + "] CSV Comparison: Both CSV Files are same.")
            print("INFO: CSV comparison is successful.")
            return True
        else:
            print("INFO: CSV comparison is Failed.")
            print("INFO: [" + time.strftime("%H:%M:%S") + "] CSV Comparison: Both CSV Files are different.")
            print("INFO: [" + time.strftime("%H:%M:%S") + "] Path of CSV difference file is : " + difference_csv_path)
            print("INFO: [" + time.strftime("%H:%M:%S") + "] Difference CSV file name : " + diff_csv)
            return False


def check_csv_data(file_name, file_path=None):
    try:
        with open(os.path.join(file_path, file_name + ".csv"), "r") as csvfile:
            csv_dict = [row for row in csv.DictReader(csvfile)]
            print("INFO: [" + time.strftime("%H:%M:%S") + "] file path: " + file_path)
            if len(csv_dict) == 0:
                msg = "INFO: [" + time.strftime("%H:%M:%S") + "] CSV file is empty."
                raise Exception(msg)
            else:
                print("INFO: [" + time.strftime("%H:%M:%S") + "] CSV file has data.")
    except Exception as e:
        print(e)

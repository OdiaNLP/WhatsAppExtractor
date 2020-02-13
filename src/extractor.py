"""
Author: Soumendra Kumar Sahoo
Date: 13th Feb 2020

Usage:
    python extractor.py -i <path/input_filename.txt>
    or
    python extractor.py -i <path/input_filename.txt> -o <path/output_filename.csv>

Default output report path: data/report_file.csv
"""
import argparse
import csv
import os
import re
import sys
from collections import defaultdict, Counter

from patterns import (  date_pattern,
                        time_pattern,
                        name_pattern,
                        msg_pattern,
                        checking_pattern,
                        count_pattern,
                        DIGIT_MAP)


col_keys = ["names", "dates", "times", "messages", "counts"]


def read_export_file(export_file: str):
    """
    Read the file content
    input: Whatsapp file
    output: list of content splitted by line
    """
    with open(export_file, encoding='utf-8') as inp_file:
        content = inp_file.readlines()
    return content


def substitute_odia_digits(text: str):
    """
    substitute Odia digits with English for easier visualization
    without affecting Odia lovers
    """
    substituted_text = ''
    for letter in text:
        substituted_text += DIGIT_MAP.get(letter, letter)
    return substituted_text


def process_file(content: list):
    """
    reads each line of the file one after another and prepares the report file
    """
    temp_dict = defaultdict(list)
    csv_list = []
    for cnt, line in enumerate(content):
        # Iterates over each line of the file
        if re.findall(date_pattern, line.strip()):
            # if date found in a line, consider it as a new message
            if len(temp_dict) == len(col_keys) and \
                re.findall(checking_pattern, ''.join(temp_dict.get('messages'))):
                # if all values of the csv columns are present then only append 
                # into the report file
                csv_list.append(temp_dict)
            temp_dict = {}
            temp_dict["names"] = ''.join(re.findall(name_pattern, line.strip()))
            # Check who sent the message
            if temp_dict["names"]:
                temp_dict["dates"] = ''.join(re.findall(date_pattern, line.strip()))
                temp_dict["times"] = ''.join(re.findall(time_pattern, line.strip()))
                temp_dict["messages"] = ''.join(re.findall(msg_pattern, line.lower().strip()))
                temp_dict["counts"] = substitute_odia_digits(''.join(re.findall(count_pattern, 
                                                                line.lower().strip())))
        else:
            # if date not found, consider it as a continuation of prev line
            temp_dict["messages"] += ' ' + line.strip() # add to prev line message
            temp_dict["counts"] = substitute_odia_digits(''.join(re.findall(count_pattern,
                                                            line.strip())))
    return csv_list


def write_extract_file(output_filename: str, csv_list: list, col_keys: list):
    """
    Write the extracted content into the file
    """
    with open(output_filename, 'w+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=col_keys)
        writer.writeheader()
        writer.writerows(csv_list)


def main():
    parser = argparse.ArgumentParser(description='Whatsapp extractor')
    parser.add_argument('-i','--input', help='Input Whatsapp chat export filename',required=True)
    parser.add_argument('-o','--output',help='Output report csv filename', default='../data/report_file.csv')
    args = parser.parse_args()
 
    input_filename = args.input
    output_filename = args.output

    file_content = read_export_file(input_filename)
    csv_list = process_file(file_content)
    write_extract_file(output_filename, csv_list, col_keys)


if __name__ == '__main__':
    main()

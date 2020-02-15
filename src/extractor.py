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
                        message_pattern,
                        checking_pattern,
                        count_pattern,
                        DIGIT_MAP)


columns = dict([("names", name_pattern), 
                ("dates", date_pattern),
                ("times", time_pattern), 
                ("messages", message_pattern), 
                ("counts", count_pattern)])


def check_file_existence(func):
    def file_exists(*args):
        if not os.path.isfile(args[0]):
            raise FileNotFoundError(f'The input file: "{args[0]}" does not exist')
        return func(*args)
    return file_exists


@check_file_existence
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


def extract_patterns(line: str):
    """Extracts the patterns present in the line
    
    Arguments:
        line {str} -- contains one individual line
    """
    temp_dict = {}
    for column_name, pattern in columns.items():
        temp_dict[column_name] = ''.join(re.findall(pattern, line))
        if column_name == 'counts':
            temp_dict[column_name] = substitute_odia_digits(temp_dict[column_name])
    return temp_dict


def process_file(content: list):
    """
    reads each line of the file one after another and prepares the report file
    """
    temp_dict = defaultdict(list)
    csv_list = []
    for line in content:
        # Iterates over each line of the file
        if re.findall(date_pattern, line.strip()):
            # if date found in a line, consider it as a new message
            if len(temp_dict) == len(columns) and \
                re.findall(checking_pattern, ''.join(temp_dict.get('messages'))):
                # if all values of the csv columns are present then only append 
                # into the report file
                csv_list.append(temp_dict)
            temp_dict = extract_patterns(line.lower().strip())
        else:
            # if date not found, consider it as a continuation of prev line
            temp_dict["messages"] += ' ' + line.strip() # add to prev line message
            if 'counts' in columns.keys():
                temp_dict["counts"] = substitute_odia_digits(''.join(re.findall(count_pattern,
                                                                line.strip())))
    return csv_list


def write_extract_file(output_filename: str, csv_list: list, col_keys: list):
    """
    Write the extracted content into the file
    """
    with open(output_filename, 'w+') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=columns.keys())
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
    write_extract_file(output_filename, csv_list, columns.keys())


if __name__ == '__main__':
    main()

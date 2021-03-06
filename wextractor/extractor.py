"""
Author: Soumendra Kumar Sahoo
Date: 13th Feb 2020
"""
import argparse
import csv
import os
import re
from collections import defaultdict

from .patterns import (
    date_pattern,
    time_pattern,
    name_pattern,
    message_pattern,
    checking_pattern,
    count_pattern,
    DIGIT_MAP,
)

columns = dict(
    [
        ("names", name_pattern),
        ("dates", date_pattern),
        ("times", time_pattern),
        ("messages", message_pattern),
        ("counts", count_pattern),
    ]
)


def substitute_odia_digits(text: str):
    """
    substitute Odia digits with English for easier visualization
    without affecting Odia lovers
    """
    substituted_text = ""
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
        temp_dict[column_name] = "".join(re.findall(pattern, line))
        if column_name == "counts":
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
            if len(temp_dict) == len(columns) and re.findall(
                checking_pattern, "".join(temp_dict.get("messages"))
            ):
                # if all values of the csv columns are present then only append
                # into the report file
                csv_list.append(temp_dict)
            temp_dict = extract_patterns(line.lower().strip())
        else:
            # if date not found, consider it as a continuation of prev line
            temp_dict["messages"] += " " + line.strip()  # add to prev line message
            if "counts" in columns.keys():
                temp_dict["counts"] = substitute_odia_digits(
                    "".join(re.findall(count_pattern, line.strip()))
                )
    return csv_list


def write_extract_file(output_filename: str, csv_list: list):
    """
    Write the extracted content into the file
    """
    try:
        with open(output_filename, "w+") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=columns.keys())
            writer.writeheader()
            writer.writerows(csv_list)
    except FileNotFoundError:
        print("Output file not present", output_filename)
        print("Current dir: ", os.getcwd())
        raise FileNotFoundError

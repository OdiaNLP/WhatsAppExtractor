"""
Author: Soumendra Kumar Sahoo
Date: 2nd March 2020
"""
import os
import sys
from unittest import mock

from pytest import fixture, mark

from wextractor.extractor import (
    extract_patterns,
    main,
    process_file,
    read_export_file,
    substitute_odia_digits,
    write_extract_file,
)


@fixture
def get_file_content():
    file_path = "tests/mock_file.txt"
    with open(file_path, encoding="utf-8") as inp_file:
        content = inp_file.readlines()
    return content


class TestExtractor:
    """Test the extractor module
    """

    file_path = "tests/mock_file.txt"
    wrong_file_path = "tests/file_does_not_exist.txt"

    def test_read_export_file_happy(self):
        """open the file content and match the content

        Arguments:
            test_filename {str} -- filename
        """
        with open(self.file_path, "r+", encoding="utf-8") as mf:
            mock_content = mf.readlines()
        read_content = read_export_file(self.file_path)
        assert read_content == mock_content

    def test_read_export_file_sad(self):
        """open the file content and match the content

        Arguments:
            test_filename {str} -- filename
        """
        try:
            read_export_file(self.wrong_file_path)
        except FileNotFoundError:
            assert True

    def test_substitute_odia_digits(self):
        """tests the odia digit substitution
        """
        sample_inputs = ("COVID-୧୯", "୦୧୨୩୪୫୬୭୮୯୦", "  121୦୧୨୩  45୪୫୬୭୮୯୦3435 ", "୦m")
        exp_outputs = ("COVID-19", "01234567890", "  1210123  4545678903435 ", "0m")
        for cnt in range(len(sample_inputs)):
            assert exp_outputs[cnt] == substitute_odia_digits(sample_inputs[cnt])

    def test_extract_patterns(self, get_file_content):
        """Test the extract patterns in the input line
        """
        exp_response = [
            {
                "names": "+91 12345 67890",
                "dates": "2/28/20",
                "times": "10:32 PM",
                "messages": " QWSER: Checking In",
                "counts": "",
            },
            {
                "names": "Don MTE2O",
                "dates": "2/29/20",
                "times": "12:13 AM",
                "messages": " Looks good to me , ",
                "counts": "",
            },
            {"names": "", "dates": "", "times": "", "messages": "", "counts": ""},
            {
                "names": "+91 12345 67890",
                "dates": "2/29/20",
                "times": "12:13 AM",
                "messages": " 😊",
                "counts": "",
            },
            {
                "names": "+91 12345 67890",
                "dates": "2/29/20",
                "times": "12:15 AM",
                "messages": " Checking Out: tweet count: 8568",
                "counts": "8568",
            },
            {
                "names": "Don MTE2O",
                "dates": "2/29/20",
                "times": "8:24 AM",
                "messages": " Don : Checking IN",
                "counts": "",
            },
            {
                "names": "Don MTE2O",
                "dates": "2/29/20",
                "times": "8:45 AM",
                "messages": " Don: Checking OUT",
                "counts": "",
            },
        ]
        for cnt in range(len(get_file_content)):
            assert exp_response[cnt] == extract_patterns(get_file_content[cnt])

    def test_process_file(self, get_file_content):
        """test the entire process
        """
        exp_res = [
            {
                "names": "+91 12345 67890",
                "dates": "2/28/20",
                "times": "10:32 pm",
                "messages": " qwser: checking in",
                "counts": "",
            },
            {
                "names": "don mte2o",
                "dates": "2/29/20",
                "times": "12:13 am",
                "messages": " looks good to me , Thanks QWSER checking in",
                "counts": "",
            },
            {
                "names": "+91 12345 67890",
                "dates": "2/29/20",
                "times": "12:15 am",
                "messages": " checking out: tweet count: 8568",
                "counts": "8568",
            },
            {
                "names": "don mte2o",
                "dates": "2/29/20",
                "times": "8:24 am",
                "messages": " don : checking in",
                "counts": "",
            },
        ]
        assert exp_res == process_file(get_file_content)

    def test_write_extract_file(self, get_file_content):
        """test the report writing process
        """
        output_file_name = "tests/test_write.csv"
        csv_list = [
            {
                "names": "+91 12345 67890",
                "dates": "2/28/20",
                "times": "10:32 pm",
                "messages": " qwser: checking in",
                "counts": "",
            },
            {
                "names": "+91 12345 67890",
                "dates": "2/29/20",
                "times": "12:15 am",
                "messages": " checking out: tweet count: 8568",
                "counts": "8568",
            },
            {
                "names": "don mte2o",
                "dates": "2/29/20",
                "times": "8:24 am",
                "messages": " don : checking in",
                "counts": "",
            },
        ]
        write_extract_file(output_file_name, csv_list)
        assert os.path.isfile(output_file_name)

    def test_main(self):
        """test the main function of the extractor module
        """
        sys.argv[1:] = ["-i", "tests/mock_file.txt", "-o", "tests/test_write.csv"]
        main()

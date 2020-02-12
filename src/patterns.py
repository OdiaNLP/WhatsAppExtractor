"""
Author: Soumendra Kumar Sahoo
Date: 13th Feb 2020
"""
import re

date_pattern = re.compile(r"^\d{1,2}/\d{1,2}/\d{1,2}")
time_pattern = re.compile(r"\d{1,2}:\d{1,2}\s[AP]M")
name_pattern = re.compile(r"(?<=-\s).*?(?=\:)")
msg_pattern = re.compile(r"(?<=\:)\s.*", flags=re.IGNORECASE)
checking_pattern = re.compile(r"(?<=[:\s])(Checking|ଚେକିଂ)", flags=re.IGNORECASE)
count_pattern = re.compile(r"[୧୨୩୪୫୬୭୮୯୦\d]+$", flags=re.UNICODE)
DIGIT_MAP = {
    "୧":"1",
    "୨":"2",
    "୩":"3",
    "୪":"4",
    "୫":"5",
    "୬":"6",
    "୭":"7",
    "୮":"8",
    "୯":"9",
    "୦":"0"
}
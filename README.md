[![Build Status](https://travis-ci.com/MTEnglish2Odia/WhatsAppExtractor.svg?branch=master)](https://travis-ci.com/MTEnglish2Odia/WhatsAppExtractor)
[![codecov](https://codecov.io/gh/MTEnglish2Odia/WhatsAppExtractor/branch/master/graph/badge.svg)](https://codecov.io/gh/MTEnglish2Odia/WhatsAppExtractor)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# WhatsAppExtractor
Extracts necessary contents from a WhatsApp chat-export.  
## Prerequisites
- Please see the [Whatsapp FAQ](https://faq.whatsapp.com/en/android/23756533), if you want to know how to export chat conversations on whatsapp.
- Python >= 3.6 


## Usage:
```
python -m extractor.py -i <path/input_filename.txt>
```
or  
```
python -m extractor.py -i <path/input_filename.txt> -o <path/output_filename.csv>
```
Default output report path: data/report_file.csv

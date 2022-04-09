# Log_Search_Date

[![Build Status](https://github.com/APOSHAml/Log_Search_Date/actions/workflows/pytest-package.yml/badge.svg?branch=master)](https://github.com/APOSHAml/Log_Search_Date/actions/workflows/pytest-package.yml)

Requirements: Python 3.10 or higher;
pre-execute commands:
python -m pip install --upgrade pip;
pip install click==8.0.4


Usage: FindLogger.py [OPTIONS] PATH

  This MEGAscript find logs according to the given parametrs

Options:
  -t, --text, --Text, --TEXT TEXT
                                  To find the text in the Logs
  -d, --date, --Date, --DATE TEXT
                                  To find the date in the Logs
  -n, --unwanted, --Unwanted, --UNWANTED TEXT
                                  A text to filter out logs. Logs with this
                                  text will be excluded from the results.
  --full, --Full, --FULL TEXT     Return full log entry unstead of default Qty
  --help                          Show this message and exit.

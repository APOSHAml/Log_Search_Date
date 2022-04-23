# Log_Search_Date

[![Build Status](https://github.com/APOSHAml/Log_Search_Date/actions/workflows/pytest-package.yml/badge.svg?branch=master, main)](https://github.com/APOSHAml/Log_Search_Date/actions/workflows/pytest-package.yml)

* ___Requirements: Python 3.10 or higher___
* pre-execute commands:

```
python -m pip install --upgrade pip
pip install click==8.0.4
```

___Usage: FindLogger.py [OPTIONS] PATH___

  _This MEGAscript find logs according to the given parametrs_

* _Options:_
___
  __-t, --text, --Text, --TEXT TEXT__
  ___
    To find the text in the Logs
___
  __-d, --date, --Date, --DATE TEXT__
  ___
    To find the date in the Logs.The Example:"2022-02-03 00:01:13.623", or less "../2022-02-03 00:01:13.623", or more "2022-02-03 00:01:13.623\..", or range "2022-02-03 00:01:13.623/2022-02-03 00:01:13.623/2022-02-03 00:06:13.838".
  __-n, --unwanted, --Unwanted, --UNWANTED TEXT__
  ___
    A text to filter out logs. Logs with this
    text will be excluded from the results.
  __--full, --Full, --FULL TEXT__ 
  ___
    Return full log entry unstead of default Qty. Example -full FULL, --Full full and etc.
  __--help__
  ___
    Show this message and exit.

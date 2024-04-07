# Reconr - Records Reconcilation Tool

Reconr compares two records to find missing values and discrapancies.

## Features

1. Find missing records from both records.
2. Find discrapancies or inconsistencies in records.
3. Select what columns should be considered in the reconcilation.
4. Apply Fuzzy matching for non-identical but similar records.

## How to run

1. Download and install Python 3. (Python 3.10 and above is recommended)
2. Optionally, set up a virtual environment with venv `python -m venv venv`
3. If you set up a virtual environment, activate it with `source venv/bin/activate` on linux / Mac or `.\venv\Scripts\activate.bat` on Windows
4. Install the requirements with `pip install -r requirements.txt`
5. You can run the command line tool with `python -m reconr <source-filename> <target-filename>`
6. You can also configure which columns should be included in the search. e.g `python -m reconr <source-filename> <target-filename> --headers Date --headers Amount`
7. You can also view the full list of possible commands with `python -m reconr --help`.

## Note
To run the above commands, your terminal / command prompt should be pointing to the directory containing the reconr folder (not inside the reconr folder).


from typing import (
    List,
    Dict,
    Tuple,
    Union
)

import sys
import os
import re

import logging

from datetime import (
    date
)

import csv

from fuzzywuzzy import fuzz


def is_date(string: str) -> bool:

    year_last = r'\d{1,2}(\/|\-)\d{1,2}(\/|\-)\d{2,4}'

    year_first = r'\d{2,4}(\/|\-)\d{1,2}(\/|\-)\d{1,2}'

    return re.fullmatch(year_last, string) or re.fullmatch(year_first, string)


def is_number(string: str) -> bool:
    """
        Uses regular expressions to check if 
        string is a number (int or float)
    """

    return re.fullmatch(r'[+-]?([0-9]*[.])?[0-9]+', string)


def transform_value(
    string: str,
    is_case_sensitive: bool
) -> Union[float, date, str]:

    """
        Function transforms string to it's appropriate format
    """

    string = string.strip()

    if is_number(string):
        return float(string)

    if is_date(string):
        return date.fromisoformat(string)

    if not is_case_sensitive:
        string = string.lower()

    return string


def read_csv(
    fp: str,
    is_case_sensitive: bool,
    headers: List[str] = None,
) -> Dict[str, Dict[str, Union[str, int, date]]]:

    """
        Function Reads a CSV file into memory

        assumes the first row is the header column
        assumes the first column is the 'id'.

        for each field, this function will identify it's datatype
        as one of (string, number, date) and transform it appropriately.

        Args:
            fp (str): file path of the CSV to read

        returns:
            Mapping of id to a column->value Mapping
            for easy comparison and querying.
    """

    try:
        result = {}

        with open(fp, newline='') as csvfile:

            reader = csv.reader(csvfile, delimiter=',')

            # All headers except ID (first col)
            file_headers = next(reader)[1:]

            for row in reader:

                rowID = row[0]

                result[rowID] = {
                    key: transform_value(value, is_case_sensitive)
                    for (key, value) in zip(file_headers, row[1:])
                    if headers is None or key in headers
                }

        return result

    except FileNotFoundError:

        logging.error("We could not find the file %s. Please provide a different path", fp)

        return None
    except UnicodeDecodeError:

        logging.error("File %s is not a valid CSV File! Only CSV files are supported", fp)


def find_missing_records(records_a: dict, records_b: dict) -> Tuple[list, list]:
    """
        Function checks the records to see which ones are missing
        it does this by comparing the IDs in both records.
        
        Args:
            records_a (dict): first set of records 
            records_b (dict): second set of records

        Returns:
            
            Tuple containing the set of records missing from a and b.
            e.g ([003, 004], [001, 005, 009, 010])

    """

    missing_in_a = records_b.keys() - records_a.keys()
    missing_in_b = records_a.keys() - records_b.keys()

    return (missing_in_a, missing_in_b)


def find_discrapancies(
    records_a: dict,
    records_b: dict,
    use_fuzzy: bool = False,
    threshold: int = 60
) -> List[tuple]:
    """
        Function checks the records to see which ones have different
        values for their fields.

        Args:
            records_a (dict): first set of records
            records_b (dict): second set of records

        Returns:

            List of tuples.
            each tuple contains the ID, field, and values in records A and B
    """

    result = []

    ids = {*records_a.keys(), *records_b.keys()}

    for rid in ids:

        # It's missing, we've already captured this
        if not (rid in records_a and rid in records_b):
            continue

        keys = {*records_a[rid].keys(), *records_b[rid].keys()}

        for key in keys:

            value_in_a = records_a[rid].get(key)
            value_in_b = records_b[rid].get(key)

            if isinstance(value_in_a, str) and use_fuzzy:
                score = fuzz.ratio(value_in_a, value_in_b)
            else:
                score = int(value_in_a == value_in_b) * 100

            if score < threshold:
                result.append((rid, key, value_in_a, value_in_b))

    return result


def write_to_csv(
    out_fn: str,
    missing_values: Tuple[list, list],
    discrapancies: list
):

    """
        Function packages the missing values and discrapancies
        and writes to a CSV file

        Args:
            out_fn (str): What we should name the output file
            missing_values (tuple): result of find_missing_records
            discrapancies (list): result of find_discrapancies
    """

    headers = [
        'Type',
        'Record Identifier',
        'Field',
        'Source Value',
        'Target Value'
    ]

    rows = []

    missing_in_source, missing_in_target = missing_values

    rows += [
        ['Missing in Source', x, '', '', '']
        for x in missing_in_source
    ]

    rows += [
        ['Missing in Target', x, '', '', '']
        for x in missing_in_target
    ]

    rows += [
        ['Field Discrapancy', *discrapancy]
        for discrapancy in discrapancies
    ]

    with open(out_fn, "w", newline='') as csvfile:

        writer = csv.writer(csvfile, delimiter=',')

        writer.writerow(headers)

        for row in rows:

            writer.writerow(row)

#!/bin/python3

import argparse
import re
import sys
from dataclasses import dataclass, field

import numpy as np
import pandas as pd


@dataclass
class Variable:
    """
    Variable object is used to store data from files as well
    as metadata useful for further data manipulation.

    Variable object contains data read from file which
    will become a column, column name, and size of an
    array to be read.

    ---

    Parameters:

    input_path: Path to file containing matrix-like data.

    col_name: Name of the column. If col_name is not defined
    then file name is used to create col_name.

    data: Is a list containing data from the matrix. It is
    sorted in the following order: A1, B1, C1 ... A5, B5, C5 etc.

    size: Is None by default. To set size use a string formatted
    like excel range eg. A1:C5. It works exactly like one would
    expect in excel.
    """
    input_path: str = field(repr=False)
    col_name: str = field(repr=False)
    data: list = field(init=False)
    size: list = field(repr=False)

    def __post_init__(self):
        # reading data from path
        self.data = read_data(self.input_path,
                              self.size)


def read_data(input_path: str, size) -> list:
    """
    TODO
    """
    # checking extensions
    filetype = input_path.split(".")[-1]
    if filetype == "xlsx" or filetype == "xls" or filetype == "ods":
        df = pd.read_excel(input_path, header=None)
    elif filetype == "csv":
        df = pd.read_csv(input_path, sep=",", header=None)
    elif filetype == "tsv":
        df = pd.read_csv(input_path, sep="\t", header=None)
    else:
        raise TypeError(f"""
                        Format is {filetype} not supported
                        You may want to use:
                        csv
                        tsv
                        xlsx
                        xls
                        ods
                        """)
    array = np.asarray(df)
    resized = resize(array, size)
    col = make_col(resized)
    return col


def resize(array, size):
    """
    Resize your array.
    TODO
    """
    if size is None:
        # default microplate reader (12x8)
        resized = array[-8:, -12:]
        return resized
    else:
        size = size[0]
        if size.count(":") == 1:
            cols = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            start = size.split(":")[0]
            end = size.split(":")[-1]

            start_column_code = re.findall("[A-Z]", start)
            end_column_code = re.findall("[A-Z]", end)

            start_col_idx = len(cols) * \
                (len(start_column_code) - 1) + \
                cols.find(start_column_code[-1])

            end_col_idx = len(cols) * \
                (len(end_column_code) - 1) + \
                cols.find(end_column_code[-1]) + 1

            start_row_idx = int("".join(re.findall("[0-9]", start))) - 1
            end_row_idx = int("".join(re.findall("[0-9]", end)))

            resized = array[start_row_idx:end_row_idx,
                            start_col_idx:end_col_idx]
            if list(resized):
                return resized
            else:
                raise ValueError(f"Range {size} returns an empty array.")
        else:
            raise ValueError(f"""Range {size} not supported. Please use
                            Excel style range format (eg. A1:C5).""")


def make_col(array) -> list:
    """
    Transforms data array into list.
    """
    # array to list
    col = []
    for row in array:
        for val in row:
            col.append(val)
    return col


def make_table(var_list: list, output_path: str):
    """
    Makes csv table from list of variables and var names.
    TODO
    """
    columns = {}
    for var in var_list:
        columns[var.col_name] = var.data
    table = pd.DataFrame(columns).astype(str)
    table.to_csv(output_path, index=False)


def run(args):
    """
    Runs the whole program.
    TODO
    """
    # assign args to variables
    input_paths = args.input
    output_path = args.output

    # make var_names
    if args.colnames:
        col_names = args.colnames
    else:
        col_names = []
        for i in input_paths:
            name = i.split("/")[-1].split(".")[0]
            col_names.append(name)

    # suplement var_names if needed
    if len(input_paths) > len(col_names):
        for i in input_paths[len(col_names):]:
            name = i.split("/")[-1].split(".")[0]
            col_names.append(name)

    # make list of Variable objects
    var_list = []
    for idx, _ in enumerate(input_paths):
        var = Variable(input_path=input_paths[idx],
                       col_name=col_names[idx],
                       size=args.size)
        var_list.append(var)

    make_table(var_list, output_path)


def argument_parser(args):
    """
    CLI argument parser.
    """
    parser = argparse.ArgumentParser(
        description="""Convert a list of csv or excel files
        containing matrices to a csv table."""
    )
    parser.add_argument(
        "-in",
        help="path(s) to matrix containing file(s)",
        dest="input",
        type=str,
        required=True,
        nargs="+",
    )
    parser.add_argument(
        "-out",
        help="path to an output file",
        dest="output",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-cols",
        help="""Column names from left to right.
        If not provided, filenames become colnames.""",
        dest="colnames",
        type=str,
        nargs="*",
    )
    parser.add_argument(
        "-size",
        help="""Adjust size of all arrays using
        excel style ranges (eg. A1:B2).""",
        dest="size",
        type=str,
        nargs="*"
    )
    return parser.parse_args(args)


def main():
    args = argument_parser(sys.argv[1:])
    run(args)


if __name__ == "__main__":
    main()

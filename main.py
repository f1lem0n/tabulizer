#!/bin/python3

import argparse
from dataclasses import dataclass, field

import numpy as np
import pandas as pd


@dataclass
class Variable:
    """
    TODO
    """
    input_path: str = field(repr=False)
    var_name: str = field(repr=False)
    data: list = field(init=False)

    def __post_init__(self):
        # reading data from path
        self.data = read_data(self.input_path)


def read_data(input_path: str) -> list:
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

    # trimming the array
    array = np.asarray(df)
    trimmed = array[-8:, -12:]

    # array to list
    col = []
    for row in trimmed:
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
        columns[var.var_name] = var.data
    table = pd.DataFrame(columns)
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
        var_names = args.colnames
    else:
        var_names = []
        for i in input_paths:
            name = i.split("/")[-1]
            var_names.append(name)

    # suplement var_names if needed
    if len(input_paths) > len(var_names):
        for i in input_paths[len(var_names):]:
            name = i.split("/")[-1].split(".")[0]
            var_names.append(name)

    # make list of Variable objects
    var_list = []
    for idx, _ in enumerate(input_paths):
        var = Variable(input_path=input_paths[idx],
                       var_name=var_names[idx])
        var_list.append(var)

    make_table(var_list, output_path)


def main():
    # argument parser
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
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

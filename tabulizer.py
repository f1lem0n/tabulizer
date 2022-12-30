#!/bin/python3

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
import argparse


@dataclass
class Variable:
    input_path: str = field(repr=False)
    var_name: str = field(repr=False)
    unit: str = field(repr=False, default="")
    header: str = field(init=False)
    data: list = field(init=False)

    def __post_init__(self):

        # make header
        if self.unit != "":
            self.header = f"{self.var_name}.{self.unit}"
        else:
            self.header = self.var_name

        # reading data from path
        self.data = read_data(self.input_path)


def read_data(input_path: str):
    # checking extensions
    filetype = input_path.split(".")[-1]
    if filetype == "xlsx" or filetype == "xls" or filetype == "ods":
        df = pd.read_excel(input_path, header=None)
    elif filetype == "csv":
        df = pd.read_csv(input_path, sep=",", header=None)
    elif filetype == "tsv":
        df = pd.read_csv(input_path, sep="\t", header=None)
    else:
        print("Filetype not supported.")
        print("Supported filetypes: xlsx, xls, ods, csv, tsv.")
        sys.exit()

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
    columns = {}
    for var in var_list:
        columns[var.header] = var.data
    table = pd.DataFrame(columns)
    table.to_csv(output_path, index=False)


def run(args):
    # assign args to variables
    input_paths = args.input
    output_path = args.output
    units = args.units

    # make var_names
    if args.colnames:
        var_names = args.colnames
    else:
        var_names = []
        for i in input_path:
            name = i.split("/")[-1]
            var_names.append(name)

    # suplement var_names if needed
    if len(input_paths) > len(var_names):
        var_names += input_paths[len(var_names):]

    # make units
    if len(input_paths) > len(units):
        nempty = len(input_paths) - len(units)
        for i in range(nempty):
            units.append("")

    # make list of Variable objects
    var_list = []
    for idx, _ in enumerate(input_paths):
        var = Variable(
            input_path = input_paths[idx],
            var_name = var_names[idx],
            unit = units[idx]
        )
        var_list.append(var)

    make_table(var_list, output_path)


def main():
    # argument parser
    parser = argparse.ArgumentParser(
        description = "Convert a list of csv or excel files containing matrices to a csv table."
    )
    parser.add_argument(
        "-in",
        help = "path to matrix containing file(s) from left to right",
        dest = "input",
        type = str,
        required = True,
        nargs = "+"
    )
    parser.add_argument(
        "-out",
        help = "path to an output file",
        dest = "output",
        type = str,
        required = True
    )
    parser.add_argument(
        "-cols",
        help =  "Column names from left to right. If not provided, filenames become colnames.",
        dest = "colnames",
        type = str,
        nargs = "*"
    )
    parser.add_argument(
        "-units",
        help =  "Units from left to right (optional).",
        dest = "units",
        type = str,
        nargs = "*"
    )
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()

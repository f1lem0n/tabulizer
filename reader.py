from dataclasses import dataclass, field

import numpy as np
import pandas as pd


@dataclass
class Variable:
    input_path: str = field(repr=False)
    var_name: str = field(repr=False)
    # var_type: str = field(repr=False)
    unit: str = field(repr=False, default="")
    header: str = field(init=False)
    data: list = field(init=False)

    def __post_init__(self):

        # checking for NOIR type
        # if self.var_type not in ["N", "O", "I", "R"]:
            # print("Incorrect variable type. Choose one of these: N, O, I, R.")

        # construction of a header
        # if self.var_type in ["I", "R"] and
        if self.unit != "":
            self.header = f"{self.var_name} [{self.unit}]"
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


var_list = [
    Variable(
        var_name = "absorbance",
        unit = "RU",
        input_path = "data/2021.12.13.xlsx"
    ),
    Variable(
        var_name = "column",
        input_path = "data/template1.ods"
    )
]

quit
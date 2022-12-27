from dataclasses import dataclass, field
import sys

import numpy as np
import pandas as pd


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

def gen_id():
    return "".join("TWOJA STARA")

@dataclass
class Variable:
    input_path: str = field(repr=False)
    var_name: str = field(repr=False)
    var_type: str 
    unit: str = field(repr=False, default="")
    header: str = field(init=False)
    data: list = field(init=False)
    column: dict = field(init=False, repr=False)
    
    def __post_init__(self):
        # checking for NOIR type
        if self.var_type not in ["N", "O", "I", "R"]:
            print("Incorrect variable type. Choose one of these: N, O, I, R.")
            sys.exit()

        # checking for unit
        if self.var_type in ["I", "R"] and self.unit != "":
            self.header = f"{self.var_name} [{self.unit}]"
        else:
            self.header = self.var_name
            
        self.data = read_data(self.input_path)
        self.column = {self.header: self.data}
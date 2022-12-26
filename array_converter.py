import sys

import numpy as np
import pandas as pd


def read_file(input_path: str):
    
    # checking extensions
    filetype = file.split(".")[-1]
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
    ordered = []
    for row in trimmed:
        for val in row:
            ordered.append(val)
    
    return ordered


def make_col(file: str, var_name: str, var_type: str, unit: str=""):
    
    # checking for NOIR type
    if var_type not in ["N", "O", "I", "R"]:
        print("Incorrect variable type.")
        sys.exit()
        
    # checking for unit
    if var_type in ["I", "R"] and unit != "":
        header = f"{var_name} [{unit}]"
    else:
        header = var_name
    
    # creating the final list
    t = [header, f"var_type:{var_type}"]
    ordered = read_file(file)
    defined = t + ordered
    
    return defined


def make_table(*col: list, output_path: str):
    
    columns = {}
    for c in col:
        columns[c[0]] = c[1:]
    table = pd.DataFrame(columns)
    table.to_csv(output_path, index=False)
                
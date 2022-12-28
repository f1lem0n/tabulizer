from reader import Variable
import subprocess

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

print("----------------")
print("Variables added:")
for var in var_list:
    print(var.header)
print("----------------")

subprocess.call("Rscript calc.R", shell=True)

import os
import curses

# W I P
var_list = []
undone = True
while undone:
    input_path = input("path to file: ")
    var_name = input("variable name: ")
    unit = input("unit (optional): ")
    var = Variable(
        input_path = input_path,
        var_name = var_name,
        unit = unit
    )
    var_list.append(var)

print(var_list)

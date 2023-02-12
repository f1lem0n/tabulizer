import os

import tabulizer.main as main

output = "sample_output/table.csv"
input = "sample_data/random2.csv"


class TestMakeTable():

    def test_make_table(self):
        file_exists = os.path.exists(output)
        if file_exists:
            os.remove(output)
        var_list = [main.Variable(input_path=input,
                                  var_name="SpanishInquisition")]
        main.make_table(var_list, output)
        file_exists = os.path.exists(output)
        assert file_exists
        with open(output) as f:
            tab = f.readlines()
            assert len(tab) == 97

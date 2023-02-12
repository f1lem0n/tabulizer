import argparse
import os

import tabulizer.main as main

inputs = ["sample_data/random2.csv",
          "sample_data/random3.tsv",
          "sample_data/random1.xls"]
colnames = ["The",
            "Holy",
            "Grail"]


class TestRun():

    def test_run_unnamed_cols(self):
        output = "sample_output/multicol_unnamed.csv"
        file_exists = os.path.exists(output)
        if file_exists:
            os.remove(output)
        args = argparse.Namespace(input=inputs,
                                  output=output,
                                  colnames=None,
                                  func=main.run)
        main.run(args)
        file_exists = os.path.exists(output)
        assert file_exists
        with open(output) as f:
            rows = f.readlines()
        for row in rows:
            assert row.count(",") == len(inputs) - 1

    def test_run_named_cols(self):
        output = "sample_output/multicol_named.csv"
        file_exists = os.path.exists(output)
        if file_exists:
            os.remove(output)
        args = argparse.Namespace(input=inputs,
                                  output=output,
                                  colnames=colnames,
                                  func=main.run)
        main.run(args)
        file_exists = os.path.exists(output)
        assert file_exists
        with open(output) as f:
            rows = f.readlines()
        for row in rows:
            assert row.count(",") == len(inputs) - 1

    def test_run_partially_named_cols(self):
        output = "sample_output/multicol_part.csv"
        file_exists = os.path.exists(output)
        if file_exists:
            os.remove(output)
        args = argparse.Namespace(input=inputs,
                                  output=output,
                                  colnames=colnames[:2],
                                  func=main.run)
        main.run(args)
        file_exists = os.path.exists(output)
        assert file_exists
        with open(output) as f:
            rows = f.readlines()
        for row in rows:
            assert row.count(",") == len(inputs) - 1

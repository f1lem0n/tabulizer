import argparse
import os

import pytest

import tabulizer.main as main

arglist_unnamed = ['-in',
                   'sample_data/random1.xls',
                   'sample_data/random2.csv',
                   'sample_data/random3.tsv',
                   '-out',
                   'sample_output/test_run_unnamed.csv']

arglist_named = ['-in',
                 'sample_data/random1.xls',
                 'sample_data/random2.csv',
                 'sample_data/random3.tsv',
                 '-out',
                 'sample_output/test_run_named.csv',
                 '-cols',
                 'The',
                 'Holy',
                 'Grail']

arglist_partially_named = ['-in',
                           'sample_data/random1.xls',
                           'sample_data/random2.csv',
                           'sample_data/random3.tsv',
                           '-out',
                           'sample_output/test_run_partially_named.csv',
                           '-cols',
                           'The',
                           'Holy']

arglist_resized = ['-in',
                   'sample_data/random1.xls',
                   'sample_data/random2.csv',
                   'sample_data/random3.tsv',
                   '-out',
                   'sample_output/test_run_resized.csv',
                   '-size',
                   'A1:C5']

arglist_resized_bad_size_1 = ['-in',
                              'sample_data/random1.xls',
                              'sample_data/random2.csv',
                              'sample_data/random3.tsv',
                              '-out',
                              'sample_output/test_run_resized.csv',
                              '-size',
                              'A1:C0']

arglist_resized_bad_size_2 = ['-in',
                              'sample_data/random1.xls',
                              'sample_data/random2.csv',
                              'sample_data/random3.tsv',
                              '-out',
                              'sample_output/test_run_resized.csv',
                              '-size',
                              'nee']


class TestRun():

    def test_run_unnamed_cols(self):
        args = main.argument_parser(arglist_unnamed)
        output = args.output
        file_exists = os.path.exists(output)
        if file_exists:
            os.remove(output)
        main.run(args)
        file_exists = os.path.exists(output)
        assert file_exists
        with open(output) as f:
            rows = f.readlines()
        for row in rows:
            assert row.count(",") == len(args.input) - 1
        assert rows[0] == "random1,random2,random3\n"

    def test_run_named_cols(self):
        args = main.argument_parser(arglist_named)
        output = args.output
        file_exists = os.path.exists(output)
        if file_exists:
            os.remove(output)
        main.run(args)
        file_exists = os.path.exists(output)
        assert file_exists
        with open(output) as f:
            rows = f.readlines()
        for row in rows:
            assert row.count(",") == len(args.input) - 1
        assert rows[0] == "The,Holy,Grail\n"

    def test_run_partially_named_cols(self):
        args = main.argument_parser(arglist_partially_named)
        output = args.output
        file_exists = os.path.exists(output)
        if file_exists:
            os.remove(output)
        main.run(args)
        file_exists = os.path.exists(output)
        assert file_exists
        with open(output) as f:
            rows = f.readlines()
        for row in rows:
            assert row.count(",") == len(args.input) - 1
        assert rows[0] == "The,Holy,random3\n"

    def test_run_resized(self):
        args = main.argument_parser(arglist_resized)
        output = args.output
        file_exists = os.path.exists(output)
        if file_exists:
            os.remove(output)
        main.run(args)
        file_exists = os.path.exists(output)
        assert file_exists
        with open(output) as f:
            rows = f.readlines()
        assert len(rows) == 16
        for row in rows:
            assert row.count(",") == 2
        assert rows[0] == "random1,random2,random3\n"

    def test_run_resized_bad_size_1(self):
        args = main.argument_parser(arglist_resized_bad_size_1)
        with pytest.raises(ValueError):
            main.run(args)

    def test_run_resized_bad_size_2(self):
        args = main.argument_parser(arglist_resized_bad_size_2)
        with pytest.raises(ValueError):
            main.run(args)

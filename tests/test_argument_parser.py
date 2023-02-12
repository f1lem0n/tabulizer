import argparse

import tabulizer.main as main

arglist_unnamed = ['-in',
                   'sample_data/random1.xls',
                   'sample_data/random2.csv',
                   '-out',
                   'sample_output/test1.csv']

arglist_named = ['-in',
                 'sample_data/random1.xls',
                 'sample_data/random2.csv',
                 '-out',
                 'sample_output/test1.csv',
                 '-cols',
                 'The',
                 'Holy',
                 'Grail']

arglist_resized = ['-in',
                   'sample_data/random1.xls',
                   'sample_data/random2.csv',
                   '-out',
                   'sample_output/test1.csv',
                   '-size',
                   'A1:C5']


class TestArgParser():

    def test_argument_parser_unnamed(self):
        args = main.argument_parser(arglist_unnamed)
        assert type(args) == argparse.Namespace
        assert args.input == ["sample_data/random1.xls",
                              "sample_data/random2.csv"]
        assert args.output == "sample_output/test1.csv"
        assert args.colnames is None

    def test_argument_parser_named(self):
        args = main.argument_parser(arglist_named)
        assert type(args) == argparse.Namespace
        assert args.input == ["sample_data/random1.xls",
                              "sample_data/random2.csv"]
        assert args.output == "sample_output/test1.csv"
        assert args.colnames == ["The", "Holy", "Grail"]

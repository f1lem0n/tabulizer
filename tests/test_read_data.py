import pytest

import tabulizer.main as main

size = None


class TestReadData():

    def test_read_data_ods(self) -> None:
        col = main.read_data("sample_data/template1.ods", size)
        assert type(col) == list and len(col) == 96

    def test_read_data_xlsx(self) -> None:
        col = main.read_data("sample_data/OD.xlsx", size)
        assert type(col) == list and len(col) == 96

    def test_read_data_xls(self) -> None:
        col = main.read_data("sample_data/random1.xls", size)
        assert type(col) == list and len(col) == 96

    def test_read_data_csv(self) -> None:
        col = main.read_data("sample_data/random2.csv", size)
        assert type(col) == list and len(col) == 96

    def test_read_data_tsv(self) -> None:
        col = main.read_data("sample_data/random3.tsv", size)
        assert type(col) == list and len(col) == 96

    def test_read_data_unsupported(self) -> None:
        with pytest.raises(TypeError):
            main.read_data("sample_data/unsupported.docx", size)

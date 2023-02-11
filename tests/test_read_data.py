import tabulizer.main as main


def test_read_data_ods() -> None:

    col = main.read_data("sample_data/template1.ods")
    assert type(col) == list and len(col) == 96


def test_read_data_xlsx() -> None:
    col = main.read_data("sample_data/OD.xlsx")
    assert type(col) == list and len(col) == 96


def test_read_data_xls() -> None:
    col = main.read_data("sample_data/random1.xls")
    assert type(col) == list and len(col) == 96


def test_read_data_csv() -> None:
    col = main.read_data("sample_data/random2.csv")
    assert type(col) == list and len(col) == 96


def test_read_data_tsv() -> None:
    col = main.read_data("sample_data/random3.tsv")
    assert type(col) == list and len(col) == 96

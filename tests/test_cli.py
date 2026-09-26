import pytest

from toolkit.__main__ import main


def test_cli_calc_success(capsys):
    assert main(["calc", "2+3*4"]) == 0
    assert capsys.readouterr().out.strip() == "14"


def test_cli_calc_errors_to_stderr(capsys):
    assert main(["calc", "1/0"]) == 2
    captured = capsys.readouterr()
    assert captured.err != ''
    assert captured.out == ''


def test_cli_convert_success(capsys):
    assert main(['convert', '1000', '--from', 'mm', '--to', 'm']) == 0
    assert capsys.readouterr().out.strip() == '1'


def test_cli_convert_below_zero_error(capsys):
    assert main(["convert", "-300", "--from", "c", "--to", "f"]) == 2
    assert capsys.readouterr().err != ""


def test_cli_help_exits_zero():
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])
    assert exc_info.value.code == 0
"""Tests for pygra.main CLI parsing."""

from pygra.main import _parse_interleaved


class TestParseInterleaved:

    def test_per_file_columns_do_not_leak_to_later_files(self):
        args = _parse_interleaved(
            ["--file", "a.dat", "--x", "0", "--y", "3", "--file", "b.dat"]
        )
        assert args["files"] == [
            {"path": "a.dat", "xcol": 0, "ycol": 3, "dxcol": 0, "dycol": 0},
            {"path": "b.dat", "xcol": 0, "ycol": 1, "dxcol": 0, "dycol": 0},
        ]

    def test_trailing_columns_apply_globally_to_positional_files(self):
        args = _parse_interleaved(["a.dat", "b.dat", "--x", "2", "--y", "4"])
        assert args["files"] == [
            {"path": "a.dat", "xcol": 2, "ycol": 4, "dxcol": 0, "dycol": 0},
            {"path": "b.dat", "xcol": 2, "ycol": 4, "dxcol": 0, "dycol": 0},
        ]

    def test_mixed_per_file_and_trailing_global_columns(self):
        args = _parse_interleaved(
            ["--file", "a.dat", "--x", "1", "--file", "b.dat", "--y", "5"]
        )
        assert args["files"] == [
            {"path": "a.dat", "xcol": 1, "ycol": 5, "dxcol": 0, "dycol": 0},
            {"path": "b.dat", "xcol": 0, "ycol": 5, "dxcol": 0, "dycol": 0},
        ]

    def test_load_argument_is_preserved(self):
        args = _parse_interleaved(["--load", "session.json", "a.dat"])
        assert args["load"] == "session.json"
        assert args["files"] == [
            {"path": "a.dat", "xcol": 0, "ycol": 1, "dxcol": 0, "dycol": 0}
        ]

    def test_per_file_error_columns_do_not_leak_to_later_files(self):
        args = _parse_interleaved(
            ["--file", "a.dat", "--dx", "2", "--dy", "3", "--file", "b.dat"]
        )
        assert args["files"] == [
            {"path": "a.dat", "xcol": 0, "ycol": 1, "dxcol": 2, "dycol": 3},
            {"path": "b.dat", "xcol": 0, "ycol": 1, "dxcol": 0, "dycol": 0},
        ]

    def test_trailing_error_columns_apply_globally_to_positional_files(self):
        args = _parse_interleaved(["a.dat", "b.dat", "--dx", "2", "--dy", "3"])
        assert args["files"] == [
            {"path": "a.dat", "xcol": 0, "ycol": 1, "dxcol": 2, "dycol": 3},
            {"path": "b.dat", "xcol": 0, "ycol": 1, "dxcol": 2, "dycol": 3},
        ]

    def test_error_columns_default_to_zero(self):
        args = _parse_interleaved(["a.dat"])
        assert args["files"] == [
            {"path": "a.dat", "xcol": 0, "ycol": 1, "dxcol": 0, "dycol": 0}
        ]

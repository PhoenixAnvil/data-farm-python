from __future__ import annotations

from argparse import Namespace
from pathlib import Path

from pytest import MonkeyPatch

from data_farm.application.bootstrap import setup_logger


def test_setup_logger_dot_creates_log_in_cwd(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    ns = Namespace(log_file=".", verbose=1)
    setup_logger(ns)


def test_setup_logger_directory_path(tmp_path: Path) -> None:
    ns = Namespace(log_file=str(tmp_path), verbose=1)
    setup_logger(ns)


def test_setup_logger_file_path(tmp_path: Path) -> None:
    ns = Namespace(log_file=str(tmp_path / "custom.log"), verbose=1)
    setup_logger(ns)

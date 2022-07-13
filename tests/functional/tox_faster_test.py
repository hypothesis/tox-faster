from unittest.mock import sentinel

import tox_faster


def test_it():
    assert tox_faster.tox_runenvreport(sentinel.venv, sentinel.action) == []

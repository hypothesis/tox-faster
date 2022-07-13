from unittest.mock import sentinel

import pytest

from tox_faster import main


class TestToxRunEnvReport:
    @pytest.mark.parametrize(
        "environ,expected",
        [
            # In dev there' no CI envvar and tox-faster disables the envreport.
            ({}, []),
            # On GitHub Actions CI is set to "true" and tox-faster doesn't disable the envreport.
            ({"CI": "true"}, None),
        ],
    )
    def test_it(self, mocker, environ, expected):
        mocker.patch.dict(main.environ, environ)

        assert main.tox_runenvreport(sentinel.venv, sentinel.action) == expected

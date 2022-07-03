from unittest.mock import sentinel

from tox_faster.main import tox_runenvreport


class TestToxRunEnvReport:
    def test_it_disables_the_env_report(self):
        # pylint:disable=use-implicit-booleaness-not-comparison
        assert tox_runenvreport(sentinel.venv, sentinel.action) == []

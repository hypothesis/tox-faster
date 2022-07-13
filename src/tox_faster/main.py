from os import environ

import pluggy

hookimpl = pluggy.HookimplMarker("tox")


@hookimpl
def tox_runenvreport(venv, action):  # pylint:disable=unused-argument
    # pragma: no cover
    if "CI" in environ:
        return None

    return []

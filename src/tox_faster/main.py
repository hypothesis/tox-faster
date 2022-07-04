import pluggy

hookimpl = pluggy.HookimplMarker("tox")


@hookimpl
def tox_runenvreport(venv, action):  # pylint:disable=unused-argument
    return []

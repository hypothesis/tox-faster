import pluggy

hookimpl = pluggy.HookimplMarker("tox")


@hookimpl
def tox_runenvreport(_venv, _action):
    return []

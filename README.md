<a href="https://github.com/hypothesis/tox-faster/actions/workflows/ci.yml?query=branch%3Amain"><img src="https://img.shields.io/github/workflow/status/hypothesis/tox-faster/CI/main"></a>
<a href="https://pypi.org/project/tox-faster"><img src="https://img.shields.io/pypi/v/tox-faster"></a>
<a><img src="https://img.shields.io/badge/python-3.10 | 3.9 | 3.8-success"></a>
<a href="https://github.com/hypothesis/tox-faster/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-BSD--2--Clause-success"></a>
<a href="https://github.com/hypothesis/cookiecutters/tree/main/pypackage"><img src="https://img.shields.io/badge/cookiecutter-pypackage-success"></a>
<a href="https://black.readthedocs.io/en/stable/"><img src="https://img.shields.io/badge/code%20style-black-000000"></a>

# tox-faster

A tox plugin that speeds up tox a little.

For installation instructions see [INSTALL.md](https://github.com/hypothesis/tox-faster/blob/main/INSTALL.md).

For how to set up a tox-faster development environment see
[HACKING.md](https://github.com/hypothesis/tox-faster/blob/main/HACKING.md).

Speedups
--------

tox-faster implements these tox speedups:

### Disables tox's dependency listing (the "env report")

Every single time you run tox it runs `pip freeze` to print out a list of all
the packages installed in the testenv being run:

<pre><code>tox -e lint
<b>lint installed: aiohttp==3.8.1,aioresponses==0.7.3,aiosignal==1.2.0,
alembic==1.8.0,amqp==5.1.1,astroid==2.11.6,async-timeout==4.0.1,attrs==20.2.0,
...</b>
lint run-test-pre: PYTHONHASHSEED='2115099637'
lint run-test: commands[0] | pylint lms bin
...</code></pre>

You don't need to see that in your terminal every time you run tox and if your
venv contains a lot of packages it's quite annoying because it prints
screenfulls of text. Running `pip freeze` also introduces a noticeable delay in
the startup time of every tox command: on my machine with my venv it adds about
250ms.

You can hide this output by running tox with `-q` but that doesn't make tox run
any faster: it seems that it still runs the `pip freeze` even though it doesn't
print it.

tox-faster actually prevents tox from running `pip freeze` so your tox output
will be shorter and your tox commands will start faster:

```terminal
$ tox -e lint
lint run-test-pre: PYTHONHASHSEED='3084948731'
lint run-test: commands[0] | pylint lms bin
...
```

**tox-faster doesn't disable the env report on CI.**
The env report can be useful diagnostic information on CI so if an environment
variable named `CI` is set to any value then tox-faster won't disable the env report.
This also enables you to re-enable the env report locally by running
`CI=true tox ...`.

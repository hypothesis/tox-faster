<a href="https://github.com/hypothesis/tox-faster/actions/workflows/ci.yml?query=branch%3Amain"><img src="https://img.shields.io/github/actions/workflow/status/hypothesis/tox-faster/ci.yml?branch=main"></a>
<a href="https://pypi.org/project/tox-faster"><img src="https://img.shields.io/pypi/v/tox-faster"></a>
<a><img src="https://img.shields.io/badge/python-3.10 | 3.9 | 3.8 | 3.7-success"></a>
<a href="https://github.com/hypothesis/tox-faster/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-BSD--2--Clause-success"></a>
<a href="https://github.com/hypothesis/cookiecutters/tree/main/pypackage"><img src="https://img.shields.io/badge/cookiecutter-pypackage-success"></a>
<a href="https://black.readthedocs.io/en/stable/"><img src="https://img.shields.io/badge/code%20style-black-000000"></a>

# tox-faster

A tox plugin that speeds up tox a little.

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

## Setting up Your tox-faster Development Environment

First you'll need to install:

* [Git](https://git-scm.com/).
  On Ubuntu: `sudo apt install git`, on macOS: `brew install git`.
* [GNU Make](https://www.gnu.org/software/make/).
  This is probably already installed, run `make --version` to check.
* [pyenv](https://github.com/pyenv/pyenv).
  Follow the instructions in pyenv's README to install it.
  The **Homebrew** method works best on macOS.
  The **Basic GitHub Checkout** method works best on Ubuntu.
  You _don't_ need to set up pyenv's shell integration ("shims"), you can
  [use pyenv without shims](https://github.com/pyenv/pyenv#using-pyenv-without-shims).

Then to set up your development environment:

```terminal
git clone https://github.com/hypothesis/tox-faster.git
cd tox-faster
make help
```

## Releasing a New Version of the Project

1. First, to get PyPI publishing working you need to go to:
   <https://github.com/organizations/hypothesis/settings/secrets/actions/PYPI_TOKEN>
   and add tox-faster to the `PYPI_TOKEN` secret's selected
   repositories.

2. Now that the tox-faster project has access to the `PYPI_TOKEN` secret
   you can release a new version by just [creating a new GitHub release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).
   Publishing a new GitHub release will automatically trigger
   [a GitHub Actions workflow](.github/workflows/pypi.yml)
   that will build the new version of your Python package and upload it to
   <https://pypi.org/project/tox-faster>.

## Changing the Project's Python Versions

To change what versions of Python the project uses:

1. Change the Python versions in the
   [cookiecutter.json](.cookiecutter/cookiecutter.json) file. For example:

   ```json
   "python_versions": "3.10.4, 3.9.12",
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request

## Changing the Project's Python Dependencies

To change the production dependencies in the `setup.cfg` file:

1. Change the dependencies in the [`.cookiecutter/includes/setuptools/install_requires`](.cookiecutter/includes/setuptools/install_requires) file.
   If this file doesn't exist yet create it and add some dependencies to it.
   For example:

   ```
   pyramid
   sqlalchemy
   celery
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request

To change the project's formatting, linting and test dependencies:

1. Change the dependencies in the [`.cookiecutter/includes/tox/deps`](.cookiecutter/includes/tox/deps) file.
   If this file doesn't exist yet create it and add some dependencies to it.
   Use tox's [factor-conditional settings](https://tox.wiki/en/latest/config.html#factors-and-factor-conditional-settings)
   to limit which environment(s) each dependency is used in.
   For example:

   ```
   lint: flake8,
   format: autopep8,
   lint,tests: pytest-faker,
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request

Testing Manually
----------------

To test it manually you can install your local development copy of
`tox-faster` into the local development environment of another tox-using
project such as
[cookiecutter-pypackage-test](https://github.com/hypothesis/cookiecutter-pypackage-test):

1. Install a local development copy of `cookiecutter-pypackage-test` in a temporary directory:

   ```terminal
   git clone https://github.com/hypothesis/cookiecutter-pypackage-test.git /tmp/cookiecutter-pypackage-test
   ```

2. Run `cookiecutter-pypackage-test`'s `make sure` command to make sure that
   everything is working and to trigger tox to create its `.tox/.tox`
   venv:

   ```terminal
   make --directory "/tmp/cookiecutter-pypackage-test" sure
   ```

3. Uninstall the production copy of `tox-faster` from `cookiecutter-pypackage-test`'s `.tox/.tox` venv:

   ```terminal
   /tmp/cookiecutter-pypackage-test/.tox/.tox/bin/pip uninstall tox-faster
   ```

4. Install your local development copy of `tox-faster` into `cookiecutter-pypackage-test`'s `.tox/.tox` venv:

   ```terminal
   /tmp/cookiecutter-pypackage-test/.tox/.tox/bin/pip install -e .
   ```

5. Now `cookiecutter-pypackage-test` commands will use your local development copy of `tox-faster`:

   ```terminal
   make --directory "/tmp/cookiecutter-pypackage-test" test
   ```

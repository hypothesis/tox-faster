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
beautifulsoup4==4.9.3,behave==1.2.6,billiard==3.6.4.0,cachetools==4.2.2,
celery==5.2.7,certifi==2020.6.20,cffi==1.15.0,charset-normalizer==2.0.1,
click==8.1.3,click-didyoumean==0.3.0,click-plugins==1.1.1,click-repl==0.2.0,
coverage==6.4.1,cryptography==36.0.2,dill==0.3.4,ecdsa==0.17.0,
factory-boy==3.2.1,Faker==8.1.2,freezegun==1.2.1,frozenlist==1.2.0,
google-auth==1.30.0,google-auth-oauthlib==0.4.4,greenlet==1.0.0,
gunicorn==20.1.0,h-api==1.0.1,h-assets==1.0.4,h-matchers==1.2.14,
h-pyramid-sentry==1.2.3,h-vialib==1.0.19,httpretty==1.1.4,hupper==1.10.2,
idna==2.10,importlib-metadata==4.8.1,importlib-resources==5.8.0,
iniconfig==1.1.1,isort==5.10.1,Jinja2==2.11.3,jsonschema==3.2.0,kombu==5.2.4,
lazy-object-proxy==1.6.0,Mako==1.1.3,MarkupSafe==1.1.1,marshmallow==3.17.0,
mccabe==0.6.1,multidict==5.2.0,newrelic==7.12.0.176,oauthlib==3.2.0,
packaging==21.3,parse==1.19.0,parse-type==0.5.2,PasteDeploy==2.1.0,plaster==1.0,
plaster-pastedeploy==0.7,platformdirs==2.2.0,pluggy==0.13.1,
prompt-toolkit==3.0.29,psycopg2==2.9.3,py==1.10.0,pyasn1==0.4.8,
pyasn1-modules==0.2.8,pycodestyle==2.8.0,pycparser==2.21,pycryptodomex==3.15.0,
pydocstyle==6.1.1,PyJWT==2.4.0,pylint==2.14.4,pyparsing==3.0.6,pyramid==2.0,
pyramid-exclog==1.1,pyramid-googleauth==1.0.2,pyramid-jinja2==2.10,
pyramid-retry==2.1.1,pyramid-services==2.2,pyramid-tm==2.5,pyrsistent==0.17.3,
pytest==7.1.2,python-dateutil==2.8.1,python-jose==3.3.0,pytz==2022.1,
requests==2.28.1,requests-oauthlib==1.3.1,rsa==4.7.2,sentry-sdk==0.17.6,
six==1.15.0,snowballstemmer==2.1.0,soupsieve==2.2.1,SQLAlchemy==1.4.39,
text-unidecode==1.3,tomli==2.0.0,tomlkit==0.11.0,transaction==2.4.0,
translationstring==1.4,typing_extensions==4.0.0,urllib3==1.26.5,venusian==3.0.0,
vine==5.0.0,waitress==2.1.2,wcwidth==0.2.5,webargs==8.1.0,WebOb==1.8.6,
WebTest==3.0.0,wired==0.2.2,wrapt==1.12.1,xmltodict==0.13.0,yarl==1.7.2,
zipp==3.4.1,zope.deprecation==4.3.0,zope.interface==5.1.0,zope.sqlalchemy==1.6</b>
lint run-test-pre: PYTHONHASHSEED='2115099637'
lint run-test: commands[0] | pylint lms bin
...</code></pre>

You don't need to see that in your terminal every time you run tox and if your
venv contains a lot of packages it's quite annoying because it prints
screenfulls of text. Running `pip freeze` also introduces a noticeable delay in
the startup time of every tox command: on my machine with my venv it adds about
250ms.

tox-faster removes this so your tox output will be shorter and your tox
commands will start faster:

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
`CI=yes tox ...`.

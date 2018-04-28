#!/usr/bin/env python
"""
creates the app instance.

can be used via
$ export FLASK_APP=manage # and any other env vars
$ flask run
--
or via $ python <script.py> # where script.py imports app from this file and calls it's run()
"""
import os
import sys
from app import create_app
from config import EnvironmentName

app_mode = None
try:
    app_mode = os.environ['FLASK_ENV']
except KeyError:
    print("Set the FLASK_ENV environmental variable: FLASK_ENV=<%s>" % "|".join(EnvironmentName.all_names()))
    exit(1)

# the Flask app instance
app = create_app(app_mode)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    sys.exit(not result.wasSuccessful())


@app.cli.command()
def which_env():
    print("command ran in %s" % app.env)

#!/usr/bin/env python
"""
exports the app instance.
"""
import os

from dotenv import load_dotenv

from app import create_app

dot_env_file = os.environ.get("DOT_ENV_FILE")
if dot_env_file:
    load_dotenv(dot_env_file, verbose=True)

app_mode = None
try:
    app_mode = os.environ['FLASK_ENV']
except KeyError:
    print("Set the FLASK_ENV environmental variable")
    exit(1)
# the Flask app instance
app = create_app(app_mode)


@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def which_env():
    print("command ran in %s" % app.env)

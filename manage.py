#!/usr/bin/env python
"""
exports the app instance.
"""
import os
from app import create_app

app_mode = None
try:
    app_mode = os.environ['FLASK_ENV']
except KeyError:
    print("Set the FLASK_ENV environmental variable")
    exit(1)

# the Flask app instance
app = create_app(app_mode)


@app.cli.command()
def which_env():
    print("command ran in %s" % app.env)

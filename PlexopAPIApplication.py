"""
run this file when running in production/not using the flask cli
set env vars and then
$ python PlexopAPIApplication.py <port>

!This uses the built-in python development server!
"""

from sys import argv
import os

os.environ['FLASK_ENV'] = 'production'
port = int(argv[1]) if len(argv) >= 2 else 5000
from manage import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)

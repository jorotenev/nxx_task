"""
run this file when running in production/not using the flask cli
set env vars and then
$ python PlexopAPIApplication.py <port>
"""
from manage import app
from sys import argv

port = int(argv[1]) if len(argv) >= 2 else 5000

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)

# NXX
## Run
* `$ export SECRET_KEY=<some secret, required by flask>`
* `$ export API_ENDPOINT_FUNNELS=<url of /dev/funnels>`
* `$ export API_ENDPOINT_FUNNELS_ENUMS=<url of /dev/funnels/enums>`
* `$ export API_AUTH_HEADER=<the auth secret>`
* `$ pipenv --python=3.6 && pipenv install && pipenv shell`
* `$ python PlexopAPIApplication.py # you can optionally pass a port number as a third param`

## Test
$ pipenv --python=3.6 && pipenv install && pipenv shell
$ python -m unittest discover --start-directory=tests/ --top-level-directory=.

or alternatively via Pycharm - select `tests/` as _Path_ when adding a new _Python test_ run configuration.
# NXX
## How to run
$ export API_ENDPOINT_FUNNELS=<url of /dev/funnels>
$ export API_ENDPOINT_FUNNELS_ENUMS=<url of /dev/funnels/enums>
$ export API_AUTH_HEADER=<the auth secret>
$ pipenv install
$ python PlexopAPIApplication.py # you can optionally pass a port number as a third param

## Tests
There are tests under `tests/test_funnels`
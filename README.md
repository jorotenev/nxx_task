# NXX
## Run
* `$ export SECRET_KEY=<some secret, required by flask>`
* `$ export API_ENDPOINT_FUNNELS=<url of /dev/funnels>`
* `$ export API_ENDPOINT_FUNNELS_ENUMS=<url of /dev/funnels/enums>`
* `$ export API_AUTH_HEADER=<the auth secret>`
* `$ pipenv --python=3.6 && pipenv install && pipenv shell`
* `$ python PlexopAPIApplication.py # you can optionally pass a port number as a third param`

Also works with `flask run`, instead of calling python directly. See note about env vars.

## Test
`$ pipenv --python=3.6 && pipenv install && pipenv shell`
`$ export DOT_ENV_FILE=.env_test`
`$ flask test`

or alternatively via Pycharm - add the full path to .env_test as `DOT_ENV_FILE` and then run the tests under `tests/`.

## Env vars
Setting the `DOT_ENV_FILE` to point to an .env file will load the env vars from it, so it's not needed to set them
manually via export/set when running/testing the app.
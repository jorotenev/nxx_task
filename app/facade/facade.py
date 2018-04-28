from app.helpers.time import measure_time_decorator
from flask import current_app
from requests import get


@measure_time_decorator("get_funnels:external")
def get_funnels():
    endpoint = current_app.config['API_ENDPOINT_FUNNELS']
    return make_request(endpoint)


@measure_time_decorator("get_funnels_enums:external")
def get_funnels_enums():
    endpoint = current_app.config['API_ENDPOINT_FUNNELS_ENUMS']
    return make_request(endpoint)


def make_request(url):
    auth_header_key = "x-api-key"
    auth_header_value = current_app.config['API_AUTH_HEADER']
    
    return get(url, headers={auth_header_key: auth_header_value}).json()

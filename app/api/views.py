from . import api
from app.helpers.api_utils import make_json_response
from app.facade import get_funnels_enums, get_funnels


@api.route("/ping")
def ping():
    return "pong"


@api.route('/funnels')
def funnels():
    return make_json_response('{}')

@api.route('/funnels/summary')
def funnels_summary():
    return make_json_response('{}')

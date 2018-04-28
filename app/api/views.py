from app.api.funnel_summary import prepare_funnels_summary
from app.api.resolve_ids import get_funnels_and_resolve_ids
from app.helpers.time import measure_time_decorator
from . import api
from app.helpers.api_utils import make_json_response



@api.route('/funnels')
@measure_time_decorator(activity_name="api.funnels")
def funnels():
    # fetch the funnels from the API and enrich the ID (i.e. use the funnels_enums mapping to resolve the ids)
    resolved_ids_funnels = get_funnels_and_resolve_ids()

    # return the funnels as json
    return make_json_response(resolved_ids_funnels)


@api.route('/funnels/summary')
@measure_time_decorator(activity_name="api.funnels_summary")
def funnels_summary():
    funnels_with_resolved_ids = get_funnels_and_resolve_ids()

    summary = prepare_funnels_summary(funnels_with_resolved_ids)

    return make_json_response(summary)

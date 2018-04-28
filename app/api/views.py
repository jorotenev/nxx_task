from app.helpers.time import measure_time_decorator
from . import api
from app.helpers.api_utils import make_json_response
from app.facade import get_funnels_enums, get_funnels


@api.route('/funnels')
@measure_time_decorator(activity_name="api.funnels")
def funnels():
    # get the funnels from the third-party API
    raw_funnels = get_funnels()
    enums = get_funnels_enums()
    # now enrich the funnels
    enriched_funnels = resolve_ids_in_funnels(raw_funnels, enums)

    return make_json_response(enriched_funnels)


@api.route('/funnels/summary')
@measure_time_decorator(activity_name="api.funnels_summary")
def funnels_summary():
    return make_json_response('{}')


def resolve_ids_in_funnels(raw_funnels, enums):
    """
    For each funnel, resolve all of ids within 'alerts' and 'extended_info'.
    Pure function since it doesn't change the input @raw_funnels
    :param raw_funnels: {list}
    :return: {list}
    """
    return [enrich_funnel(funnel, enums) for funnel in raw_funnels]


def enrich_funnel(funnel, enums):
    resolved_funnel = dict(funnel)

    resolved_funnel['alerts'] = resolve_ids_in_alerts(funnel['alerts'], enums)

    zone_type_id = resolved_funnel['extended_info']['zone_type_id']
    resolved_funnel['extended_info']['zone_type_name'] = get_name_from_enums(enums,
                                                                             'zone_types',
                                                                             zone_type_id)
    return resolved_funnel


def resolve_ids_in_alerts(alerts, enums):
    """
    Given a list of alerts resolve the <*_id> attributes to <*_name> attributes by using
    @enums dict as a source of truth.
    :param alerts: {list}
    :param enums: {dict} the source of truth (id -> name mappings) when resolving an id to the corresponding truth
    :return:
    """
    resolved_alerts = []
    # we use the mapping so that given a `<something>_id` attribute,
    # we know in which "namespace" of the funnels_enums to look for the corresponding value
    # the "name_key" is the name we will use in the alert object for the resolved id.
    mappings = {
        "alert_type_id": {"name_key": "alert_type_name", "enums_namespace": "alert_types"},
        "alert_category_id": {"name_key": "alert_category_name", "enums_namespace": "alert_categories"},
        "severity_level_id": {"name_key": "severity_level_name", "enums_namespace": "severity_levels"},
        "snooze_reason_id": {"name_key": "snooze_reason_name", "enums_namespace": "snooze_reasons"}
    }
    for a in alerts:
        alert = dict(a)
        for id_key, key_info in mappings.items():
            alert[key_info['name_key']] = get_name_from_enums(enums, key_info['enums_namespace'], alert[id_key])

        resolved_alerts.append(alert)

    return resolved_alerts


def get_name_from_enums(enums, enum_namespace, id):
    """
    Utility method. Given an @enums with the following shape:
    {
        "alert_types":
        [
            {
                "id": 1,
                "name": "some name"
            },...
        ],...
    }

    @enum_namespace is a top-level key from @enums. @id will be compared against values under the "id"
    keys. when there's a match, the "name" value will be returned.

    e.g. get_name_from_enums(enums, "alert_types", 1) will return "some name"
    """
    if id == None:
        return None
    valid = [enum['name'] for enum in enums[enum_namespace] if str(enum['id']) == str(id)]
    return valid[0]

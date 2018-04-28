from app.facade import get_funnels, get_funnels_enums
import logging as log


def get_funnels_and_resolve_ids():
    """
    Interacts with the third-party API to get the funnels and the enums.
    For each funnel, resolve all of ids within its 'alerts' and 'extended_info'.
    :return: {list}
    """
    raw_funnels = get_funnels()
    funnels_enums = get_funnels_enums()
    return [resolve_ids_single_funnel(funnel, funnels_enums) for funnel in raw_funnels]


def resolve_ids_single_funnel(funnel, enums):
    resolved_funnel = dict(funnel)

    # resolve alerts
    resolved_funnel['alerts'] = resolve_ids_alerts(funnel['alerts'], enums)

    # resolve extended_info's zone_type
    zone_type_id = resolved_funnel['extended_info']['zone_type_id']
    zone_type_name = get_name_from_enums(enums, 'zone_types', zone_type_id)
    resolved_funnel['extended_info']['zone_type_name'] = zone_type_name

    return resolved_funnel


def resolve_ids_alerts(alerts, enums):
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
            try:
                alert[key_info['name_key']] = get_name_from_enums(enums, key_info['enums_namespace'], alert[id_key])
            except Exception as ex:
                log.critical("Couldn't resolve {attr_name} for alert_id={alert_id}. Original exception {exc}".
                             format(alert_id=alert['alert_id'],
                                    attr_name=id_key,
                                    exc=str(ex)))
                continue

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
    try:
        return valid[0]
    except:
        raise Exception("[{namespace}] doesn't have object with id={id}".format(namespace=enum_namespace, id=id))

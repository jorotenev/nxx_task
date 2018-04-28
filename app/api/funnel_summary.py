def prepare_funnels_summary(funnels):
    enriched_funnels = [prepare_single_funnel_summary(funnel) for funnel in funnels]

    return list(sorted(enriched_funnels, key=lambda funnel: funnel['exposure_sum'], reverse=True))


def prepare_single_funnel_summary(funnel):
    attrs_to_remove = ['alerts', 'actions_history', 'extended_info']

    enriched_funnel = dict(funnel)

    enriched_funnel['number_of_alerts'] = len(funnel['alerts'])
    enriched_funnel['number_of_snoozed_alerts'] = len([a for a in funnel['alerts'] if a['is_snoozed']])
    enriched_funnel['exposure_sum'] = sum(a['exposure'] for a in funnel['alerts'])
    enriched_funnel['max_exposure_alert_id'] = \
        max([a for a in funnel['alerts']], key=lambda alert: alert['exposure'])['alert_id']

    # "Properties of “extended_info” should be flattened to the “funnel” level"
    for k, v in enriched_funnel['extended_info'].items():
        enriched_funnel[k] = v
    for to_remove in attrs_to_remove:
        enriched_funnel.pop(to_remove)
    return enriched_funnel

import json

from app.funnels.resolve_ids import get_name_from_enums
from tests.base_test import BaseTest, BaseTestWithHTTPMethodsMixin, PatchMixin
from tests.test_funnels.dummy_data import dummy_funnels_enums, dummy_funnels


class TestFunnels(BaseTest, BaseTestWithHTTPMethodsMixin, PatchMixin):
    def setUp(self):
        self.endpoint = "api.funnels"

        self.patched_get_funnels = self.patch("app.funnels.resolve_ids.get_funnels")
        self.patched_get_funnels.return_value = dummy_funnels
        self.patched_get_funnels_enums = self.patch("app.funnels.resolve_ids.get_funnels_enums")
        self.patched_get_funnels_enums.return_value = dummy_funnels_enums

        self.response_json = json.loads(self.get(url=self.endpoint))

    def test_smoke(self):
        response_raw = self.get("api.funnels", raw_response=True)

        self.assertTrue(len(self.response_json), "Response shouldn't be empty")
        self.assertEqual(200, response_raw.status_code)

    def test_funnel_object_resolved_ids(self):
        """
        Test that the `_id` attributes of a funnel were resolved with `_name` attrs
        using the correct "name" from the enum
        """

        result_json = self.response_json
        self.assertTrue(len(result_json))

        mappings = {
            'alert_type_id': {"namespace": "alert_types", "name_key": "alert_type_name"},
            'alert_category_id': {"namespace": "alert_categories", "name_key": "alert_category_name"},
            'severity_level_id': {"namespace": "severity_levels", "name_key": "severity_level_name"},
            'snooze_reason_id': {"namespace": "snooze_reasons", "name_key": "snooze_reason_name"}
        }
        for funnel in result_json:
            source_funnel = [f for f in dummy_funnels if f['funnel_id'] == funnel['funnel_id']][0]

            for alert in funnel['alerts']:
                source_alert = [a for a in source_funnel['alerts'] if a['alert_id'] == alert['alert_id']][0]

                for key, key_info in mappings.items():
                    value_for_name_attr = alert[key_info['name_key']]
                    expected_name_val = get_name_from_enums(dummy_funnels_enums, key_info['namespace'],
                                                            source_alert[key])
                    self.assertEqual(expected_name_val,
                                     value_for_name_attr)

            source_extended_info = source_funnel['extended_info']
            extended_info = funnel['extended_info']

            self.assertEqual(source_extended_info['zone_type_name'], extended_info['zone_type_name'])

    def test_none_id_none_name(self):
        """
        "If some id is null, the name will also be null"
        """
        copy_dumy_funnels = [dict(dummy_funnels[1])]
        copy_dumy_funnels[0]['alerts'][0]['alert_type_id'] = None
        self.patched_get_funnels.return_value = copy_dumy_funnels

        response_json = json.loads(self.get(url=self.endpoint))
        alert_name = response_json[0]['alerts'][0]['alert_type_name']
        self.assertIsNone(alert_name)


class TestFunnelsSummary(BaseTest, BaseTestWithHTTPMethodsMixin, PatchMixin):
    def setUp(self):
        self.endpoint = "api.funnels_summary"

        self.patched_get_funnels = self.patch("app.funnels.resolve_ids.get_funnels")
        self.patched_get_funnels.return_value = dummy_funnels
        self.patched_get_funnels_enums = self.patch("app.funnels.resolve_ids.get_funnels_enums")
        self.patched_get_funnels_enums.return_value = dummy_funnels_enums

        self.response_json = json.loads(self.get(url=self.endpoint, raw_response=False))

    def test_contains_correct_keys(self):
        """
        test that the expected_summary_enriched_fields are in the funnels from the response
        &&
        that the keys that should have been removed are not in the funnels from the response
        """
        response_json = self.response_json
        self.assertTrue(len(self.response_json), "Response shouldn't be empty")

        expected_summary_enriched_fields = [
            "number_of_alerts", "number_of_snoozed_alerts",
            "exposure_sum", "max_exposure_alert_id"
        ]
        expected_removed_fields = [
            "alerts", "actions_history"
        ]

        for funnel in response_json:
            self.assertTrue(all([(enriched_field in funnel) for enriched_field in expected_summary_enriched_fields]))
            self.assertTrue(
                all([(enriched_field not in funnel) for enriched_field in expected_removed_fields]))

    def test_flattened_extended_info(self):
        """
        "Properties of “extended_info” should be flattened to the “funnel” level,
         “extended_info” property itself should be removed."
        """
        response_json = self.response_json
        extended_info_keys = ["advertiser_id", "funnel_is_published",
                              "brand_id", "zone_type_id"]
        for funnel in response_json:
            self.assertNotIn('extended_info', funnel)
            self.assertTrue(all([(extended_info_key in funnel) for extended_info_key in extended_info_keys]))

    def test_funnels_order(self):
        """
        "Funnels should be sorted by “exposure_sum” field by descending order."
        """
        response_json = self.response_json
        sorted_funnels = sorted(response_json, key=lambda tunnel: tunnel['exposure_sum'], reverse=True)

        self.assertEqual(sorted_funnels, response_json, "The funnels were not sorted correctly")

    def test_enriched_attrs_values(self):
        response_json = self.response_json
        for funnel in response_json:
            source_funnel = [f for f in dummy_funnels if f['funnel_id'] == funnel['funnel_id']][0]
            expected_number_of_alerts = len(source_funnel['alerts'])
            self.assertEqual(expected_number_of_alerts, funnel['number_of_alerts'])
            expected_number_of_snoozed_alerts = len([alert for alert in source_funnel['alerts'] if alert['is_snoozed']])
            self.assertEqual(expected_number_of_snoozed_alerts, funnel['number_of_snoozed_alerts'])

            expected_exposure_sum = sum([alert['exposure'] for alert in source_funnel['alerts']])
            self.assertEqual(expected_exposure_sum, funnel['exposure_sum'])

            expected_max_exposure_id = max(source_funnel['alerts'], key=lambda a: a['exposure'])['alert_id']
            self.assertEqual(expected_max_exposure_id, funnel['max_exposure_alert_id'])

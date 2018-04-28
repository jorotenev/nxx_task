import json

from tests.base_test import BaseTest, BaseTestWithHTTPMethodsMixin, PatchMixin
from tests.test_funnels.dummy_data import dummy_funnels_enums, dummy_funnels

expected_plain_fields = [
    "alert_id", "alert_type_id", "alert_category_id", "severity_level_change_date",
    "severity_level_id", "is_active", "exposure", "is_snoozed", "snooze_reason_id",
    "snooze_comment", "calculated_value", "benchmark"
]
enriched_fields = [
    "alert_type_name", "alert_category_name", "severity_level_name",
    "snooze_reason_name"
]
combined_fields = expected_plain_fields + enriched_fields


class TestFunnels(BaseTest, BaseTestWithHTTPMethodsMixin, PatchMixin):
    def setUp(self):
        self.endpoint = "api.funnels"

        self.patched_get_funnels = self.patch("app.api.views.get_funnels")
        self.patched_get_funnels = dummy_funnels
        self.patched_get_funnels_enums = self.patch("app.api.views.get_funnels_enums")
        self.patched_get_funnels_enums = dummy_funnels_enums

        self.response_json = json.loads(self.get(url=self.endpoint))

    def test_smoke(self):
        response_raw = self.get("api.funnels", raw_response=True)
        self.assertTrue(len(self.response_json), "Response shouldn't be empty")

        self.assertEqual(200, response_raw.status_code)

    def test_response_has_expected_attrs(self):
        result_json = self.response_json
        self.assertTrue(len(result_json))
        for funnel in result_json:
            self.assertEqual(len(combined_fields), len(funnel),
                             "The response json object doesn't contain the expected number of attributes")

            self.assertEqual(set(combined_fields), set(funnel.keys()), "The response doesn't contain the expected"
                                                                       "attributes")

    def test_funnel_object_resolved_ids(self):
        """
        Test that the `_id` attributes of a funnel were resolved with `_name` attrs
        using the correct value from the enum
        """

        result_json = self.response_json

        self.assertFalse(True)
        mappings = {
            "alert_type_id": "alert_type_name",
            "alert_category_id": "alert_category_name",
            "severity_level_id": "severity_level_name",
            "snooze_reason_id": "snooze_reason_id"
        }
        for funnel in result_json:
            for original_id_key, resolved_name_key in mappings.items():
                original_id = funnel[original_id_key]
                expected_resolved_value = [enum['name'] for enum in dummy_funnels_enums[original_id_key] if
                                           enum['id'] == original_id][0]
                self.assertEqual(expected_resolved_value, funnel[resolved_name_key])


class TestFunnelsSummary(BaseTest, BaseTestWithHTTPMethodsMixin, PatchMixin):
    def setUp(self):
        self.endpoint = "api.funnels_summary"

        self.patched_get_funnels = self.patch("app.api.views.get_funnels")
        self.patched_get_funnels = dummy_funnels
        self.patched_get_funnels_enums = self.patch("app.api.views.get_funnels_enums")
        self.patched_get_funnels_enums = dummy_funnels_enums

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
            source_funnel = [f for f in dummy_funnels if f['id'] == funnel['id']][0]
            expected_number_of_alerts = len(source_funnel['alerts'])
            self.assertEqual(expected_number_of_alerts, funnel['number_of_alerts'])
            expected_number_of_snoozed_alerts = len([alert for alert in source_funnel['alerts'] if alert['is_snoozed']])
            self.assertEqual(expected_number_of_snoozed_alerts, funnel['number_of_snoozed_alerts'])

            expected_exposure_sum = sum([alert['exposure'] for alert in source_funnel['alerts']])
            self.assertEqual(expected_exposure_sum, funnel['exposure_sum'])

            expected_max_exposure_id = max(funnel['alerts'], key=lambda a: a['exposure'])['alert_id']
            self.assertEqual(expected_max_exposure_id, funnel['max_exposure_alert_id'])

# NXX
## The task
* endpoints returning views on alert data
* log the time it takes to serve the request and the time taken for handling requests to external services
  * write logs to stdout & file
*  input data comes from two API endpoints secured via an api-key - uses a custom header for auth
* response format from API #1
```
[
    {
        "funnel_id":<some funnel id>,
        "agency_id":<some agency id>,
        "is_published": <true|false>,
        "extended_info": {"nested":"attrs"},
        "alerts": [
            {
                "severity_level_id": "",
                "alert_type_id": "",
                "snooze_reason_id": "",
                "alert_category_id": ""
            }
        ]

    }
]
```
Mapping for the above ids comes from API #2.
* Add `[GET] /funnels`
  * data as returned by API #1 but with ids resolved by API #2
* Add `[GET] /funnels/summary` - enriched funnel object


## How to run
$ export API_ENDPOINT_FUNNELS=<url of /dev/funnels>
$ export API_ENDPOINT_FUNNELS_ENUMS=<url of /dev/funnels/enums>
$ export API_AUTH_HEADER=<the auth secret>
$ pipenv install
$ python PlexopAPIApplication.py  # you can optionally pass a number as a port


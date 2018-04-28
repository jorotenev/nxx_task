from datetime import datetime, timezone
from functools import wraps
from time import monotonic
import logging as log


def utc_now_str():
    return datetime.now(timezone.utc).isoformat()


def measure_time_decorator(activity_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start = monotonic()
            endpoint_result = f(*args, **kwargs)
            log.info("[%s] took %.3f seconds" % (activity_name, (monotonic() - start)))
            return endpoint_result

        return decorated_function

    return decorator

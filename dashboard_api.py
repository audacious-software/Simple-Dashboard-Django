import random

import pytz

from django.conf import settings
from django.utils import timezone

def dashboard_signals():
    return [{
        'name': 'Random Test Signal',
        'refresh_interval': 900,
        'configuration': {
            'widget_columns': 2
        }
    }, {
        'name': 'Latest Time Signal',
        'refresh_interval': 60,
        'configuration': {
            'widget_columns': 4
        }
    }]

def dashboard_template(signal_name):
    if signal_name == 'Random Test Signal':
        return 'simple_dashboard_widget_random_test.html'

    return None

def update_dashboard_signal_value(signal_name):
    if signal_name == 'Random Test Signal':
        random_value = random.randint(1, 6)

        return {
            'display_value': random_value,
            'value': random_value,
            'range_min': 1,
            'range_max': 6,
        }

    if signal_name == 'Latest Time Signal':
        now = timezone.now().astimezone(pytz.timezone(settings.TIME_ZONE))

        return str(now)

    return None

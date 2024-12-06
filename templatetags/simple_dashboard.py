# pylint: disable=line-too-long, no-member

import datetime

from django import template
from django.template.loader import render_to_string

from ..models import DashboardSignal

register = template.Library()

@register.simple_tag(takes_context=True)
def simple_dashboard_active_signals(context):
    template_context = {}

    template_context.update(context.flatten())

    template_context['active_dashboard_signals'] = DashboardSignal.objects.filter(active=True).order_by('-priority', 'name')

    return render_to_string('simple_dashboard_active_signals.html', template_context)

@register.filter
def simple_dashboard_is_date(value):
    try:
        datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f%z')

        return True
    except ValueError:
        pass
    except TypeError:
        pass

    try:
        datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f%z')

        return True
    except ValueError:
        pass
    except TypeError:
        pass

    return False

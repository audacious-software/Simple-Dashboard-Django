# pylint: disable=line-too-long, no-member

import importlib
import datetime

from django import template
from django.conf import settings
from django.template.loader import render_to_string

from ..models import DashboardSignal

register = template.Library()

@register.simple_tag(takes_context=True)
def simple_dashboard_active_signals(context):
    template_context = {}

    template_context.update(context.flatten())

    signal_context = template_context.get('signal_context', None)

    if signal_context is not None:
        template_context['active_dashboard_signals'] = DashboardSignal.objects.filter(active=True, configuration__signal_context=signal_context).order_by('-priority', 'name')
    else:
        template_context['active_dashboard_signals'] = []

        for signal in DashboardSignal.objects.filter(active=True).order_by('-priority', 'name'):
            if signal.configuration.get('signal_context', None) is None:
                template_context['active_dashboard_signals'].append(signal)

    return render_to_string('simple_dashboard_active_signals.html', template_context)

@register.simple_tag(takes_context=False)
def simple_dashboard_site_name():
    try:
        return settings.SIMPLE_DASHBOARD_SITE_NAME
    except AttributeError:
        pass

    return '(Missing site name - set settings.SIMPLE_DASHBOARD_SITE_NAME.)'

@register.simple_tag(takes_context=False)
def simple_dashboard_additional_pages():
    dashboard_pages = []

    for app in settings.INSTALLED_APPS:
        try:
            app_module = importlib.import_module('.dashboard_api', package=app)

            dashboard_pages.extend(app_module.dashboard_pages())
        except ImportError:
            pass
        except AttributeError:
            pass

    template_context = {
        'dashboard_pages': dashboard_pages
    }

    return render_to_string('simple_dashboard_additional_pages.html', template_context)

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

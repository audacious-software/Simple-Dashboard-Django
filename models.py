# pylint: disable=line-too-long, no-member

import calendar
import importlib
import traceback

from django.conf import settings
from django.core.checks import Warning, register # pylint: disable=redefined-builtin
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone

try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField

class DashboardSignal(models.Model):
    package = models.CharField(max_length=4096)
    name = models.CharField(max_length=4096)
    refresh_interval = models.DurationField()

    active = models.BooleanField(default=False)

    configuration = JSONField(default=dict, null=True, blank=True, encoder=DjangoJSONEncoder)

    priority = models.IntegerField(default=0)

    next_run = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '%s (%s)' % (self.name, self.package)

    def update_value(self):
        now = timezone.now()

        app_module = importlib.import_module('.dashboard_api', package=self.package)

        new_value = app_module.update_dashboard_signal_value(self.name)

        if new_value is None:
            return

        DashboardSignalValue.objects.create(signal=self, recorded=now, value=new_value)

        self.next_run = now + self.refresh_interval
        self.save()

    def widget_columns(self):
        return self.configuration.get('widget_columns', 3)

    def widget_body(self):
        context = {
            'signal': self
        }

        widget_template = None

        try:
            app_module = importlib.import_module('.dashboard_api', package=self.package)

            widget_template = app_module.dashboard_template(self.name)
        except ImportError:
            traceback.print_exc() # pass
        except AttributeError:
            traceback.print_exc() # pass

        if widget_template is None:
            widget_template = 'simple_dashboard_widget_generic.html'

        context['widget_template'] = widget_template

        return render_to_string(widget_template, context)

    def latest_value(self):
        return self.signal_values.order_by('-recorded').first()

    def latest_values(self, limit=12):
        values = list(self.signal_values.order_by('-recorded')[:limit])
        values.reverse()

        return values

class DashboardSignalValue(models.Model):
    signal = models.ForeignKey(DashboardSignal, related_name='signal_values', on_delete=models.CASCADE)

    recorded = models.DateTimeField()

    value = JSONField(default=dict, encoder=DjangoJSONEncoder)

    def __str__(self):
        return '%s = %s' % (self.signal, self.display_value())

    def display_value(self):
        try:
            display_value = self.value.get('display_value', None)

            if display_value is not None:
                return display_value
        except AttributeError:
            pass # Unstructured value

        return self.value

    def fetch_value(self):
        return self.value

    def timestamp(self):
        return calendar.timegm(self.recorded.utctimetuple())

    def edit_link(self):
        return '/admin/simple_dashboard/dashboardsignalvalue/%s/change/' % self.pk

@register()
def check_prettyjson_installed(app_configs, **kwargs): # pylint: disable=unused-argument
    errors = []

    if ('prettyjson' in settings.INSTALLED_APPS) is False:
        error = Warning('"prettyjson" not found in settings.INSTALLED_APPS', hint='Add "prettyjson" to settings.INSTALLED_APPS.', obj=None, id='simple_dashboard.W001')
        errors.append(error)

    return errors

@register()
def check_site_name_defined(app_configs, **kwargs): # pylint: disable=unused-argument
    errors = []

    if hasattr(settings, 'SIMPLE_DASHBOARD_SITE_NAME') is False:
        error = Warning('SIMPLE_DASHBOARD_SITE_NAME parameter not defined', hint='Update configuration to include SIMPLE_DASHBOARD_SITE_NAME.', obj=None, id='simple_dashboard.W002')
        errors.append(error)

    return errors

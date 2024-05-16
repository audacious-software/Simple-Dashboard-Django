from prettyjson import PrettyJSONWidget

from django.contrib import admin

try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField

from .models import DashboardSignal, DashboardSignalValue

@admin.register(DashboardSignal)
class DashboardSignalAdmin(admin.ModelAdmin):
    list_display = ('name', 'package', 'active', 'priority', 'refresh_interval', 'next_run',)
    list_filter = ('active', 'refresh_interval', 'package', 'next_run',)

    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget(attrs={'initial': 'parsed'})}
    }

@admin.register(DashboardSignalValue)
class DashboardSignalValueAdmin(admin.ModelAdmin):
    list_display = ('signal', 'recorded', 'fetch_value',)
    list_filter = ('recorded', 'signal',)

    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget(attrs={'initial': 'parsed'})}
    }

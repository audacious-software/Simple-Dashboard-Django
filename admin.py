from prettyjson import PrettyJSONWidget

from django.contrib import admin, messages

try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField

from .models import DashboardSignal, DashboardSignalValue

@admin.register(DashboardSignalValue)
class DashboardSignalValueAdmin(admin.ModelAdmin):
    list_display = ('signal', 'recorded', 'display_value',)
    list_filter = ('recorded', 'signal',)

    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget(attrs={'initial': 'parsed'})}
    }

class DashboardSignalValueInline(admin.TabularInline):
    model = DashboardSignalValue

    verbose_name = 'Signal Value'
    verbose_name_plural = 'Signal Values'
    template = 'admin_inlines/dashboard_signal_value_tabular.html'

    fields = ['recorded', 'edit_link']
    readonly_fields = ['recorded', 'edit_link']
    ordering = ('-recorded',)

    def has_change_permission(self, request, obj=None): # pylint: disable=arguments-differ,unused-argument
        return False

    def has_add_permission(self, request, obj=None): # pylint: disable=arguments-differ,unused-argument
        return False

    def has_delete_permission(self, request, obj=None): # pylint: disable=arguments-differ,unused-argument
        return False

def activate_signal(modeladmin, request, queryset): # pylint: disable=unused-argument
    updated = queryset.update(active=True)

    messages.add_message(request, messages.INFO, '%d signal(s) activated.' % updated)

activate_signal.short_description = "Activate selected signals"

def deactivate_signal(modeladmin, request, queryset): # pylint: disable=unused-argument
    updated = queryset.update(active=False)

    messages.add_message(request, messages.INFO, '%d signal(s) deactivated.' % updated)

deactivate_signal.short_description = "Deactivate selected signals"

@admin.register(DashboardSignal)
class DashboardSignalAdmin(admin.ModelAdmin):
    list_display = ('name', 'package', 'active', 'priority', 'refresh_interval', 'next_run',)
    list_filter = ('active', 'refresh_interval', 'package', 'next_run',)
    search_fields = ('name', 'package', 'configuration',)

    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget(attrs={'initial': 'parsed'})}
    }

    inlines = [
        DashboardSignalValueInline,
    ]

    actions = [activate_signal, deactivate_signal]

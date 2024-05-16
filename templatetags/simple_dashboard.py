from django import template
from django.template.loader import render_to_string

register = template.Library()

from ..models import DashboardSignal

@register.simple_tag(takes_context=True)
def simple_dashboard_active_signals(context):
    template_context = {}

    template_context.update(context.flatten())

    template_context['active_dashboard_signals'] = DashboardSignal.objects.filter(active=True).order_by('-priority')

    return render_to_string('simple_dashboard_active_signals.html', template_context)
# pylint: disable=line-too-long, no-member

import json

from django import template
from django.template.loader import render_to_string
from django.utils.html import mark_safe
from ..models import DashboardSignal

register = template.Library()

@register.simple_tag(takes_context=True)
def simple_dashboard_active_signals(context):
    template_context = {}

    template_context.update(context.flatten())

    template_context['active_dashboard_signals'] = DashboardSignal.objects.filter(active=True).order_by('-priority', 'name')

    return render_to_string('simple_dashboard_active_signals.html', template_context)

@register.filter
def simple_dashboard_to_json(raw_obj):
    return mark_safe(json.dumps(raw_obj))

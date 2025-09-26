# -*- coding: utf-8 -*-
# pylint: disable=no-member,line-too-long

import six

from django.core.management.base import BaseCommand

from quicksilver.decorators import handle_schedule, add_qs_arguments, handle_lock

from ...models import DashboardSignal

class Command(BaseCommand):
    help = 'Refreshes dashboard signals'

    @add_qs_arguments
    def add_arguments(self, parser):
        pass

    @handle_schedule
    @handle_lock
    def handle(self, *args, **options):
        six.print_('Deleted: %s' % (DashboardSignal.objects.all().delete(),))

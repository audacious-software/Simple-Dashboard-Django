# -*- coding: utf-8 -*-
# pylint: disable=no-member,line-too-long

from __future__ import print_function

import datetime
import importlib

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from quicksilver.decorators import handle_schedule, add_qs_arguments

from ...models import DashboardSignal

class Command(BaseCommand):
    help = 'Refreshes dashboard signals'

    @add_qs_arguments
    def add_arguments(self, parser):
        pass

    @handle_schedule
    def handle(self, *args, **options):
        print('Deleted: %s' % (DashboardSignal.objects.all().delete(),))

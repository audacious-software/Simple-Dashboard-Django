# -*- coding: utf-8 -*-
# pylint: disable=no-member,line-too-long

import datetime
import importlib
import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from quicksilver.decorators import handle_schedule, add_qs_arguments, handle_logging, handle_lock

from ...models import DashboardSignal

class Command(BaseCommand):
    help = 'Refreshes dashboard signals'

    @add_qs_arguments
    def add_arguments(self, parser):
        parser.add_argument('--force',
                            action='store_true',
                            dest='force',
                            default=False,
                            help='Force updated of all signal values (including inactive)')

    @handle_logging
    @handle_schedule
    @handle_lock
    def handle(self, *args, **options): # pylint: disable=too-many-locals
        logger = logging.getLogger(__name__)

        logger.debug('Updating signals...')

        for app in settings.INSTALLED_APPS:
            try:
                app_module = importlib.import_module('.dashboard_api', package=app)

                logger.debug('Fetching signals from %s...', app)

                dashboard_signals = app_module.dashboard_signals()

                for dashboard_signal in dashboard_signals:
                    signal_name = dashboard_signal.get('name', None)

                    refresh_interval = datetime.timedelta(seconds=dashboard_signal.get('refresh_interval', -1))

                    existing = DashboardSignal.objects.filter(package=app, name=signal_name).first()

                    if existing is None:
                        configuration = dashboard_signal.get('configuration', {})

                        signal = DashboardSignal.objects.create(package=app, name=signal_name, refresh_interval=refresh_interval, configuration=configuration)

                        if configuration.get('active', False):
                            signal.active = True
                            signal.save()

                logger.debug('Fetched signals from %s: %s', app, dashboard_signals)
            except ImportError:
                pass
            except AttributeError:
                pass

        now = timezone.now()

        signals_due = DashboardSignal.objects.exclude(next_run__gte=now).exclude(active=False)

        if options.get('force', False):
            signals_due = DashboardSignal.objects.all()

        for signal_due in signals_due:
            logging.debug('Updating signal %s...', signal_due)
            signal_due.update_value()
            logger.debug('Updated signal %s.', signal_due)

        logging.debug('Done updating signals.')

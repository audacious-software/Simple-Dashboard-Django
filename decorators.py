# pylint: disable=line-too-long, no-member

import datetime
import inspect

from .models import DashboardSignal

def add_dashboard_signal(**kwargs):
    def wrap(func):
        def wrapped_func(*args):
            refresh_interval = datetime.timedelta(seconds=kwargs.get('refresh_interval', -1))

            module = inspect.getmodule(func)

            package = '?'

            if module is not None:
                package = module.__name__.split('.')[0]

            signal_name = func.__name__

            existing = DashboardSignal.objects.filter(package=package, name=signal_name).first()

            if existing is not None:
                if existing.refresh_interval != refresh_interval:
                    existing.refresh_interval = refresh_interval
                    existing.save()
            else:
                DashboardSignal.objects.create(package=package, name=signal_name, refresh_interval=refresh_interval)

            return func(*args)

        return wrapped_func

    return wrap

# @add_dashboard_signal(refresh_interval=60)
# def user_count():
#     pass

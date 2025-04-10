# pylint: disable=line-too-long, wrong-import-position

import sys

if sys.version_info[0] > 2:
    from django.urls import re_path as url # pylint: disable=no-name-in-module
else:
    from django.conf.urls import url

from .views import simple_dashboard_home, simple_dashboard_logout, simple_dashboard_account

urlpatterns = [
    url(r'^logout$', simple_dashboard_logout, name='simple_dashboard_logout'),
    url(r'^account$', simple_dashboard_account, name='simple_dashboard_account'),
    url(r'^$', simple_dashboard_home, name='simple_dashboard_home'),
]

# pylint: skip-file
# Generated by Django 4.2.11 on 2024-05-10 18:31

import django.contrib.postgres.fields.jsonb

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_dashboard', '0004_alter_dashboardsignal_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardsignal',
            name='configuration',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
    ]

# pylint: skip-file
# Generated by Django 4.2.13 on 2024-05-16 18:53

import django.core.serializers.json
import django.contrib.postgres.fields.jsonb

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_dashboard', '0005_alter_dashboardsignal_configuration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardsignal',
            name='configuration',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True),
        ),
        migrations.AlterField(
            model_name='dashboardsignalvalue',
            name='value',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
        ),
    ]

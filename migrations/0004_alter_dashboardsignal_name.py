# pylint: skip-file
# Generated by Django 4.2.11 on 2024-05-10 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_dashboard', '0003_alter_dashboardsignal_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardsignal',
            name='name',
            field=models.CharField(max_length=4096),
        ),
    ]

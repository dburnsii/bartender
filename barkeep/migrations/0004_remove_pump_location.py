# Generated by Django 3.0.2 on 2020-01-31 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barkeep', '0003_auto_20200110_0821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pump',
            name='location',
        ),
    ]
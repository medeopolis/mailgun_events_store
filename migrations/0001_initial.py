# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-09 10:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MailgunEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(max_length=30)),
                ('event_id', models.CharField(max_length=254)),
                ('timestamp', models.CharField(max_length=30)),
                ('json', models.TextField(blank=True, null=True)),
            ],
        ),
    ]

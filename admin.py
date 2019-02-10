# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from datetime import datetime

# Register your models here.
from .models import MailgunEvent

class MailgunEventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'display_timestamp', 'event_id')
    list_filter = ('event_type',)

    def display_timestamp(self, obj):
        return datetime.fromtimestamp(float(obj.timestamp))

admin.site.register(MailgunEvent, MailgunEventAdmin)

# add display options

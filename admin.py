# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from datetime import datetime

# Register your models here.
from .models import MailgunEvent

class MailgunEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_type', 'display_timestamp', 'event_id', 'recipient')
    list_filter = ('event_type', 'method', 'severity', 'recipient_domain')
    search_fields = ('event_type', 'envelope', 'recipient', 'ip')

    def display_timestamp(self, obj):
        return datetime.fromtimestamp(float(obj.timestamp))

admin.site.register(MailgunEvent, MailgunEventAdmin)

# add display options

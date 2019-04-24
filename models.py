# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class MailgunEvent(models.Model):
    event_type = models.CharField(max_length=30)
    event_id = models.CharField(max_length=254)
    timestamp = models.CharField(max_length=30)
    json = models.TextField(default='', blank=True)
    # New, not guaranteed available fields
    log_level = models.CharField(default='', blank=True, max_length=30)
    method = models.CharField(default='', blank=True, max_length=30)
    envelope = models.TextField(default='', blank=True)
    flags = models.TextField(default='', blank=True)
    delivery_status = models.TextField(default='', blank=True)
    geolocation = models.TextField(default='', blank=True)
    message = models.TextField(default='', blank=True)
    severity = models.CharField(default='', blank=True, max_length=30)
    storage = models.TextField(default='', blank=True)
    reason = models.CharField(default='', blank=True, max_length=255)
    recipient = models.CharField(default='', blank=True, max_length=255)
    recipient_domain = models.CharField(default='', blank=True, max_length=255)
    campaigns = models.TextField(default='', blank=True)
    tags = models.TextField(default='', blank=True)
    user_variables = models.TextField(default='', blank=True)
    routes = models.TextField(default='', blank=True)
    ip = models.CharField(default='', blank=True, max_length=30)
    client_info = models.TextField(default='', blank=True)

    def __unicode__(self):
        # TODO: output timestamp in a human readable format
        return '{} event with id {}'.format(self.event_type, self.event_id)


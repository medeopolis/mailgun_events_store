# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class MailgunEvent(models.Model):
    event_type = models.CharField(max_length=30)
    event_id = models.CharField(max_length=254)
    timestamp = models.CharField(max_length=30)
    json = models.TextField(null=True, blank=True)

    def __unicode__(self):
        # TODO: output timestamp in a human readable format
        return '{} event with id {}'.format(self.event_type, self.event_id)


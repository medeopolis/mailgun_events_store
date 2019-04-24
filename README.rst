Download Mailgun events and store them in Django.

Why
===

Mailgun_ provide a `mail forwarding, tracking, and management service`_. It is
good.

.. _Mailgun: https://www.mailgun.com/
.. _`mail forwarding, tracking, and management service`: https://www.mailgun.com/email-api

Sadly at the free tier `records are maintained`_ for only 2 days and the paid
tiers around 30 days.

.. _`records are maintained`: https://documentation.mailgun.com/en/latest/quickstart-events.html#events

Using this package enables the storage of those records for an extended period,
tieing them to other data about the user as required.


How
===

Configure mailgun::

    MAILGUN_EVENTS_API_URL='https://api.mailgun.net/v3'
    MAILGUN_EVENTS_DOMAIN='email.example.com'
    MAILGUN_EVENTS_AUTH_KEY='you will be supplied with this by mailgun'
    # Optional, set to value in seconds if desired.
    MAILGUN_EVENTS_START_TIME=None
    # MAILGUN_EVENTS_START_TIME='Thu, 07 Feb 2019 22:00:00+1100'


Expand your INSTALLED_APPS to include this::

    INSTALLED_APPS += [ 'mailgun_events_store' ]


Add get_mailgun_events.py to your crontab, I'm running it hourly.

::

    /etc/crontab:1 * * * * root  /srv/service/environment/bin/python2.7 /srv/site/website/manage.py get_mailgun_events


Known problems
==============

Codebase is only tested with python 2.7; upgrading to 3.x will occur at a future date.


from django.core.management import BaseCommand

from django.conf import settings
import requests
from datetime import datetime, timedelta
from mailgun_events_store.models import MailgunEvent

# Pretty sure this is an hour early
if settings.MAILGUN_EVENTS_START_TIME:
    start_time = settings.MAILGUN_EVENTS_START_TIME
else:
    # Two hours ago
    two_hours_ago = datetime.now() - timedelta(hours=2)
    start_time = datetime.strftime(two_hours_ago, '%s')

mailgun_api = '{}/{}'.format(settings.MAILGUN_EVENTS_API_URL, settings.MAILGUN_EVENTS_DOMAIN)
login_auth = ('api', settings.MAILGUN_EVENTS_AUTH_KEY)

def record_events(json_values):
    for mail_record in json_values:
        # FIXME: time limit to this ~48 hours; mailgun don't guarantee an event_id is ALWAYS unique
        # when doing comparisons, Note the database is storing unix time
        if not MailgunEvent.objects.filter(event_id = mail_record['id']):
            # TODO: error handling: what if this fails?
            # Record guaranteed data
            new_event_object = MailgunEvent(
                event_type = mail_record['event'],
                event_id = mail_record['id'],
                timestamp = mail_record['timestamp'],
                json = mail_record
                )
            # Pre save so if the next part goes wrong we still get the json.
            new_event_object.save()
            # Now record variable fields; re use new_event_object
            for sect in mail_record:
                try:
                  # In my testing on Guest models this never failed and silently failed
                  # (by succeeding) by simply not writing out the data
                  if sect == 'id':
                    setattr(new_event_object, 'event_id', mail_record[sect])
                  elif not mail_record[sect]:
                    pass
                  else:
                    setattr(new_event_object, sect.replace('-', '_'), mail_record[sect])
                except AttributeError as ae:
                  setattr(new_event_object, sect.replace('-', '_'), '') # set to empty text
            new_event_object.save()

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting command')
        # Downloading initial batch of events
        next_page_token = ''
        self.stdout.write('Performing First query')
        url_params = {'begin': start_time, 'ascending': 'yes', 'event': 'accepted OR rejected OR delivered OR failed OR opened OR clicked OR unsubscribed OR complained OR stored', 'limit': 300}
        r = requests.get('{}/events'.format(mailgun_api, next_page_token), auth=login_auth, params=url_params)
        # There are likely to be more results so set up pagination.
        try:
            if len(r.json()['items']) == 300:
                next_page_token = len(r.json()['paging']['next'])
            self.stdout.write('Inital request had {} items'.format(len(r.json()['items'])))
            record_events(r.json()['items'])
        except KeyError as kee:
            self.stderr.write('No items returned in current search')
            self.stderr.write(r.text)

        loop_count = 1
        while next_page_token:
            self.stdout.write('Performing query in loop {}'.format(loop_count))
            r = requests.get('{}/events/{}'.format(mailgun_api, next_page_token), auth=login_auth, params=url_params)
            try:
                if len(r.json()['items']) == 300:
                    next_page_token = len(r.json()['paging']['next'])
                else:
                    next_page_token = ''
                self.stdout.write('Extras loop {} had {} items'.format(loop_count, len(r.json()['items'])))
                record_events(r.json()['items'])
            except KeyError as kee:
                self.stderr.write('No items returned in current search')
                self.stderr.write(r.text)
                break
            loop_count += 1


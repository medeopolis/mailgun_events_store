from django.core.management import BaseCommand

from mailgun_events_store.models import MailgunEvent

import ast

def update_db():
    for existing_event_object in MailgunEvent.objects.all():
        converted_json = ast.literal_eval(existing_event_object.json)
        # for sect in json.loads(existing_event_object.json):
        for sect in converted_json:
            try:
                # In my testing on Guest models this never failed and silently failed
                # (by succeeding) by simply not writing out the data
                if sect == 'id':
                    setattr(existing_event_object, 'event_id', converted_json[sect])
                elif not converted_json[sect]:
                    pass
                else:
                    setattr(existing_event_object, sect.replace('-', '_'), converted_json[sect])
            except AttributeError as ae:
                setattr(existing_event_object, sect.replace('-', '_'), '') # set to empty text
        existing_event_object.save()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write('About to update DB')
        update_db()




from django.core.management.base import BaseCommand
from django.utils.timezone import now

from socialfeedsparser.models import Channel


class Command(BaseCommand):
    """
    Command used to get messages for the instances stored in models.Channel.

    usage:

        python manage.py collect_info_about_us
    """
    help = 'Collect messages from social services'

    def handle(self, *args, **options):
        channels = Channel.objects.to_update()
        for channel in channels:
            self.stdout.write('Processing source: "%s"' % channel)
            sc = channel.source_class(channel=channel)
            sc.collect_messages()
            channel.updated = now()
            channel.save()

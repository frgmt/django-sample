from django.core.management import BaseCommand

from cache.wrapper import RedisClient


class Command(BaseCommand):
    """ usage: python manage.py clearcache
    mainly used when deploying.
    """

    help = 'Clear cache'

    def handle(self, *args, **options):
        RedisClient().clear_general_cache()

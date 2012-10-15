from django.contrib.auth.management import create_permissions
from django.db.models import get_apps
from optparse import make_option
from django.contrib.contenttypes.management import update_all_contenttypes
from django.core.management.base import AppCommand, BaseCommand


class Command(BaseCommand):
    option_list = AppCommand.option_list + (
        make_option('--noinput', action='store_false',
                    dest='interactive', default=True,
                    help=('Tells Django to NOT prompt the user for input of '
                          'any kind.')),
    )

    help = 'Updates permissions list with any updated permissions'

    def handle(self, *args, **options):
        # Add any missing content types
        update_all_contenttypes()

        # Add any missing permissions
        for app in get_apps():
            create_permissions(app, None, 2)

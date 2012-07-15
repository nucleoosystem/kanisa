from optparse import make_option
from django.conf import settings
from django.contrib.contenttypes.management import update_all_contenttypes
from django.core.management import call_command
from django.core.management.base import AppCommand, BaseCommand, CommandError
import kanisa.models
import os
import os.path
import shutil


class Command(BaseCommand):
    option_list = AppCommand.option_list + (
        make_option('--noinput', action='store_false',
                    dest='interactive', default=True,
                    help=('Tells Django to NOT prompt the user for input of '
                          'any kind.')),
    )

    help = 'Resets database and loads sample data for demonstrating Kanisa'

    def handle(self, *args, **options):
        if not getattr(settings, 'MEDIA_ROOT', None):
            raise CommandError("Please define MEDIA_ROOT.")

        call_command('reset', 'kanisa', **options)
        self.reset_permissions()
        self.load_fixtures()
        print ""
        print "Resetting search indexes..."
        call_command('rebuild_index', **options)

    def reset_permissions(self):
        # Add any missing content types
        update_all_contenttypes()

        # Add any missing permissions
        from django.contrib.auth.management import create_permissions
        from django.db.models import get_apps
        for app in get_apps():
            create_permissions(app, None, 2)

    def load_fixtures(self):
        for subapp in ['banners', 'diary', 'sermons', ]:
            print "Loading data for %s." % subapp
            call_command('loaddata', '%s.json' % subapp)
            self.copy_media(subapp)
            print ""

    def copy_media(self, destination):
        kanisa_directory = os.path.dirname(kanisa.models.__file__)
        kanisa_fixtures_media = os.path.join(kanisa_directory,
                                             '../',
                                             'fixtures/media')

        src_files = os.listdir(kanisa_fixtures_media)

        destination_directory = os.path.join(settings.MEDIA_ROOT,
                                             "kanisa",
                                             destination)

        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)

        for file_name in src_files:
            full_file_name = os.path.join(kanisa_fixtures_media, file_name)
            if (os.path.isfile(full_file_name)):
                destination_file = os.path.join(destination_directory,
                                                file_name)
                shutil.copy(full_file_name,
                            destination_file)

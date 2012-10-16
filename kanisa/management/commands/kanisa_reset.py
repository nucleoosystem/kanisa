# flake8: noqa
from optparse import make_option
from django.conf import settings
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

        try:
            import south
            fake_options = options.copy()
            fake_options['fake'] = True
            call_command('migrate', 'kanisa', '0001', **fake_options)
            call_command('migrate', 'kanisa', **options)
        except ImportError:
            pass

        call_command('kanisa_update_permissions', **options)
        self.load_fixtures()
        print ""
        print "Resetting search indexes..."
        call_command('rebuild_index', **options)

    def load_fixtures(self):
        for subapp in ['banners', 'diary', 'sermons', 'pages', 'navigation', ]:
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

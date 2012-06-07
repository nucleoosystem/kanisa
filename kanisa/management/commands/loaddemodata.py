from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
import kanisa.models
import os, os.path
import shutil

class Command(BaseCommand):
    help = 'Loads sample data for demonstrating Kanisa'

    def handle(self, *args, **options):
        if not getattr(settings, 'MEDIA_ROOT', None):
            raise CommandError("Please define MEDIA_ROOT.")

        self.load_fixtures()
        self.copy_media()

    def load_fixtures(self):
        call_command('loaddata', 'banners.json')

    def copy_media(self):
        kanisa_directory = os.path.dirname(kanisa.models.__file__)
        kanisa_fixtures_media = os.path.join(kanisa_directory, '../', 'fixtures/media')

        src_files = os.listdir(kanisa_fixtures_media)

        destination_directory = os.path.join(settings.MEDIA_ROOT,
                                             "kanisa",
                                             "banners")

        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)

        for file_name in src_files:
            full_file_name = os.path.join(kanisa_fixtures_media, file_name)
            if (os.path.isfile(full_file_name)):
                destination_file = os.path.join(destination_directory,
                                                file_name)
                shutil.copy(full_file_name,
                            destination_file)

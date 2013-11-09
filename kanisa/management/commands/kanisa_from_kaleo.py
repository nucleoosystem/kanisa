from datetime import datetime
import json
import os.path
from os.path import basename
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import make_aware, get_current_timezone
import shutil

from kanisa.models import (
    Document,
    InlineImage,
    NavigationElement,
    Page,
)


def datetime_from_str(str):
    return make_aware(datetime.strptime(str, '%Y-%m-%dT%H:%M:%S'),
                      get_current_timezone())


class Command(BaseCommand):
    args = '<path_to_json> <path_to_media>'
    help = 'Loads data from a dump of a Kaleo installation'

    seen_page_pks = {}
    seen_navigation_link_pks = {}

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("Insufficient arguments")

        filename = args[0]
        self.uploads_path = args[1]

        try:
            with open(filename) as f:
                data = json.loads(f.read())
        except IOError as e:
            raise CommandError("Invalid JSON file %s: %s." % (filename, e))
        except ValueError as e:
            raise CommandError("Invalid JSON file %s: %s." % (filename, e))

        for item in data:
            self.handle_item(item)

    def handle_item(self, item):
        model = item['model'].replace('.', '_')
        funcname = 'handle_%s' % model
        try:
            func = getattr(self, funcname)
        except AttributeError:
            return

        func(item)

    def copy_file(self, original_pk, original_file_name, dest_dir):
        target_file_name = '%s-%s' % (str(original_pk),
                                      basename(original_file_name))
        path_for_django = os.path.join('kanisa/%s' % dest_dir,
                                       target_file_name)
        path_to_write_file = os.path.join(settings.MEDIA_ROOT,
                                          path_for_django)
        origin_path = os.path.join(self.uploads_path, original_file_name)
        shutil.copyfile(origin_path, path_to_write_file)

        return path_for_django

    def handle_serviceplans_serviceplan(self, item):
        pass

    def handle_serviceplans_band(self, item):
        pass

    def handle_serviceplans_composer(self, item):
        pass

    def handle_serviceplans_song(self, item):
        pass

    def handle_serviceplans_serviceplansongchoice(self, item):
        pass

    def handle_members_userprofile(self, item):
        pass

    def handle_people_person(self, item):
        pass

    def handle_auth_user(self, item):
        pass

    def handle_auth_group(self, item):
        pass

    def handle_auth_permission(self, item):
        pass

    def handle_attachments_attachment(self, item):
        pass

    def handle_attachments_inlineimage(self, item):
        pk = item['pk']
        title = item['fields']['name']
        slug = item['fields']['slug']
        image_path = item['fields']['image']

        path_for_django = self.copy_file(pk, image_path, 'media')

        InlineImage.objects.create(title=title,
                                   slug=slug,
                                   image=path_for_django)
        print "Created image %s." % title

    def handle_kaleo_page(self, item):

        pk = item['pk']

        parent = item['fields']['parent']
        slug = item['fields']['slug']
        title = item['fields']['title']
        contents = item['fields']['contents']
        published = item['fields']['published']

        if parent and parent not in self.seen_page_pks:
            print ("Haven't processed parent of page '%s', parent has pk %d."
                   % (title, parent))
            return

        real_parent = None
        if parent:
            real_parent = self.seen_page_pks[parent]

        draft = not published

        page = Page.objects.create(title=title,
                                   slug=slug,
                                   contents=contents,
                                   draft=draft,
                                   parent=real_parent)
        print "Created page %s, with origin pk %d." % (page.title, pk)
        self.seen_page_pks[pk] = page

    def handle_kaleo_legacypathmapping(self, item):
        pass

    def handle_sermons_sermonseries(self, item):
        pass

    def handle_sermons_sermon(self, item):
        pass

    def handle_diary_diaryeventcategory(self, item):
        pass

    def handle_diary_diaryeventtype(self, item):
        pass

    def handle_diary_diaryeventlocation(self, item):
        pass

    def handle_diary_diaryeventseries(self, item):
        pass

    def handle_diary_diaryevent(self, item):
        pass

    def handle_banners_datelessbanner(self, item):
        pass

    def handle_banners_banner(self, item):
        pass

    def handle_navigation_link(self, item):

        title = item['fields']['title']
        description = item['fields']['description']
        url = item['fields']['url']
        parent = item['fields']['parent']
        pk = item['pk']

        if parent == 1:
            # Kaleo used to have a magic top-level element which
            # everything was the child of for reasons I forget.
            real_parent = None
        else:
            if parent and parent not in self.seen_navigation_link_pks:
                print ("Haven't processed parent of link '%s', parent "
                       "has pk %d."
                       % (title, parent))
                return

            real_parent = None
            if parent:
                real_parent = self.seen_navigation_link_pks[parent]

        link = NavigationElement.objects.create(title=title,
                                                description=description,
                                                url=url,
                                                parent=real_parent)
        print "Created link with title %s, origin is %d." % (link.title, pk)
        self.seen_navigation_link_pks[pk] = link

    def handle_members_document(self, item):
        pk = item['pk']
        title = item['fields']['name']
        uploaded = item['fields']['uploaded']
        description = item['fields']['description']
        downloads = item['fields']['downloads']
        path_for_django = self.copy_file(pk, item['fields']['file'],
                                         'documents')

        uploaded = datetime_from_str(uploaded)
        document = Document.objects.create(title=title,
                                           file=path_for_django,
                                           details=description,
                                           public=True,
                                           downloads=downloads)
        document.created = uploaded
        document.save()
        print "Created document with title %s." % document.title

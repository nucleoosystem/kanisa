from datetime import datetime
import json
import os
import os.path
from os.path import basename
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import make_aware, get_current_timezone
import shutil

from kanisa.models import (
    Banner,
    Composer,
    Document,
    EventCategory,
    EventContact,
    InlineImage,
    NavigationElement,
    Page,
    Song,
)


def datetime_from_str(str):
    return make_aware(datetime.strptime(str, '%Y-%m-%dT%H:%M:%S'),
                      get_current_timezone())


class Command(BaseCommand):
    args = '<path_to_json> <path_to_media>'
    help = 'Loads data from a dump of a Kaleo installation'

    seen_composer_pks = {}
    seen_page_pks = {}
    seen_navigation_link_pks = {}
    seen_event_categories = {}
    seen_event_contacts = {}

    ordering = [
        'auth_group',
        'auth_user',
        'auth_permission',
        'members_userprofile',
        'serviceplans_composer',
        'serviceplans_song',
        'serviceplans_band',
        'serviceplans_serviceplan',
        'serviceplans_serviceplansongchoice',
        'people_person',
        'attachments_attachment',
        'attachments_inlineimage',
        'kaleo_page',
        'kaleo_legacypathmapping',
        'sermons_sermonseries',
        'sermons_sermon',
        'diary_diaryeventcategory',
        'diary_diaryeventtype',
        'diary_diaryeventlocation',
        'diary_diaryeventseries',
        'diary_diaryevent',
        'banners_datelessbanner',
        'banners_banner',
        'navigation_link',
        'members_document',
    ]

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

        for model in self.ordering:
            for item in data:
                self.handle_item(item, model)

    def handle_item(self, item, model_to_process):
        model = item['model'].replace('.', '_')

        if model != model_to_process:
            return

        funcname = 'handle_%s' % model
        try:
            func = getattr(self, funcname)
        except AttributeError:
            return

        func(item)

    def copy_file(self, original_pk, original_file_name, dest_dir):
        target_file_name = '%s-%s' % (str(original_pk),
                                      basename(original_file_name))
        path_for_django = os.path.join('kanisa', dest_dir,
                                       target_file_name)
        try:
            os.makedirs(os.path.join(settings.MEDIA_ROOT,
                                     'kanisa', dest_dir))
        except OSError:
            pass

        path_to_write_file = os.path.join(settings.MEDIA_ROOT,
                                          path_for_django)
        origin_path = os.path.join(self.uploads_path, original_file_name)

        try:
            shutil.copyfile(origin_path, path_to_write_file)
        except IOError:
            print ("Failed to copy %s to %s." % (origin_path,
                                                 path_to_write_file))
            raise

        return path_for_django

    def handle_serviceplans_serviceplan(self, item):
        pass

    def handle_serviceplans_band(self, item):
        pass

    def handle_serviceplans_composer(self, item):
        pk = item['pk']
        surname = item['fields']['last_name']
        forename = item['fields']['forenames']

        composer = Composer.objects.create(forename=forename,
                                           surname=surname)
        self.seen_composer_pks[pk] = composer
        print "Created composer %s %s." % (forename, surname)

    def handle_serviceplans_song(self, item):
        composers = item['fields']['composers']
        title = item['fields']['title']

        song = Song.objects.create(title=title)

        for c in composers:
            song.composers.add(self.seen_composer_pks[c])

        print "Created song %s." % title

    def handle_serviceplans_serviceplansongchoice(self, item):
        pass

    def handle_members_userprofile(self, item):
        pass

    def handle_people_person(self, item):
        pk = item['pk']
        first_name = item['fields']['first_name']
        last_name = item['fields']['last_name']
        name = '%s %s' % (first_name, last_name)
        email = item['fields']['email']
        image_path = item['fields']['image']

        if image_path:
            path_for_django = self.copy_file(pk, image_path, 'diary/contacts')
        else:
            path_for_django = None

        contact = EventContact.objects.create(name=name,
                                              email=email,
                                              image=path_for_django)
        self.seen_event_contacts[pk] = contact

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
        pk = item['pk']
        title = item['fields']['title']
        category = EventCategory.objects.create(title=title)

        self.seen_event_categories[pk] = category
        print "Created event category %s." % title

    def handle_diary_diaryeventtype(self, item):
        pass

    def handle_diary_diaryeventlocation(self, item):
        pass

    def handle_diary_diaryeventseries(self, item):
        pass

    def handle_diary_diaryevent(self, item):
        pass

    def handle_banners_datelessbanner(self, item):
        self.handle_banners_banner(item)

    def handle_banners_banner(self, item):
        pk = item['pk']
        headline = item['fields']['headline']
        url = item['fields']['url']
        link_text = item['fields']['link_text']
        contents = item['fields']['contents']
        image_path = item['fields']['image']
        path_for_django = self.copy_file(pk, image_path, 'banners')

        publish_from = item['fields'].get('publish_from', None)
        publish_until = item['fields'].get('publish_until', None)

        Banner.objects.create(headline=headline,
                              contents=contents,
                              image=path_for_django,
                              link_text=link_text,
                              url=url,
                              publish_from=publish_from,
                              publish_until=publish_until)
        print "Created banner %s." % headline

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

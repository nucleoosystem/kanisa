from datetime import datetime
import json
import os
import os.path
from os.path import basename
from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import make_aware, get_current_timezone
from kanisa import models
import shutil


def datetime_from_str(str):
    return make_aware(datetime.strptime(str, '%Y-%m-%dT%H:%M:%S'),
                      get_current_timezone())


def date_from_str(str):
    return datetime.strptime(str, '%Y-%m-%d').date()


def model_to_permission(model_str):
    model_to_area = {
        'attachment': 'documents',
        'band': 'services',
        'banner': 'banners',
        'datelessbanner': 'banners',
        'diaryevent': 'diary',
        'diaryeventcategory': 'diary',
        'diaryeventinstance': 'diary',
        'diaryeventlocation': 'diary',
        'diaryeventtype': 'diary',
        'document': 'documents',
        'hymn': 'services',
        'inlineimage': 'media',
        'link': 'navigation',
        'page': 'pages',
        'sermon': 'sermons',
        'sermonseries': 'sermons',
        'serviceplan': 'services',
        'serviceplansongchoice': 'services',
        'snippet': 'blocks',
        'song': 'services',
        'user': 'users',
    }

    area = model_to_area.get(model_str, None)

    if not area:
        return None

    return Permission.objects.get(codename='manage_%s' % area)


def add_attachments(contents, attachments, seen_attachments):
    for attachment_pk in attachments:
        contents = contents + '\n\n{@%s}' % seen_attachments[attachment_pk]

    return contents


class Command(BaseCommand):
    args = '<path_to_json> <path_to_media>'
    help = 'Loads data from a dump of a Kaleo installation'

    seen_attachments = {}
    seen_composer_pks = {}
    seen_content_types = {}
    seen_event_categories = {}
    seen_event_contacts = {}
    seen_event_series = {}
    seen_event_types = {}
    seen_events = {}
    seen_groups = {}
    seen_navigation_link_pks = {}
    seen_page_pks = {}
    seen_permissions = {}
    seen_sermon_series = {}
    seen_sermon_speakers = {}
    seen_services = {}
    seen_songs = {}
    seen_users = {}

    ordering = [
        'contenttypes_contenttype',
        'auth_permission',
        'auth_group',
        'auth_user',
        'people_person',
        'attachments_attachment',
        'attachments_inlineimage',
        'diary_diaryeventcategory',
        'diary_diaryeventtype',
        'diary_diaryeventseries',
        'diary_diaryevent',
        'serviceplans_composer',
        'serviceplans_song',
        'serviceplans_band',
        'serviceplans_serviceplan',
        'serviceplans_serviceplansongchoice',
        'kaleo_page',
        'sermons_sermonseries',
        'sermons_sermon',
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

        for model in self.ordering:
            funcname = 'cleanup_%s' % model
            try:
                func = getattr(self, funcname)
            except AttributeError:
                continue

            func()

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
        if not original_file_name:
            return None

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
            return None

        return path_for_django

    def handle_serviceplans_serviceplan(self, item):
        pk = item['pk']
        band_leader_user = item['fields']['band_leader_user']

        if not band_leader_user:
            # The only site that uses this stuff much has 5 as the pk
            # of the likely user. This is awesome.
            band_leader_user = 5

        band_leader = self.seen_users[band_leader_user]
        event = self.seen_events[item['fields']['event']]
        musicians = item['fields']['band_member_users']

        service = models.Service.objects.create(
            event=event,
            band_leader=band_leader
        )

        for m in musicians:
            service.musicians.add(self.seen_users[m])

        self.seen_services[pk] = service

    def handle_serviceplans_band(self, item):
        band_leader_user = item['fields']['band_leader_user']
        band_member_users = item['fields']['band_member_users']

        band = models.Band.objects.create(
            band_leader=self.seen_users[band_leader_user]
        )

        for m in band_member_users:
            band.musicians.add(self.seen_users[m])

        print "Created band %s." % unicode(band)

    def handle_serviceplans_composer(self, item):
        pk = item['pk']
        surname = item['fields']['last_name']
        forename = item['fields']['forenames']

        composer = models.Composer.objects.create(
            forename=forename,
            surname=surname
        )
        self.seen_composer_pks[pk] = composer
        print "Created composer %s %s." % (forename, surname)

    def handle_serviceplans_song(self, item):
        pk = item['pk']
        composers = item['fields']['composers']
        title = item['fields']['title']

        song = models.Song.objects.create(title=title)

        for c in composers:
            song.composers.add(self.seen_composer_pks[c])

        self.seen_songs[pk] = song
        print "Created song %s." % title

    def handle_serviceplans_serviceplansongchoice(self, item):
        models.SongInService.objects.create(
            song=self.seen_songs[item['fields']['song']],
            service=self.seen_services[item['fields']['service']],
            order=item['fields']['order']
        )

    def handle_people_person(self, item):
        pk = item['pk']
        first_name = item['fields']['first_name'].strip()
        last_name = item['fields']['last_name'].strip()
        name = '%s %s' % (first_name, last_name)
        email = item['fields']['email']
        image_path = item['fields']['image']

        if image_path:
            path_event = self.copy_file(pk, image_path, 'diary/contacts')
            path_speaker = self.copy_file(pk, image_path, 'sermons/speakers')
        else:
            path_event = None
            path_speaker = None

        contact = models.EventContact.objects.create(
            name=name,
            email=email,
            image=path_event
        )

        speaker = models.SermonSpeaker.objects.create(
            forename=first_name,
            surname=last_name,
            image=path_speaker
        )

        self.seen_event_contacts[pk] = contact
        self.seen_sermon_speakers[pk] = speaker

        print "Created event contact %s." % name
        print "Created sermon speaker %s." % name

    def handle_auth_user(self, item):
        pk = item['pk']
        username = item['fields']['username']
        first_name = item['fields']['first_name']
        last_name = item['fields']['last_name']
        is_active = item['fields']['is_active']
        is_superuser = item['fields']['is_superuser']
        last_login = datetime_from_str(item['fields']['last_login'])
        groups = item['fields']['groups']
        user_permissions = item['fields']['user_permissions']
        password = item['fields']['password']
        email = item['fields']['email']
        date_joined = datetime_from_str(item['fields']['date_joined'])

        permissions = set()
        for group in groups:
            for perm in self.seen_groups[group]:
                permissions.add(perm)

        for perm in user_permissions:
            permissions.add(self.seen_permissions[perm])

        real_permissions = set()

        for model_str in permissions:
            perm = model_to_permission(model_str)
            if not perm:
                # Model is not one we care about any more
                continue

            real_permissions.add(perm)

        user = models.RegisteredUser.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            is_staff=is_superuser,
            is_superuser=is_superuser,
            last_login=last_login,
            password=password,
            email=email,
            date_joined=date_joined
        )

        for p in real_permissions:
            user.user_permissions.add(p)

        self.seen_users[pk] = user
        print "Created user %s." % user.get_display_name()

    def handle_auth_group(self, item):
        pk = item['pk']
        permissions = item['fields']['permissions']
        self.seen_groups[pk] = set([self.seen_permissions[p]
                                    for p in permissions])

    def handle_auth_permission(self, item):
        pk = item['pk']
        content_type = item['fields']['content_type']
        self.seen_permissions[pk] = self.seen_content_types[content_type]

    def handle_contenttypes_contenttype(self, item):
        pk = item['pk']
        model = item['fields']['model']
        self.seen_content_types[pk] = model

    def handle_attachments_attachment(self, item):
        pk = item['pk']
        name = item['fields']['name']
        slug = item['fields']['slug']
        uploaded = datetime_from_str(item['fields']['uploaded'])
        path_for_django = self.copy_file(
            pk,
            item['fields']['file'],
            'documents'
        )

        document = models.Document.objects.create(
            title=name,
            slug=slug,
            file=path_for_django,
            public=True
        )

        document.created = uploaded
        document.save()
        self.seen_attachments[pk] = document.slug
        print "Document %s saved." % name

    def handle_attachments_inlineimage(self, item):
        pk = item['pk']
        title = item['fields']['name']
        slug = item['fields']['slug']
        image_path = item['fields']['image']

        path_for_django = self.copy_file(pk, image_path, 'media')

        models.InlineImage.objects.create(
            title=title,
            slug=slug,
            image=path_for_django
        )
        print "Created image %s." % title

    def handle_kaleo_page(self, item):
        pk = item['pk']

        parent = item['fields']['parent']
        slug = item['fields']['slug']
        title = item['fields']['title']
        contents = item['fields']['contents']
        published = item['fields']['published']

        contents = add_attachments(contents,
                                   item['fields']['attachments'],
                                   self.seen_attachments)

        if parent and parent not in self.seen_page_pks:
            print ("Haven't processed parent of page '%s', parent has pk %d."
                   % (title, parent))
            return

        real_parent = None
        if parent:
            real_parent = self.seen_page_pks[parent]

        draft = not published

        page = models.Page.objects.create(
            title=title,
            slug=slug,
            contents=contents,
            draft=draft,
            parent=real_parent
        )
        print "Created page %s, with origin pk %d." % (page.title, pk)
        self.seen_page_pks[pk] = page

    def handle_sermons_sermonseries(self, item):
        pk = item['pk']
        active = not item['fields']['complete']
        title = item['fields']['title']
        details = item['fields']['details']
        passage = item['fields']['passage']
        image_path = item['fields']['image']
        path_for_django = self.copy_file(pk, image_path, 'sermons/series')

        series = models.SermonSeries.objects.create(
            title=title,
            image=path_for_django,
            details=details,
            active=active,
            passage=passage
        )

        self.seen_sermon_series[pk] = series
        print "Created sermon series %s." % title

    def handle_sermons_sermon(self, item):
        pk = item['pk']

        delivered = date_from_str(item['fields']['delivered'])
        series_pk = item['fields']['series']
        downloads = item['fields']['downloads']
        title = item['fields']['title']
        passage = item['fields']['passage']
        speaker_pk = item['fields']['speaker']
        mp3_path = item['fields']['mp3']
        podcast_downloads = item['fields']['podcast_downloads']
        transcript = item['fields']['transcript']
        details = item['fields']['details']
        created = datetime_from_str(item['fields']['created'])

        path_for_django = self.copy_file(pk, mp3_path, 'sermons/mp3s/old/')

        series = self.seen_sermon_series.get(series_pk)
        speaker = self.seen_sermon_speakers[speaker_pk]

        sermon = models.Sermon.objects.create(
            title=title,
            date=delivered,
            series=series,
            speaker=speaker,
            passage=passage,
            mp3=path_for_django,
            details=details,
            transcript=transcript,
            downloads=downloads,
            podcast_downloads=podcast_downloads
        )

        # Fake creation time
        sermon.created = created
        sermon.save()

        print "Created sermon %s." % title

    def handle_diary_diaryeventcategory(self, item):
        pk = item['pk']
        title = item['fields']['title']
        slug = item['fields']['slug']

        # Redirect the old category pages
        category = models.EventCategory.objects.create(title=title)
        site = Site.objects.get_current()
        Redirect.objects.create(site=site,
                                old_path='/diary/%s/' % slug,
                                new_path='/diary/')

        self.seen_event_categories[pk] = category
        print "Created event category %s." % title

    def handle_diary_diaryeventtype(self, item):
        pk = item['pk']
        title = item['fields']['title']
        category_pk = item['fields']['category']
        contact_pk = item['fields']['contact']
        details = item['fields']['details']
        intro = item['fields']['intro']
        image_path = item['fields']['image']

        path_for_django = self.copy_file(pk, image_path, 'diary/events')

        details = add_attachments(details,
                                  item['fields']['attachments'],
                                  self.seen_attachments)

        contact = self.seen_event_contacts[contact_pk]
        event = models.RegularEvent.objects.create(
            title=title,
            image=path_for_django,
            contact=contact,
            start_time='19:00',
            intro=intro,
            details=details
        )
        event.categories.add(self.seen_event_categories[category_pk])

        self.seen_event_types[pk] = event

        print "Created event %s." % title

    def handle_diary_diaryeventseries(self, item):
        pk = item['pk']
        title = item['fields']['title']

        series = models.ScheduledEventSeries.objects.create(name=title)
        self.seen_event_series[pk] = series

    def handle_diary_diaryevent(self, item):
        pk = item['pk']
        contact = item['fields']['contact_override']
        details = item['fields']['details']
        event_end = datetime_from_str(item['fields']['event_end'])
        event_start = datetime_from_str(item['fields']['event_start'])
        event_type = item['fields']['event_type']
        intro = item['fields']['intro']
        series = item['fields']['series']
        title = item['fields']['title']

        details = add_attachments(details,
                                  item['fields']['attachments'],
                                  self.seen_attachments)

        start_time = event_start.time()

        if event_end.date() == event_start.date():
            end_date = None
            duration = event_end - event_start
            duration = int(duration.total_seconds() / 60)
        else:
            end_date = event_end.date()
            duration = None

        if contact:
            contact = self.seen_event_contacts[contact]

        if event_type:
            event_type = self.seen_event_types[event_type]

            if not intro:
                intro = event_type.intro

            if not contact:
                contact = event_type.contact

        if series:
            series = self.seen_event_series[series]

        event = models.ScheduledEvent.objects.create(
            event=event_type,
            title=title,
            date=event_start.date(),
            start_time=start_time,
            duration=duration,
            end_date=end_date,
            contact=contact,
            intro=intro,
            details=details,
            series=series
        )

        print "Created event %s." % event
        self.seen_events[pk] = event

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

        models.Banner.objects.create(
            headline=headline,
            contents=contents,
            image=path_for_django,
            link_text=link_text,
            url=url,
            publish_from=publish_from,
            publish_until=publish_until
        )
        print "Created banner %s." % headline

    def handle_navigation_link(self, item):
        title = item['fields']['title']
        description = item['fields']['description']
        url = item['fields']['url']
        parent = item['fields']['parent']
        pk = item['pk']

        if len(description) > 50:
            print ("Trimming description to 50 characters (leaves '%s')..."
                   % description[:50])

        description = description[:50]

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

        if real_parent:
            try:
                models.NavigationElement.objects.get(parent=real_parent,
                                                     url=url)
                print ("Skipping creating non-root link '%s' - link already "
                       "exists." % title)
                return
            except models.NavigationElement.DoesNotExist:
                pass

        link = models.NavigationElement.objects.create(
            title=title,
            description=description,
            url=url,
            parent=real_parent
        )
        print "Created link with title %s, origin is %d." % (link.title,
                                                             pk)
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
        document = models.Document.objects.create(
            title=title,
            file=path_for_django,
            details=description,
            public=True,
            downloads=downloads
        )
        document.created = uploaded
        document.save()
        print "Created document with title %s." % document.title

    def cleanup_people_person(self):
        for contact in self.seen_event_contacts.values():
            if contact.regularevent_set.all().count() != 0:
                continue

            if contact.scheduledevent_set.all().count() != 0:
                continue

            print "Removing unused contact %s." % contact.name

            if contact.image:
                os.remove(contact.image.file.name)

            contact.delete()

        for speaker in self.seen_sermon_speakers.values():
            if speaker.sermon_set.all().count() != 0:
                continue

            print "Removing unused speaker %s." % speaker.name()

            if speaker.image:
                os.remove(speaker.image.file.name)

            speaker.delete()

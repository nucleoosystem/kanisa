# -*- coding: utf-8 -*-
# flake8: noqa
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RegisteredUser'
        db.create_table(u'kanisa_registereduser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['RegisteredUser'])

        # Adding M2M table for field groups on 'RegisteredUser'
        m2m_table_name = db.shorten_name(u'kanisa_registereduser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('registereduser', models.ForeignKey(orm['kanisa.registereduser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['registereduser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'RegisteredUser'
        m2m_table_name = db.shorten_name(u'kanisa_registereduser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('registereduser', models.ForeignKey(orm['kanisa.registereduser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['registereduser_id', 'permission_id'])

        # Adding model 'Banner'
        db.create_table(u'kanisa_banner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('contents', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
            ('link_text', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('publish_from', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('publish_until', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=100)),
            ('visits', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['Banner'])

        # Adding model 'Block'
        db.create_table(u'kanisa_block', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('contents', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['Block'])

        # Adding model 'EventContact'
        db.create_table(u'kanisa_eventcontact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['EventContact'])

        # Adding model 'EventCategory'
        db.create_table(u'kanisa_eventcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('kanisa', ['EventCategory'])

        # Adding model 'RegularEvent'
        db.create_table(u'kanisa_regularevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from='title', unique_with=())),
            ('pattern', self.gf('recurrence.fields.RecurrenceField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('duration', self.gf('django.db.models.fields.IntegerField')(default=60)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kanisa.EventContact'], null=True, blank=True)),
            ('intro', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('autoschedule', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['RegularEvent'])

        # Adding M2M table for field categories on 'RegularEvent'
        m2m_table_name = db.shorten_name(u'kanisa_regularevent_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('regularevent', models.ForeignKey(orm['kanisa.regularevent'], null=False)),
            ('eventcategory', models.ForeignKey(orm['kanisa.eventcategory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['regularevent_id', 'eventcategory_id'])

        # Adding model 'ScheduledEventSeries'
        db.create_table(u'kanisa_scheduledeventseries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('kanisa', ['ScheduledEventSeries'])

        # Adding model 'ScheduledEvent'
        db.create_table(u'kanisa_scheduledevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kanisa.RegularEvent'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('duration', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kanisa.EventContact'], null=True, blank=True)),
            ('intro', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('series', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='events', null=True, to=orm['kanisa.ScheduledEventSeries'])),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['ScheduledEvent'])

        # Adding model 'Document'
        db.create_table(u'kanisa_document', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from='title', unique_with=())),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('downloads', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('kanisa', ['Document'])

        # Adding model 'InlineImage'
        db.create_table(u'kanisa_inlineimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from='title', unique_with=())),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['InlineImage'])

        # Adding model 'Page'
        db.create_table(u'kanisa_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from='title', unique_with=())),
            ('lead', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contents', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('draft', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['kanisa.Page'])),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('kanisa', ['Page'])

        # Adding model 'NavigationElement'
        db.create_table(u'kanisa_navigationelement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['kanisa.NavigationElement'])),
            ('require_login', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('kanisa', ['NavigationElement'])

        # Adding model 'SermonSeries'
        db.create_table(u'kanisa_sermonseries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from='title', unique_with=())),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('intro', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('passage', self.gf('kanisa.models.bible.db_field.BiblePassageField')(max_length=25, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['SermonSeries'])

        # Adding model 'SermonSpeaker'
        db.create_table(u'kanisa_sermonspeaker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forename', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from=None, unique_with=())),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['SermonSpeaker'])

        # Adding model 'Sermon'
        db.create_table(u'kanisa_sermon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from='title', unique_with=())),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('series', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kanisa.SermonSeries'], null=True, blank=True)),
            ('speaker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kanisa.SermonSpeaker'])),
            ('passage', self.gf('kanisa.models.bible.db_field.BiblePassageField')(max_length=25, null=True, blank=True)),
            ('mp3', self.gf('django.db.models.fields.files.FileField')(max_length=200, null=True, blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('transcript', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('downloads', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('podcast_downloads', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['Sermon'])

        # Adding model 'Composer'
        db.create_table(u'kanisa_composer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forename', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['Composer'])

        # Adding model 'Song'
        db.create_table(u'kanisa_song', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('kanisa', ['Song'])

        # Adding M2M table for field composers on 'Song'
        m2m_table_name = db.shorten_name(u'kanisa_song_composers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('song', models.ForeignKey(orm['kanisa.song'], null=False)),
            ('composer', models.ForeignKey(orm['kanisa.composer'], null=False))
        ))
        db.create_unique(m2m_table_name, ['song_id', 'composer_id'])

        # Adding model 'Service'
        db.create_table(u'kanisa_service', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kanisa.ScheduledEvent'], unique=True)),
            ('band_leader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kanisa.RegisteredUser'])),
        ))
        db.send_create_signal('kanisa', ['Service'])

        # Adding M2M table for field musicians on 'Service'
        m2m_table_name = db.shorten_name(u'kanisa_service_musicians')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('service', models.ForeignKey(orm['kanisa.service'], null=False)),
            ('registereduser', models.ForeignKey(orm['kanisa.registereduser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['service_id', 'registereduser_id'])

        # Adding model 'SongInService'
        db.create_table(u'kanisa_songinservice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('song', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kanisa.Song'])),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kanisa.Service'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('kanisa', ['SongInService'])

        # Adding model 'Band'
        db.create_table(u'kanisa_band', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('band_leader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kanisa.RegisteredUser'])),
        ))
        db.send_create_signal('kanisa', ['Band'])

        # Adding M2M table for field musicians on 'Band'
        m2m_table_name = db.shorten_name(u'kanisa_band_musicians')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('band', models.ForeignKey(orm['kanisa.band'], null=False)),
            ('registereduser', models.ForeignKey(orm['kanisa.registereduser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['band_id', 'registereduser_id'])

        # Adding model 'ScheduledTweet'
        db.create_table(u'kanisa_scheduledtweet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tweet', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('posted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['ScheduledTweet'])


    def backwards(self, orm):
        # Deleting model 'RegisteredUser'
        db.delete_table(u'kanisa_registereduser')

        # Removing M2M table for field groups on 'RegisteredUser'
        db.delete_table(db.shorten_name(u'kanisa_registereduser_groups'))

        # Removing M2M table for field user_permissions on 'RegisteredUser'
        db.delete_table(db.shorten_name(u'kanisa_registereduser_user_permissions'))

        # Deleting model 'Banner'
        db.delete_table(u'kanisa_banner')

        # Deleting model 'Block'
        db.delete_table(u'kanisa_block')

        # Deleting model 'EventContact'
        db.delete_table(u'kanisa_eventcontact')

        # Deleting model 'EventCategory'
        db.delete_table(u'kanisa_eventcategory')

        # Deleting model 'RegularEvent'
        db.delete_table(u'kanisa_regularevent')

        # Removing M2M table for field categories on 'RegularEvent'
        db.delete_table(db.shorten_name(u'kanisa_regularevent_categories'))

        # Deleting model 'ScheduledEventSeries'
        db.delete_table(u'kanisa_scheduledeventseries')

        # Deleting model 'ScheduledEvent'
        db.delete_table(u'kanisa_scheduledevent')

        # Deleting model 'Document'
        db.delete_table(u'kanisa_document')

        # Deleting model 'InlineImage'
        db.delete_table(u'kanisa_inlineimage')

        # Deleting model 'Page'
        db.delete_table(u'kanisa_page')

        # Deleting model 'NavigationElement'
        db.delete_table(u'kanisa_navigationelement')

        # Deleting model 'SermonSeries'
        db.delete_table(u'kanisa_sermonseries')

        # Deleting model 'SermonSpeaker'
        db.delete_table(u'kanisa_sermonspeaker')

        # Deleting model 'Sermon'
        db.delete_table(u'kanisa_sermon')

        # Deleting model 'Composer'
        db.delete_table(u'kanisa_composer')

        # Deleting model 'Song'
        db.delete_table(u'kanisa_song')

        # Removing M2M table for field composers on 'Song'
        db.delete_table(db.shorten_name(u'kanisa_song_composers'))

        # Deleting model 'Service'
        db.delete_table(u'kanisa_service')

        # Removing M2M table for field musicians on 'Service'
        db.delete_table(db.shorten_name(u'kanisa_service_musicians'))

        # Deleting model 'SongInService'
        db.delete_table(u'kanisa_songinservice')

        # Deleting model 'Band'
        db.delete_table(u'kanisa_band')

        # Removing M2M table for field musicians on 'Band'
        db.delete_table(db.shorten_name(u'kanisa_band_musicians'))

        # Deleting model 'ScheduledTweet'
        db.delete_table(u'kanisa_scheduledtweet')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'kanisa.band': {
            'Meta': {'object_name': 'Band'},
            'band_leader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kanisa.RegisteredUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'musicians': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'band_musicians'", 'symmetrical': 'False', 'to': "orm['kanisa.RegisteredUser']"})
        },
        'kanisa.banner': {
            'Meta': {'ordering': "('order', 'publish_from', '-publish_until')", 'object_name': 'Banner'},
            'contents': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'link_text': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'publish_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'publish_until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'visits': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'kanisa.block': {
            'Meta': {'ordering': "('-modified',)", 'object_name': 'Block'},
            'contents': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'kanisa.composer': {
            'Meta': {'ordering': "('surname', 'forename')", 'object_name': 'Composer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'forename': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'kanisa.document': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Document'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'downloads': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'title'", 'unique_with': '()'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'kanisa.eventcategory': {
            'Meta': {'ordering': "('title',)", 'object_name': 'EventCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'kanisa.eventcontact': {
            'Meta': {'object_name': 'EventContact'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'kanisa.inlineimage': {
            'Meta': {'object_name': 'InlineImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'title'", 'unique_with': '()'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'kanisa.navigationelement': {
            'Meta': {'object_name': 'NavigationElement'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['kanisa.NavigationElement']"}),
            'require_login': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'kanisa.page': {
            'Meta': {'object_name': 'Page'},
            'contents': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['kanisa.Page']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'title'", 'unique_with': '()'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'kanisa.registereduser': {
            'Meta': {'ordering': "('last_name', 'first_name')", 'object_name': 'RegisteredUser'},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'kanisa.regularevent': {
            'Meta': {'ordering': "('title',)", 'object_name': 'RegularEvent'},
            'autoschedule': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['kanisa.EventCategory']", 'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kanisa.EventContact']", 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '60'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'intro': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pattern': ('recurrence.fields.RecurrenceField', [], {}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'title'", 'unique_with': '()'}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'kanisa.scheduledevent': {
            'Meta': {'ordering': "('date', 'start_time')", 'object_name': 'ScheduledEvent'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kanisa.EventContact']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kanisa.RegularEvent']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'events'", 'null': 'True', 'to': "orm['kanisa.ScheduledEventSeries']"}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'kanisa.scheduledeventseries': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ScheduledEventSeries'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'kanisa.scheduledtweet': {
            'Meta': {'ordering': "('date', 'time')", 'object_name': 'ScheduledTweet'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'posted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'tweet': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'kanisa.sermon': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Sermon'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'downloads': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'mp3': ('django.db.models.fields.files.FileField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'passage': ('kanisa.models.bible.db_field.BiblePassageField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'podcast_downloads': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kanisa.SermonSeries']", 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'title'", 'unique_with': '()'}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kanisa.SermonSpeaker']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'transcript': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'kanisa.sermonseries': {
            'Meta': {'ordering': "('-active',)", 'object_name': 'SermonSeries'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'intro': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'passage': ('kanisa.models.bible.db_field.BiblePassageField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'title'", 'unique_with': '()'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'kanisa.sermonspeaker': {
            'Meta': {'ordering': "('surname', 'forename')", 'object_name': 'SermonSpeaker'},
            'forename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'kanisa.service': {
            'Meta': {'ordering': "('event__date',)", 'object_name': 'Service'},
            'band_leader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kanisa.RegisteredUser']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kanisa.ScheduledEvent']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'musicians': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'service_musicians'", 'blank': 'True', 'to': "orm['kanisa.RegisteredUser']"}),
            'songs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['kanisa.Song']", 'through': "orm['kanisa.SongInService']", 'symmetrical': 'False'})
        },
        'kanisa.song': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Song'},
            'composers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['kanisa.Composer']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'kanisa.songinservice': {
            'Meta': {'ordering': "('order',)", 'object_name': 'SongInService'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kanisa.Service']"}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kanisa.Song']"})
        }
    }

    complete_apps = ['kanisa']

# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Banner'
        db.create_table('kanisa_banner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('contents', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
            ('link_text', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('publish_from', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('publish_until', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('visits', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['Banner'])

        # Adding model 'Block'
        db.create_table('kanisa_block', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('contents', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['Block'])

        # Adding model 'EventContact'
        db.create_table('kanisa_eventcontact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['EventContact'])

        # Adding model 'RegularEvent'
        db.create_table('kanisa_regularevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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

        # Adding model 'ScheduledEvent'
        db.create_table('kanisa_scheduledevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kanisa.RegularEvent'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('duration', self.gf('django.db.models.fields.IntegerField')(default=60)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kanisa.EventContact'], null=True, blank=True)),
            ('intro', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['ScheduledEvent'])

        # Adding model 'Document'
        db.create_table('kanisa_document', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['Document'])

        # Adding model 'InlineImage'
        db.create_table('kanisa_inlineimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from='title', unique_with=())),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['InlineImage'])

        # Adding model 'Page'
        db.create_table('kanisa_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from='title', unique_with=())),
            ('lead', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('contents', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('draft', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['kanisa.Page'])),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('kanisa', ['Page'])

        # Adding model 'NavigationElement'
        db.create_table('kanisa_navigationelement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['kanisa.NavigationElement'])),
            ('require_login', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('kanisa', ['NavigationElement'])

        # Adding model 'SermonSeries'
        db.create_table('kanisa_sermonseries', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from='title', unique_with=())),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
            ('intro', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('passage', self.gf('kanisa.models.bible.db_field.BiblePassageField')(max_length=25, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['SermonSeries'])

        # Adding model 'SermonSpeaker'
        db.create_table('kanisa_sermonspeaker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forename', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from=None, unique_with=())),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['SermonSpeaker'])

        # Adding model 'Sermon'
        db.create_table('kanisa_sermon', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from='title', unique_with=())),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('series', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kanisa.SermonSeries'], null=True, blank=True)),
            ('speaker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kanisa.SermonSpeaker'])),
            ('passage', self.gf('kanisa.models.bible.db_field.BiblePassageField')(max_length=25, null=True, blank=True)),
            ('mp3', self.gf('django.db.models.fields.files.FileField')(max_length=200, null=True, blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['Sermon'])

        # Adding model 'ScheduledTweet'
        db.create_table('kanisa_scheduledtweet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tweet', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('posted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kanisa', ['ScheduledTweet'])


    def backwards(self, orm):
        # Deleting model 'Banner'
        db.delete_table('kanisa_banner')

        # Deleting model 'Block'
        db.delete_table('kanisa_block')

        # Deleting model 'EventContact'
        db.delete_table('kanisa_eventcontact')

        # Deleting model 'RegularEvent'
        db.delete_table('kanisa_regularevent')

        # Deleting model 'ScheduledEvent'
        db.delete_table('kanisa_scheduledevent')

        # Deleting model 'Document'
        db.delete_table('kanisa_document')

        # Deleting model 'InlineImage'
        db.delete_table('kanisa_inlineimage')

        # Deleting model 'Page'
        db.delete_table('kanisa_page')

        # Deleting model 'NavigationElement'
        db.delete_table('kanisa_navigationelement')

        # Deleting model 'SermonSeries'
        db.delete_table('kanisa_sermonseries')

        # Deleting model 'SermonSpeaker'
        db.delete_table('kanisa_sermonspeaker')

        # Deleting model 'Sermon'
        db.delete_table('kanisa_sermon')

        # Deleting model 'ScheduledTweet'
        db.delete_table('kanisa_scheduledtweet')


    models = {
        'kanisa.banner': {
            'Meta': {'object_name': 'Banner'},
            'contents': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'link_text': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'publish_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'publish_until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'visits': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'kanisa.block': {
            'Meta': {'ordering': "('-modified',)", 'object_name': 'Block'},
            'contents': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'kanisa.document': {
            'Meta': {'ordering': "('-modified',)", 'object_name': 'Document'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'kanisa.eventcontact': {
            'Meta': {'object_name': 'EventContact'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'kanisa.inlineimage': {
            'Meta': {'object_name': 'InlineImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'title'", 'unique_with': '()'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'kanisa.navigationelement': {
            'Meta': {'object_name': 'NavigationElement'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['kanisa.NavigationElement']"}),
            'require_login': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'kanisa.page': {
            'Meta': {'object_name': 'Page'},
            'contents': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['kanisa.Page']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'title'", 'unique_with': '()'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'kanisa.regularevent': {
            'Meta': {'ordering': "('title',)", 'object_name': 'RegularEvent'},
            'autoschedule': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kanisa.EventContact']", 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '60'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '60'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kanisa.RegularEvent']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'kanisa.scheduledtweet': {
            'Meta': {'ordering': "('date', 'time')", 'object_name': 'ScheduledTweet'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'posted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'tweet': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'kanisa.sermon': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Sermon'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'mp3': ('django.db.models.fields.files.FileField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'passage': ('kanisa.models.bible.db_field.BiblePassageField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kanisa.SermonSeries']", 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'title'", 'unique_with': '()'}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kanisa.SermonSpeaker']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'kanisa.sermonseries': {
            'Meta': {'ordering': "('-active',)", 'object_name': 'SermonSeries'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'intro': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'passage': ('kanisa.models.bible.db_field.BiblePassageField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'title'", 'unique_with': '()'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'kanisa.sermonspeaker': {
            'Meta': {'ordering': "('surname', 'forename')", 'object_name': 'SermonSpeaker'},
            'forename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['kanisa']
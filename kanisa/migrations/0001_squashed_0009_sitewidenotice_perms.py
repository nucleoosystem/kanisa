# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields
import recurrence.fields
import kanisa.models.bible.db_field
import autoslug.fields
import mptt.fields
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    replaces = [(b'kanisa', '0001_initial'), (b'kanisa', '0002_registereduser_is_spam'), (b'kanisa', '0003_increase_nav_length'), (b'kanisa', '0004_add_size_info_to_media_help'), (b'kanisa', '0005_delete_scheduledtweet'), (b'kanisa', '0006_sitewidenotice'), (b'kanisa', '0007_sitewidenotice_meta'), (b'kanisa', '0008_regularevent_mothballed'), (b'kanisa', '0009_sitewidenotice_perms')]

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisteredUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created', models.DateTimeField(null=True, editable=False, blank=True)),
                ('updated', models.DateTimeField(null=True, editable=False, blank=True)),
                ('image', sorl.thumbnail.fields.ImageField(null=True, upload_to=b'kanisa/users', blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to=b'auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to=b'auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'ordering': ('last_name', 'first_name'),
                'verbose_name': 'registered user',
                'verbose_name_plural': 'registered users',
                'permissions': (('manage_users', 'Can manage your users'),),
            },
        ),
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('band_leader', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('musicians', models.ManyToManyField(related_name='band_musicians', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('headline', models.CharField(help_text=b'Keep this short, summarise your banner in a few words.', max_length=60)),
                ('contents', models.TextField(help_text=b"At most two sentences, give extra details about what you're advertising.", null=True, blank=True)),
                ('image', sorl.thumbnail.fields.ImageField(help_text=b'Must be at least 800px by 600px.', upload_to=b'kanisa/banners/')),
                ('link_text', models.CharField(help_text=b'The text that users will click  on to visit the URL for this banner.', max_length=60, null=True, blank=True)),
                ('url', models.URLField(help_text=b'The web address your banner will link to.', null=True, verbose_name=b'URL', blank=True)),
                ('publish_from', models.DateField(help_text=b'The date at which your banner will become visible on the website. If left blank the start date is unrestricted.', null=True, blank=True)),
                ('publish_until', models.DateField(help_text=b'The final date on which your banner will be visible. If left blank your banner will be visible indefinitely.', null=True, blank=True)),
                ('order', models.IntegerField(default=100, help_text=b'Lower numbers here mean this banner will appear earlier in the list of banners.')),
                ('visits', models.IntegerField(default=0, help_text=b'The number of click-throughs this banner has had.', editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('order', 'publish_from', '-publish_until'),
                'permissions': (('manage_banners', 'Can manage your banners'),),
            },
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True)),
                ('contents', models.TextField(null=True, blank=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-modified',),
                'permissions': (('manage_blocks', 'Can manage your content blocks'),),
            },
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField(verbose_name=b'Comment')),
                ('publish_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['publish_date', 'pk'],
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('publish_date', models.DateField(help_text=b'Blog posts are published on the site at 00:00 on the publish date.')),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('teaser_text', models.TextField(help_text=b'This should normally be the first few sentences of your post.', verbose_name=b'Teaser')),
                ('main_text', models.TextField(help_text=b"This should be the bulk of your post, and will follow on from what's in the teaser.", verbose_name=b'Main text')),
                ('enable_comments', models.BooleanField(default=True, help_text=b'Comments are automatically closed 30 days after the blog post is published.')),
                ('author', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-publish_date', '-pk'],
                'permissions': (('manage_blog', 'Can manage your blog posts'),),
            },
        ),
        migrations.CreateModel(
            name='Composer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('forename', models.CharField(max_length=60)),
                ('surname', models.CharField(max_length=60)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('surname', 'forename'),
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'The name of the document.', max_length=60)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('file', models.FileField(upload_to=b'kanisa/documents')),
                ('details', models.TextField(help_text=b"Give a brief idea of what's in this document.", null=True, blank=True)),
                ('public', models.BooleanField(default=True, help_text=b'If checked, this document can be added as an attachment to publicly accessible areas of your site.')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('downloads', models.IntegerField(default=0, editable=False)),
            ],
            options={
                'ordering': ('-created',),
                'permissions': (('manage_documents', 'Can manage your documents'),),
            },
        ),
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ('title',),
                'verbose_name_plural': 'Event categories',
            },
        ),
        migrations.CreateModel(
            name='EventContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'The full name of the contact', max_length=60)),
                ('email', models.EmailField(help_text=b'Bear in mind that this will be displayed on a public website.', max_length=75)),
                ('image', sorl.thumbnail.fields.ImageField(help_text=b'Must be at least 200px by 200px', null=True, upload_to=b'kanisa/diary/contacts/', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='InlineImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'This will be used to help you find it later.', max_length=60)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('image', sorl.thumbnail.fields.ImageField(help_text=b'Image will be: <ul><li>960x200px for headline images (the image will be cropped to fit);</li><li>260x260px for medium images (resized without cropping);</li><li>174x174px for small images (resized without cropping).</li></ul>', upload_to=b'kanisa/media/')),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'permissions': (('manage_media', 'Can manage your media'),),
            },
        ),
        migrations.CreateModel(
            name='NavigationElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=40)),
                ('alternate_title', models.CharField(help_text=b'This will be used where the link is the root link, as the text for the link itself (as opposed to the dropdown menu title).', max_length=40, null=True, blank=True)),
                ('description', models.CharField(help_text=b'This will be displayed on mouseover, so should describe the linked to page in a few words.', max_length=50)),
                ('url', models.CharField(help_text=b'Should be specified relative to the domain (e.g. /sermons/, not http://www.example.com/sermons/).', max_length=200, null=True, verbose_name=b'URL', blank=True)),
                ('require_login', models.BooleanField(default=False, help_text=b'If checked, this navigation element will only be shown to users who are logged in.')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='kanisa.NavigationElement', null=True)),
            ],
            options={
                'permissions': (('manage_navigation', 'Can manage your navigation'),),
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=60)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('lead', models.TextField(help_text=b"This should be the introductory sentence or two to the page you're writing.", null=True, blank=True)),
                ('contents', models.TextField(help_text=b"This will follow the lead paragraph, so don't repeat information already entered there.", null=True, blank=True)),
                ('draft', models.BooleanField(default=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='kanisa.Page', null=True)),
            ],
            options={
                'permissions': (('manage_pages', 'Can manage your pages'),),
            },
        ),
        migrations.CreateModel(
            name='RegularEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'The name of the event.', max_length=60)),
                ('image', sorl.thumbnail.fields.ImageField(help_text=b'Must be at least 200px by 200px.', upload_to=b'kanisa/diary/events/')),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('pattern', recurrence.fields.RecurrenceField(verbose_name=b'Timetable')),
                ('start_time', models.TimeField(help_text=b'What time does the event start?')),
                ('duration', models.IntegerField(default=60, help_text=b'Duration in minutes.')),
                ('intro', models.CharField(help_text=b'Brief description (no Markdown here) of what the event is and who it is for.', max_length=200)),
                ('details', models.TextField(help_text=b'e.g. Who is this event for? What does it involve? How much does it cost? Where is it held?', null=True, blank=True)),
                ('autoschedule', models.BooleanField(default=True, help_text=b'Uncheck this to not auto-schedule this event when bulk-scheduling.', verbose_name=b'auto-schedule')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('categories', models.ManyToManyField(to=b'kanisa.EventCategory', null=True, verbose_name=b'Event Categories', blank=True)),
                ('contact', models.ForeignKey(blank=True, to='kanisa.EventContact', null=True)),
            ],
            options={
                'ordering': ('title',),
                'permissions': (('manage_diary', 'Can manage your diary'),),
            },
        ),
        migrations.CreateModel(
            name='ScheduledEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=60)),
                ('date', models.DateField()),
                ('start_time', models.TimeField(help_text=b'What time does the event start?')),
                ('duration', models.IntegerField(help_text=b'Duration in minutes (leave blank for unknown duration and for multi-day events).', null=True, blank=True)),
                ('end_date', models.DateField(help_text=b'If an end date is specified, any duration given will be ignored.', null=True, blank=True)),
                ('intro', models.CharField(help_text=b'Brief description (no Markdown here) of what the event is and who it is for.', max_length=200)),
                ('details', models.TextField(help_text=b'e.g. Who is this event for? What does it involve? How much does it cost? Where is it held?', null=True, blank=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('contact', models.ForeignKey(blank=True, to='kanisa.EventContact', null=True)),
                ('event', models.ForeignKey(blank=True, to='kanisa.RegularEvent', help_text=b'You can leave this blank, but if you do you must give the event a title.', null=True)),
            ],
            options={
                'ordering': ('date', 'start_time'),
            },
        ),
        migrations.CreateModel(
            name='ScheduledEventSeries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='SeasonalEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('season', models.CharField(max_length=1, choices=[(b'E', b'Easter'), (b'C', b'Christmas')])),
                ('title', models.CharField(max_length=60)),
                ('date', models.DateField()),
                ('start_time', models.TimeField(help_text=b'What time does the event start?')),
                ('duration', models.IntegerField(help_text=b'Duration in minutes (leave blank for unknown).', null=True, blank=True)),
                ('intro', models.CharField(help_text=b'Brief description (no Markdown here) of what the event is and who it is for.', max_length=200, blank=True)),
            ],
            options={
                'ordering': ('date', 'start_time'),
            },
        ),
        migrations.CreateModel(
            name='Sermon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'The title of the sermon.', max_length=120)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('date', models.DateField(help_text=b'The date the sermon was preached.')),
                ('passage', kanisa.models.bible.db_field.BiblePassageField(help_text=b"NB. This doesn't currently support multiple passages.", max_length=25, null=True, blank=True)),
                ('mp3', models.FileField(upload_to=b'kanisa/sermons/mp3s/%Y/', max_length=200, blank=True, help_text=b'The MP3 will automatically have ID3 data filled in (e.g. title, genre).', null=True, verbose_name=b'MP3')),
                ('details', models.TextField(help_text=b'e.g. What themes does the sermon cover?', null=True, blank=True)),
                ('transcript', models.TextField(help_text=b'For audio-impaired users - as close to a verbatim transcript as possible.', null=True, blank=True)),
                ('downloads', models.IntegerField(default=0, editable=False)),
                ('podcast_downloads', models.IntegerField(default=0, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='SermonSeries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'The name of the series.', max_length=120)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('image', sorl.thumbnail.fields.ImageField(help_text=b'This will be used in most places where the series is shown on the site. Must be at least 400px by 300px.', null=True, upload_to=b'kanisa/sermons/series/', blank=True)),
                ('intro', models.TextField(help_text=b'Sum up this series in a few sentences. In some places this may be displayed without the details section below.', null=True, blank=True)),
                ('details', models.TextField(help_text=b'e.g. What themes does the series cover?', null=True, blank=True)),
                ('active', models.BooleanField(default=True, help_text=b'Is this series currently ongoing?')),
                ('passage', kanisa.models.bible.db_field.BiblePassageField(help_text=b"NB. This doesn't currently support multiple passages.", max_length=25, null=True, blank=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-active',),
                'verbose_name_plural': 'Sermon series',
                'permissions': (('manage_sermons', 'Can manage your sermons'),),
            },
        ),
        migrations.CreateModel(
            name='SermonSpeaker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('forename', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('image', sorl.thumbnail.fields.ImageField(help_text=b'Must be at least 400px by 300px.', null=True, upload_to=b'kanisa/sermons/speakers/', blank=True)),
                ('biography', models.TextField(help_text=b'Give a brief biography of the speaker.', blank=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('surname', 'forename'),
                'verbose_name': 'Speaker',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('band_leader', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(to='kanisa.ScheduledEvent', unique=True)),
                ('musicians', models.ManyToManyField(related_name='service_musicians', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ('event__date',),
                'verbose_name': 'Service Plan',
                'permissions': (('manage_services', 'Can manage service plans'),),
            },
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('composers', models.ManyToManyField(to=b'kanisa.Composer', blank=True)),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='SongInService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=1)),
                ('service', models.ForeignKey(to='kanisa.Service')),
                ('song', models.ForeignKey(to='kanisa.Song')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Song',
            },
        ),
        migrations.AddField(
            model_name='service',
            name='songs',
            field=models.ManyToManyField(to=b'kanisa.Song', through='kanisa.SongInService'),
        ),
        migrations.AddField(
            model_name='sermon',
            name='series',
            field=models.ForeignKey(blank=True, to='kanisa.SermonSeries', help_text=b'What series the sermon is from, if any - you can add a series using <a href="/manage/sermons/series/create/">this form</a>.', null=True),
        ),
        migrations.AddField(
            model_name='sermon',
            name='speaker',
            field=models.ForeignKey(help_text=b'You can add a speaker using <a href="/manage/sermons/speaker/create/">this form</a>.', to='kanisa.SermonSpeaker'),
        ),
        migrations.AddField(
            model_name='scheduledevent',
            name='series',
            field=models.ForeignKey(related_name='events', blank=True, to='kanisa.ScheduledEventSeries', null=True),
        ),
        migrations.AddField(
            model_name='blogcomment',
            name='post',
            field=models.ForeignKey(to='kanisa.BlogPost'),
        ),
        migrations.AddField(
            model_name='registereduser',
            name='is_spam',
            field=models.BooleanField(default=False, help_text=b'Hides this user from management screens'),
        ),
        migrations.CreateModel(
            name='SiteWideNotice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('headline', models.CharField(help_text=b'Keep this short, summarise your announcement in a few words.', max_length=60)),
                ('contents', models.TextField(help_text=b'This should be a few sentences at most.')),
                ('created', models.DateField(auto_now_add=True)),
                ('publish_until', models.DateField(help_text=b'The last date on which your notice will be visible.')),
                ('published', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-publish_until',),
                'permissions': (('manage_banners', 'Can manage your banners'),),
            },
        ),
        migrations.AlterModelOptions(
            name='sitewidenotice',
            options={'ordering': ('-publish_until',), 'permissions': (('manage_sitewidenotices', 'Can manage your banners'),)},
        ),
        migrations.AddField(
            model_name='regularevent',
            name='mothballed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterModelOptions(
            name='sitewidenotice',
            options={'ordering': ('-publish_until',), 'permissions': (('manage_sitewidenotices', 'Can manage your site wide notices'),)},
        ),
    ]

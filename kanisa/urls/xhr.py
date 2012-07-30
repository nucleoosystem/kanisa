from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^passage/$',
                           'kanisa.views.xhr.check_bible_passage',
                           {},
                           'kanisa_xhr_biblepassage_check'),
                       url(r'^permissions/$',
                           'kanisa.views.xhr.assign_permission',
                           {},
                           'kanisa_management_assign_permission'),

                       )

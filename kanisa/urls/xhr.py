from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^passage/$',
                           'kanisa.views.xhr.check_bible_passage',
                           {},
                           'kanisa_xhr_biblepassage_check'),
                       url(r'^permissions/$',
                           'kanisa.views.xhr.assign_permission',
                           {},
                           'kanisa_xhr_management_assign_permission'),
                       url(r'^createpage/$',
                           'kanisa.views.xhr.create_page',
                           {},
                           'kanisa_xhr_management_create_page'),
                       )

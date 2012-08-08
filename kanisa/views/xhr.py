from datetime import datetime
from django.contrib.auth.models import User, Permission
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden)
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET
from django.views.generic import View
import json

from kanisa.models import Page, SermonSeries, RegularEvent
from kanisa.models.bible.bible import to_passage, InvalidPassage
from kanisa.utils.diary import get_schedule


class MissingArgument(Exception):
    pass


class BadArgument(Exception):
    pass


class XHRBaseView(View):
    required_arguments = []

    def check_permissions(self, request):
        if not request.is_ajax():
            return HttpResponseForbidden("This page is not directly "
                                         "accessible.")

        if hasattr(self, 'permission'):
            if not request.user.has_perm(self.permission):
                return HttpResponseForbidden("You do not have permission "
                                             "to view this page.")

    def check_required_arguments(self):
        for arg in self.required_arguments:
            if arg not in self.arguments:
                raise MissingArgument(arg)


class XHRBasePostView(XHRBaseView):
    def post(self, request, *args, **kwargs):
        self.arguments = request.POST

        response = self.check_permissions(request)

        if response:
            return response

        try:
            self.check_required_arguments()
        except MissingArgument, e:
            message = "Required argument '%s' not found." % e.message
            return HttpResponseBadRequest(message)

        try:
            return self.handle_post(request, *args, **kwargs)
        except BadArgument, e:
            return HttpResponseBadRequest(e.message)


class CheckBiblePassageView(XHRBasePostView):
    required_arguments = ['passage', ]

    def handle_post(self, request, *args, **kwargs):
        try:
            passage = to_passage(request.POST['passage'])
            return HttpResponse(unicode(passage))
        except InvalidPassage, e:
            return HttpResponseBadRequest(unicode(e))


class AssignPermissionView(XHRBasePostView):
    permission = 'kanisa.manage_users'
    required_arguments = ['permission', 'user', 'assigned', ]

    def get_user(self):
        user_pk = self.arguments['user']

        try:
            return User.objects.get(pk=user_pk)
        except (User.DoesNotExist, ValueError):
            raise BadArgument("No user found with ID %s." % user_pk)

    def get_permission(self):
        input_perm = self.arguments['permission']
        try:
            app, perm = input_perm.split('.')
        except ValueError:
            raise BadArgument("Malformed permission: '%s'." % input_perm)

        try:
            return Permission.objects.get(codename=perm)
        except Permission.DoesNotExist:
            raise BadArgument("Permission '%s' not found." % input_perm)

    def handle_post(self, request, *args, **kwargs):
        assigned = self.arguments['assigned'] == 'true'
        user = self.get_user()
        permission = self.get_permission()

        if assigned:
            user.user_permissions.add(permission)
            msg = '%s %s.' % (user, permission.name.lower())
        else:
            what = permission.name.lower().replace("can ", "can no longer ")
            user.user_permissions.remove(permission)
            msg = '%s %s.' % (user, what)

        user.save()

        return HttpResponse(msg)


class CreatePageView(XHRBasePostView):
    permission = 'kanisa.manage_pages'
    required_arguments = ['title', 'parent', ]

    def get_title(self):
        title = self.arguments['title']

        if not title:
            raise BadArgument("Title must not be empty.")

        return title

    def get_parent(self):
        parent = self.arguments['parent']

        if not parent:
            return None

        try:
            return Page.objects.get(pk=parent)
        except (Page.DoesNotExist, ValueError):
            raise BadArgument("Page with ID '%s' not found."
                              % parent)

    def handle_post(self, request, *args, **kwargs):
        title = self.get_title()
        parent = self.get_parent()

        Page.objects.create(title=title,
                            parent=parent,
                            draft=True)

        return HttpResponse("Page created.")


@require_GET
def list_pages(request):
    if not request.is_ajax():
        return HttpResponseForbidden(("This page is not directly accessible."))

    if not request.user.has_perm('kanisa.manage_pages'):
        return HttpResponseForbidden(("You do not have permission to manage "
                                      "pages."))

    pages = Page.objects.all()
    page_table = render_to_string('kanisa/management/pages/_page_table.html',
                                  {'page_list': pages},
                                  context_instance=RequestContext(request))

    tmpl = 'kanisa/management/pages/_parent_select_options.html'
    options = render_to_string(tmpl,
                               {'page_list': pages},
                               context_instance=RequestContext(request))

    response = {'page_table': page_table,
                'options': options}
    return HttpResponse(json.dumps(response))


class MarkSermonSeriesCompleteView(XHRBasePostView):
    required_arguments = ['series', ]
    permission = 'kanisa.manage_sermons'

    def get_series(self):
        try:
            series_pk = int(self.arguments['series'])
            return SermonSeries.objects.get(pk=series_pk)
        except (SermonSeries.DoesNotExist, ValueError):
            raise BadArgument("No sermon series found with ID '%s'."
                              % self.arguments['series'])

    def handle_post(self, request, *args, **kwargs):
        series = self.get_series()
        series.active = False
        series.save()
        return HttpResponse("Series marked complete.")


class ScheduleRegularEventView(XHRBasePostView):
    required_arguments = ['event', 'date', ]
    permission = 'kanisa.manage_diary'

    def get_date(self):
        try:
            event_date = datetime.strptime(self.arguments['date'], '%Y%m%d')
            return event_date
        except ValueError:
            given = self.arguments['date']
            raise BadArgument("'%s' is not a valid date." % given)

    def get_event(self):
        try:
            event_pk = int(self.arguments['event'])
            return RegularEvent.objects.get(pk=event_pk)
        except (RegularEvent.DoesNotExist, ValueError):
            raise BadArgument("No event found with ID '%s'."
                              % self.arguments['event'])

    def handle_post(self, request, *args, **kwargs):
        event_date = self.get_date()
        event = self.get_event()

        try:
            event.schedule_once(event_date)
            return HttpResponse("Event scheduled.")
        except event.AlreadyScheduled:
            return HttpResponseBadRequest("That event is already scheduled.")


@require_GET
def get_events(request, date):
    if not request.is_ajax():
        return HttpResponseForbidden(("This page is not directly accessible."))

    if not request.user.has_perm('kanisa.manage_diary'):
        return HttpResponseForbidden(("You do not have permission to manage "
                                      "the diary."))

    try:
        thedate = datetime.strptime(date, '%Y%m%d').date()
    except ValueError:
        return HttpResponseBadRequest("Invalid date '%s' provided."
                                      % date)

    schedule = get_schedule(thedate)

    tmpl = 'kanisa/management/diary/_diary_page.html'
    return render_to_response(tmpl,
                              {'calendar': schedule.calendar_entries},
                              context_instance=RequestContext(request))

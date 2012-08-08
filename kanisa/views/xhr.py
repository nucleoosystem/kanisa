from datetime import datetime
from django.contrib.auth.models import User, Permission
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden)
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import View
import json

from kanisa.models import Page, SermonSeries, RegularEvent
from kanisa.models.bible.bible import to_passage, InvalidPassage
from kanisa.utils.diary import get_schedule


class MissingArgument(Exception):
    pass


class BadArgument(Exception):
    pass


class XHRBasePostView(View):
    required_arguments = []

    def check_required_arguments(self, request):
        for arg in self.required_arguments:
            if arg not in request.POST:
                raise MissingArgument(arg)

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseForbidden("This page is not directly "
                                         "accessible.")

        if hasattr(self, 'permission'):
            if not request.user.has_perm(self.permission):
                return HttpResponseForbidden("You do not have permission "
                                             "to view this page.")

        try:
            self.check_required_arguments(request)
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


@require_POST
def assign_permission(request):
    if not request.is_ajax():
        return HttpResponseForbidden(("This page is not directly accessible."))

    if not request.user.has_perm('kanisa.manage_users'):
        return HttpResponseForbidden(("You do not have permission to manage "
                                      "users."))

    if not 'permission' in request.POST:
        return HttpResponseBadRequest("Permission ID not found.")

    if not 'user' in request.POST:
        return HttpResponseBadRequest("User ID not found.")

    if not 'assigned' in request.POST:
        return HttpResponseBadRequest("Assigned status not found.")

    input_perm = request.POST['permission']
    user_pk = request.POST['user']
    assigned = request.POST['assigned'] == 'true'

    try:
        user = User.objects.get(pk=user_pk)
    except (User.DoesNotExist, ValueError):
        return HttpResponseBadRequest("No user found with ID %s." % user_pk)

    try:
        app, perm = input_perm.split('.')
    except ValueError:
        msg = "Malformed permission: '%s'." % input_perm
        return HttpResponseBadRequest(msg)

    try:
        p = Permission.objects.get(codename=perm)
    except Permission.DoesNotExist:
        msg = "Permission '%s' not found." % input_perm
        return HttpResponseBadRequest(msg)

    if assigned:
        user.user_permissions.add(p)
        msg = '%s %s.' % (user, p.name.lower())
    else:
        what = p.name.lower().replace("can ", "can no longer ")
        user.user_permissions.remove(p)
        msg = '%s %s.' % (user, what)

    user.save()

    return HttpResponse(msg)


class CreatePageView(XHRBasePostView):
    permission = 'kanisa.manage_pages'
    required_arguments = ['title', 'parent', ]

    def get_title(self, request):
        title = request.POST['title']

        if not title:
            raise BadArgument("Title must not be empty.")

        return title

    def get_parent(self, request):
        parent = request.POST['parent']

        if not parent:
            return None

        try:
            return Page.objects.get(pk=parent)
        except (Page.DoesNotExist, ValueError):
            raise BadArgument("Page with ID '%s' not found."
                              % parent)

    def handle_post(self, request, *args, **kwargs):
        title = self.get_title(request)
        parent = self.get_parent(request)

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

    def get_series(self, request):
        try:
            series_pk = int(request.POST['series'])
            return SermonSeries.objects.get(pk=series_pk)
        except (SermonSeries.DoesNotExist, ValueError):
            raise BadArgument("No sermon series found with ID '%s'."
                              % request.POST['series'])

    def handle_post(self, request, *args, **kwargs):
        series = self.get_series(request)
        series.active = False
        series.save()
        return HttpResponse("Series marked complete.")


class ScheduleRegularEventView(XHRBasePostView):
    required_arguments = ['event', 'date', ]
    permission = 'kanisa.manage_diary'

    def get_date(self, request):
        try:
            event_date = datetime.strptime(request.POST['date'], '%Y%m%d')
            return event_date
        except ValueError:
            given = request.POST['date']
            raise BadArgument("'%s' is not a valid date." % given)

    def get_event(self, request):
        try:
            event_pk = int(request.POST['event'])
            return RegularEvent.objects.get(pk=event_pk)
        except (RegularEvent.DoesNotExist, ValueError):
            raise BadArgument("No event found with ID '%s'."
                              % request.POST['event'])

    def handle_post(self, request, *args, **kwargs):
        event_date = self.get_date(request)
        event = self.get_event(request)

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

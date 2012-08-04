from django.contrib.auth.models import User, Permission
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden)
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST, require_GET
import json

from kanisa.models import Page
from kanisa.models.bible.bible import to_passage, InvalidPassage


@require_POST
def check_bible_passage(request):
    if not request.is_ajax():
        return HttpResponseForbidden(("This page is not directly accessible."))

    if not 'passage' in request.POST:
        return HttpResponseBadRequest("Passage not found.")

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
    except User.DoesNotExist:
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


@require_POST
def create_page(request):
    if not request.is_ajax():
        return HttpResponseForbidden(("This page is not directly accessible."))

    if not request.user.has_perm('kanisa.manage_pages'):
        return HttpResponseForbidden(("You do not have permission to manage "
                                      "pages."))

    if not 'title' in request.POST:
        return HttpResponseBadRequest("Title not found.")

    if not 'parent' in request.POST:
        return HttpResponseBadRequest("Parent not found.")

    title = request.POST['title']

    if not title:
        return HttpResponseBadRequest("Title must not be empty.")

    parent = request.POST['parent']

    if not parent:
        parent = None
    else:
        try:
            parent = Page.objects.get(pk=parent)
        except Page.DoesNotExist:
            return HttpResponseBadRequest("Page with ID '%s' not found."
                                          % parent)

    Page.objects.create(title=request.POST['title'],
                        parent=parent)

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

    response = {'page_table': page_table}
    return HttpResponse(json.dumps(response))

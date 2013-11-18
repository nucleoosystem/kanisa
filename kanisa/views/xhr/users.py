from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseForbidden
from kanisa.views.xhr.base import XHRBasePostView, BadArgument


class AssignPermissionView(XHRBasePostView):
    permission = 'kanisa.manage_users'
    required_arguments = ['permission', 'user', 'assigned', ]

    def get_user(self):
        user_pk = self.arguments['user']

        try:
            return get_user_model().objects.get(pk=user_pk)
        except (ObjectDoesNotExist, ValueError):
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

    def render(self, request, *args, **kwargs):
        assigned = self.arguments['assigned'] == 'true'
        user = self.get_user()
        permission = self.get_permission()

        permission_text = self.arguments['permission']
        if not self.request.user.has_perm(permission_text):
            return HttpResponseForbidden("You do not have permission to "
                                         "grant or deny this permission.")

        if assigned:
            user.user_permissions.add(permission)
            msg = '%s %s.' % (user, permission.name.lower())
        else:
            what = permission.name.lower().replace("can ", "can no longer ")
            user.user_permissions.remove(permission)
            msg = '%s %s.' % (user, what)

        user.save()

        return HttpResponse(msg)
assign_permission = AssignPermissionView.as_view()

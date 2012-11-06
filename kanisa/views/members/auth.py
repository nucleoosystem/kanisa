from kanisa.views.generic import KanisaAuthorizationMixin


class MembersBaseView(KanisaAuthorizationMixin):
    def authorization_check(self, user):
        return user.is_active

from datetime import time
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.base import RedirectView
from kanisa.forms.social import ScheduledTweetForm
from kanisa.models import ScheduledTweet
from kanisa.utils.social import (TwitterException,
                                 post_to_twitter,
                                 get_cached_twitter_handle)
from kanisa.views.generic import (KanisaAuthorizationMixin,
                                  KanisaTemplateView,
                                  KanisaCreateView,
                                  KanisaUpdateView,
                                  KanisaDeleteView,
                                  KanisaListView)


class SocialBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Having a presence on social networks allows your Church '
                   'to communicate with people it might not otherwise reach.')
    kanisa_root_crumb = {'text': 'Social',
                         'url': reverse_lazy('kanisa_manage_social')}
    permission = 'kanisa.manage_social'
    kanisa_nav_component = 'social'

    def get_twitter_context(self):
        twitter = get_cached_twitter_handle()
        context = {}

        try:
            context['twitter_username'] = twitter.screen_name
            context['followers'] = twitter.followers_count
            context['statuses'] = twitter.statuses_count
            context['current_status'] = twitter.status
        except TwitterException, e:
            context['twitter_status'] = e.value

        return context


class SocialIndexView(SocialBaseView, KanisaTemplateView):
    template_name = 'kanisa/management/social/index.html'
    kanisa_title = 'Manage Social Networks'
    kanisa_is_root_view = True

    def get_context_data(self, **kwargs):
        context = super(SocialIndexView,
                        self).get_context_data(**kwargs)

        context.update(self.get_twitter_context())
        return context


class SocialTwitterIndexView(SocialBaseView, KanisaListView):
    kanisa_title = 'Manage Twitter'
    queryset = ScheduledTweet.future_objects.all
    template_name = 'kanisa/management/social/twitter.html'

    def get_context_data(self, **kwargs):
        context = super(SocialTwitterIndexView,
                        self).get_context_data(**kwargs)

        context.update(self.get_twitter_context())
        return context


class ScheduledTweetCreateView(SocialBaseView, KanisaCreateView):
    form_class = ScheduledTweetForm
    kanisa_title = 'Schedule Tweet'
    success_url = reverse_lazy('kanisa_manage_social_twitter')

    def get_initial(self):
        initial = super(ScheduledTweetCreateView, self).get_initial()
        initial['time'] = time(17, 0, 0)
        return initial


class ScheduledTweetUpdateView(SocialBaseView, KanisaUpdateView):
    form_class = ScheduledTweetForm
    queryset = ScheduledTweet.future_objects.all()
    success_url = reverse_lazy('kanisa_manage_social_twitter')
    kanisa_title = 'Edit Scheduled Tweet'


class ScheduledTweetDeleteView(SocialBaseView, KanisaDeleteView):
    queryset = ScheduledTweet.future_objects.all()
    kanisa_title = 'Delete Scheduled Tweet'

    def get_cancel_url(self):
        return reverse('kanisa_manage_social_twitter')

    def get_success_url(self):
        messages.success(self.request, 'Tweet deleted')
        return reverse('kanisa_manage_social_twitter')

    def get_deletion_confirmation_message(self):
        return 'Are you sure you want to delete this tweet?'

    def get_extra_context(self):
        return self.object

    def get_deletion_button_title(self):
        return 'Yes, delete this tweet'


class SocialTwitterPostView(SocialBaseView, RedirectView):
    permanent = False

    def get_redirect_url(self):
        twitter_status = self.request.POST.get('twitter-status', None)

        if not twitter_status:
            messages.error(self.request, "You must enter a Twitter status.")
            return reverse('kanisa_manage_social')

        try:
            post_to_twitter(twitter_status)
        except TwitterException, e:
            messages.error(self.request, "Error posting tweet: %s" % e.value)
            return reverse('kanisa_manage_social')

        message = 'Tweet posted.'
        messages.success(self.request, message)

        return reverse('kanisa_manage_social')

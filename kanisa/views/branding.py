import json
import os
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from kanisa.forms.branding import (LogoBrandingForm,
                                   AppleBrandingForm,
                                   FaviconBrandingForm,
                                   BrandingColoursForm)
from kanisa.views.generic import (KanisaAuthorizationMixin,
                                  KanisaTemplateView,
                                  KanisaFormView)
from sorl.thumbnail import delete


class BrandingBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Customise your site logos and icons.')
    kanisa_root_crumb = {'text': 'Branding',
                         'url': reverse_lazy('kanisa_manage_branding')}
    kanisa_title = 'Manage Branding'

    def authorization_check(self, user):
        return user.is_superuser


def get_brand_colours_filename():
    return os.path.join(settings.MEDIA_ROOT,
                        'branding',
                        'colours.json', )


def get_brand_colours():
    with open(get_brand_colours_filename(), 'r') as destination:
        return json.loads(destination.read())


def flush_brand_colours(colours):
    with open(get_brand_colours_filename(), 'w') as destination:
        destination.write(json.dumps(colours))


def ensure_branding_directory_exists():
    try:
        os.makedirs(os.path.join(settings.MEDIA_ROOT,
                                 'branding'))
    except OSError:
        pass


class BrandingManagementIndexView(BrandingBaseView,
                                  KanisaTemplateView):
    template_name = 'kanisa/management/branding/index.html'
    kanisa_is_root_view = True

    def get_context_data(self, **kwargs):
        context = super(BrandingManagementIndexView,
                        self).get_context_data(**kwargs)

        context['colours'] = get_brand_colours()

        return context


class BrandingManagementUpdateView(BrandingBaseView,
                                   KanisaFormView):
    template_name = 'kanisa/management/create.html'
    success_url = reverse_lazy('kanisa_manage_branding')
    kanisa_title = 'Update Branding'

    def get_form_class(self):
        if self.kwargs['resource'] == 'logo':
            return LogoBrandingForm

        if self.kwargs['resource'] == 'apple':
            return AppleBrandingForm

        if self.kwargs['resource'] == 'favicon':
            return FaviconBrandingForm

        raise Http404

    def get_destination_filename(self):
        resource = self.kwargs['resource']

        if resource == 'logo':
            return 'logo.jpg'

        if resource == 'apple':
            return 'apple.jpg'

        if resource == 'favicon':
            return 'favicon.ico'

    def form_valid(self, form):
        root = settings.MEDIA_ROOT

        ensure_branding_directory_exists()

        destination_name = os.path.join(root,
                                        'branding',
                                        self.get_destination_filename())

        if os.path.exists(destination_name):
            delete(os.path.join('branding',
                                self.get_destination_filename()))

        with open(destination_name, 'wb') as destination:
            for chunk in form.files['image'].chunks():
                destination.write(chunk)

        messages.success(self.request, ('Image updated - changes may take '
                                        'a few minutes to take effect.'))

        return super(BrandingManagementUpdateView,
                     self).form_valid(form)


class BrandingManagementUpdateColoursView(BrandingBaseView,
                                          KanisaFormView):
    template_name = 'kanisa/management/create.html'
    success_url = reverse_lazy('kanisa_manage_branding')
    kanisa_title = 'Update Colours'
    form_class = BrandingColoursForm

    def form_valid(self, form):
        root = settings.MEDIA_ROOT

        ensure_branding_directory_exists()

        colours = {'logo_background': form.cleaned_data['colour'], }
        flush_brand_colours(colours)

        messages.success(self.request, ('Colours updated - changes may take '
                                        'a few minutes to take effect.'))

        return super(BrandingManagementUpdateColoursView,
                     self).form_valid(form)

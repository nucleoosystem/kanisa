import os
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from kanisa.forms.branding import (
    AppleBrandingForm,
    BrandingColoursForm,
    FaviconBrandingForm,
    LogoBrandingForm,
    SeasonalBrandingForm,
    PodcastBrandingForm
)
from kanisa.utils.branding import (
    ensure_branding_directory_exists,
    flush_brand_colours,
    get_available_colours,
    get_brand_colours,
    get_branding_disk_file,
    BRANDING_COMPONENTS,
    BrandingInformation
)
from kanisa.views.generic import (
    KanisaAuthorizationMixin,
    KanisaTemplateView,
    KanisaFormView
)
from sorl.thumbnail import delete


class BrandingBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Customise your site logos and icons.')
    kanisa_root_crumb = {'text': 'Branding',
                         'url': reverse_lazy('kanisa_manage_branding')}
    kanisa_title = 'Manage Branding'
    kanisa_nav_component = 'branding'

    def authorization_check(self, user):
        return user.is_superuser


class BrandingManagementIndexView(BrandingBaseView,
                                  KanisaTemplateView):
    template_name = 'kanisa/management/branding/index.html'
    kanisa_is_root_view = True

    def get_context_data(self, **kwargs):
        context = super(BrandingManagementIndexView,
                        self).get_context_data(**kwargs)

        colour_values = get_brand_colours()
        colour_descriptions = get_available_colours()

        colours = []

        for key, value in colour_values.items():
            try:
                colours.append((value, colour_descriptions[key]))
            except KeyError:
                # We've presumably removed a colour that was once
                # defined.
                pass

        context['colours'] = colours

        return context
branding_management = BrandingManagementIndexView.as_view()


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

        if self.kwargs['resource'] == 'seasonal':
            return SeasonalBrandingForm

        if self.kwargs['resource'] == 'podcast':
            return PodcastBrandingForm

        raise Http404

    def get_destination_filename(self):
        resource = self.kwargs['resource']

        return BRANDING_COMPONENTS[resource]['filename']

    def form_valid(self, form):
        ensure_branding_directory_exists()
        brand = BrandingInformation(self.kwargs['resource'])
        brand.clear_cached_hash()

        dest_name = get_branding_disk_file(self.get_destination_filename())

        if os.path.exists(dest_name):
            delete(os.path.join('kanisa',
                                'branding',
                                self.get_destination_filename()))

        with open(dest_name, 'wb') as destination:
            for chunk in form.files['image'].chunks():
                destination.write(chunk)

        messages.success(self.request, ('Image updated - changes may take '
                                        'a few minutes to take effect.'))

        return super(BrandingManagementUpdateView,
                     self).form_valid(form)
branding_update = BrandingManagementUpdateView.as_view()


class BrandingManagementUpdateColoursView(BrandingBaseView,
                                          KanisaFormView):
    template_name = 'kanisa/management/create.html'
    success_url = reverse_lazy('kanisa_manage_branding')
    kanisa_title = 'Update Colours'
    form_class = BrandingColoursForm
    kanisa_form_warning = ("Colours must be entered as their 6 digit hex code "
                           "(including the preceding '#'), e.g. #FF00FF.")

    def get_initial(self):
        initial = super(BrandingManagementUpdateColoursView,
                        self).get_initial()
        initial.update(get_brand_colours())
        return initial

    def form_valid(self, form):
        ensure_branding_directory_exists()

        flush_brand_colours(form.cleaned_data)

        messages.success(self.request, ('Colours updated - changes may take '
                                        'a few minutes to take effect.'))

        return super(BrandingManagementUpdateColoursView,
                     self).form_valid(form)
branding_update_colours = BrandingManagementUpdateColoursView.as_view()

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from PIL import Image


class BrandingForm(forms.Form):
    image = forms.FileField()

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        css = "btn-primary btn-large btn-success"
        submit_text = 'Update Image'
        self.helper.add_input(Submit('submit',
                                     submit_text,
                                     css_class=css))
        self.helper.form_class = 'form-horizontal'

        super(BrandingForm, self).__init__(*args, **kwargs)

    def check_format(self, format):
        if format != self.expected_format:
            raise forms.ValidationError('The uploaded image must be '
                                        'a %s (the uploaded image '
                                        'was a %s).' % (self.expected_format,
                                                        format))

    def clean_image(self):
        data = self.cleaned_data['image']

        try:
            i = Image.open(self.files['image'].file)
        except IOError:
            raise forms.ValidationError('Please upload a valid image.')

        self.check_format(i.format)

        width, height = i.size

        self.check_size(width, height)

        return data


class LogoBrandingForm(BrandingForm):
    expected_format = 'JPEG'

    def __init__(self, *args, **kwargs):
        super(LogoBrandingForm, self).__init__(*args, **kwargs)
        self.fields['image'].help_text = ('Your site logo is used at the top '
                                          'of every page. It should be a JPEG '
                                          'exactly 140px high, and no wider '
                                          'than 500px.')

    def check_size(self, width, height):
        if height < 140:
            raise forms.ValidationError('The uploaded image must be at least '
                                        '140px high (the uploaded image was '
                                        '%s%s).' % (height, 'px'))


class AppleBrandingForm(BrandingForm):
    expected_format = 'JPEG'

    def __init__(self, *args, **kwargs):
        super(AppleBrandingForm, self).__init__(*args, **kwargs)
        self.fields['image'].help_text = ('The Apple icon needs to be 144px '
                                          'by 144px. This will be scaled down '
                                          'for non-retina devices to 72px by '
                                          '72px.')

    def check_size(self, width, height):
        if height != width:
            raise forms.ValidationError('The uploaded image must be exactly '
                                        'square (the uploaded image was '
                                        '%s by %s).' % (width, height))

        if height < 144:
            raise forms.ValidationError('The uploaded image must be at least '
                                        '144px high (the uploaded image was '
                                        '%s%s).' % (height, 'px'))

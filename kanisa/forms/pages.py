from django import forms
from kanisa.forms import KanisaBaseForm, EpicWidget
from kanisa.models import Page


class PageForm(KanisaBaseForm):
    class Meta:
        model = Page
        widgets = {'contents': EpicWidget(), }

    def clean_parent(self):
        parent = self.cleaned_data['parent']

        if not self.instance.pk:
            return parent

        if self.instance == parent:
            raise forms.ValidationError('A page cannot be its own parent.')

        if self.instance.is_ancestor_of(parent):
            raise forms.ValidationError('Invalid parent - cyclical '
                                        'hierarchy detected.')

        return parent

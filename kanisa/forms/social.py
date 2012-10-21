from datetime import datetime
from django import forms
from kanisa.forms import (KanisaBaseForm,
                          BootstrapDateField,
                          BootstrapTimeField)
from kanisa.forms.widgets import KanisaTinyInputWidget
from kanisa.models import ScheduledTweet


class ScheduledTweetForm(KanisaBaseForm):
    date = BootstrapDateField()
    time = BootstrapTimeField()

    def clean(self):
        cleaned_data = super(ScheduledTweetForm, self).clean()

        if self.instance.pk:
            return cleaned_data

        thedate = cleaned_data.get("date")
        thetime = cleaned_data.get("time")

        thedt = datetime.combine(thedate, thetime)
        if thedt < datetime.now():
            raise forms.ValidationError('You cannot scheduled tweets in the '
                                        'past.')

        return cleaned_data

    class Meta:
        model = ScheduledTweet
        exclude = ('posted', )
        widgets = {'tweet': KanisaTinyInputWidget(), }

from django.contrib.auth import get_user_model
from kanisa.forms import KanisaBaseModelForm, BootstrapDateField
from kanisa.forms.fields import AccountChoiceField
from kanisa.forms.widgets import KanisaMainInputWidget
from kanisa.models import BlogPost


class BlogPostForm(KanisaBaseModelForm):
    author = AccountChoiceField(
        get_user_model().objects.all(),
        required=False
    )
    publish_date = BootstrapDateField(
        help_text=('Blog posts are published on the site at 00:00 on the '
                   'publish date.')
    )

    class Meta:
        model = BlogPost
        widgets = {
            'main_text': KanisaMainInputWidget(),
            'teaser_text': KanisaMainInputWidget(),
        }

from django import forms


class KanisaMediaWidget(object):
    def _media(self):
        if hasattr(self.KanisaMedia, 'js'):
            js = self.KanisaMedia.js
        else:
            js = None

        if hasattr(self.KanisaMedia, 'css'):
            css = self.KanisaMedia.css
        else:
            css = None

        return forms.Media(css=css, js=js)
    media = property(_media)

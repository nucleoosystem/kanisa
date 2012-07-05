from django.db import models


class SearchableModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(SearchableModel, self).save(*args, **kwargs)
        from haystack import site as haystack_site
        haystack_site.get_index(self.__class__).update_object(self)

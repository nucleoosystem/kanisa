from django.template.defaultfilters import slugify
from django.db.models.fields import SlugField


class KanisaAutoSlugField(SlugField):
    def __init__(self, *args, **kwargs):
        self.populate_from = kwargs.pop('populate_from', 'title')

        kwargs['db_index'] = True
        kwargs['editable'] = False

        super(KanisaAutoSlugField, self).__init__(*args, **kwargs)

    def pre_save(self, instance, add):
        value = self.value_from_object(instance)

        if not value:
            if callable(self.populate_from):
                value = self.populate_from(instance)
            else:
                value = getattr(instance, self.populate_from)

        slug = slugify(value)

        if slug:
            slug = self.generate_unique_slug(instance, slug)

        setattr(instance, self.name, slug)

        return slug

    def generate_unique_slug(self, instance, slug):
        index_sep = '-'
        slug = slug[:self.max_length]
        original_slug = slug

        index = 1

        manager = type(instance).objects

        while True:
            lookups = dict(**{self.name: slug})
            rivals = manager.filter(**lookups).exclude(pk=instance.pk)

            if not rivals:
                # We have a unique slug
                return slug

            # We don't have a unique slug, bump the index
            index += 1

            # Check length
            tail_length = len(index_sep) + len(str(index))
            combined_length = len(original_slug) + tail_length
            if self.max_length < combined_length:
                original_slug = original_slug[:self.max_length - tail_length]

            # Re-generate the slug
            data = {
                'slug': original_slug,
                'sep': index_sep,
                'index': index
            }

            slug = '%(slug)s%(sep)s%(index)d' % data

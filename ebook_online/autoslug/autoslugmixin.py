from django.template.defaultfilters import slugify

class AutoSlugMixin(object):
    """
    """
    _slug_from = 'name'
    _slug_field = 'slug'

    def slugify(self, name):
        return slugify(name)

    def generate_slug(self):
        name = getattr(self, self._slug_from)
        return self.slugify(name)

    def update_slug(self, commit=True):
        if not getattr(self, self._slug_field) and \
               getattr(self, self._slug_from):
            setattr(self, self._slug_field, self.generate_slug())

            if commit:
                self.save()


class AutoUniqueSlugMixin(AutoSlugMixin):
    """ Make sure that the generated slug is unique. """

    def is_unique_slug(self, slug):
        qs = self.__class__.objects.filter(**{self._slug_field: slug})
        return not qs.exists()

    def generate_slug(self):
        original_slug = super(AutoUniqueSlugMixin, self).generate_slug()
        slug = original_slug

        iteration = 1
        while not self.is_unique_slug(slug):
            slug = "%s-%d" % (original_slug, iteration)
            iteration += 1

        return slug
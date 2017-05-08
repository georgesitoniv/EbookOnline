from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from autoslug.autoslugmixin import AutoUniqueSlugMixin
from filer.fields.image import FilerImageField

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    follow =  models.ManyToManyField(User, related_name="followers", symmetrical=False, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    display_image =  models.ImageField(
        upload_to='users/%Y/%m/%d',
        blank=True, null=True,
        )

    def get_absolute_url(self):
        return reverse_lazy("account:profile", kwargs={"slug": self.slug})

    def image_url(self):
        if self.display_image and hasattr(self.display_image, 'url'):
            return self.display_image.url
        else:
            return '/static/img/info.png'

    def __unicode__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.slug = self.user.username
        super(UserProfile, self).save(*args, **kwargs)

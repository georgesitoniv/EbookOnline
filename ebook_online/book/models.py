from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.core.validators import MaxValueValidator, MinValueValidator

from django_autoslug.fields import AutoSlugField
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from fields import FilerPDFField
import operator

from autoslug.autoslugmixin import AutoUniqueSlugMixin

class Author(AutoUniqueSlugMixin, models.Model):
    name = models.CharField(max_length=250, null=False, blank=False)
    description = HTMLField(max_length=2000, null=True, blank=True)
    display_image = FilerImageField(
        verbose_name="display image",
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name="author_image"
        )
    slug = models.SlugField(unique=True, null=True, blank=True)
    visitors = models.ManyToManyField(User, blank=True)

    def __unicode__(self):
        return self.name

    def image_url(self):
        if self.display_image and hasattr(self.display_image, 'url'):
            return self.display_image.url
        else:
            return '/static/img/info.png'

    def add_visitor(self, user):
        if user not in self.visitors.all():
            self.visitors.add(user)

    def get_absolute_url(self):
        return reverse_lazy("book:author_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        super(Author, self).save(*args, **kwargs)
        self.update_slug()

class Category(AutoUniqueSlugMixin, models.Model):
    name = models.CharField(max_length=250, unique=True, null=False, blank=False)
    display_image = FilerImageField(
        verbose_name="display image",
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name="category_image"
        )
    slug = models.SlugField(unique=True, null=True, blank=True)
    visitors = models.ManyToManyField(User, blank=True)

    def __unicode__(self):
        return self.name

    def image_url(self):
        if self.display_image and hasattr(self.display_image, 'url'):
            return self.display_image.url
        else:
            return '/static/img/info.png'

    def get_absolute_url(self):
        return reverse_lazy("book:category_detail", kwargs={"slug": self.slug})

    def add_visitor(self, user):
        if user not in self.visitors.all():
            self.visitors.add(user)

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        self.update_slug()

class Book(AutoUniqueSlugMixin,models.Model):
    name = models.CharField(max_length=250, unique=True, blank=False, null=False)
    author = models.ForeignKey(Author)
    category = models.ManyToManyField(Category,blank=True)
    date_published = models.DateField(blank=False, null=False)
    date_posted = models.DateField(auto_now=True)
    description = HTMLField(
        max_length=3000, blank=True, null=True,
        )
    display_image = FilerImageField(
        verbose_name="display image",
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name="book_image"
        )
    ebook_file = FilerFileField(
        verbose_name="file",
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name="ebook_file"
    )
    slug = models.SlugField(unique=True, null=True, blank=True)
    visitors = models.ManyToManyField(User, blank=True)
    is_featured = models.BooleanField(default=False, blank=True)

    def __unicode__(self):
        return self.name

    def image_url(self):
        if self.display_image and hasattr(self.display_image, 'url'):
            return self.display_image.url
        else:
            return '/static/img/info.png'

    def get_absolute_url(self):
        return reverse_lazy("book:book_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        super(Book, self).save(*args, **kwargs)
        self.update_slug()

    def get_average_rating(self):
        rating = 0
        try:
            reviews = self.review_set.all()
            if reviews:
                for review in reviews:
                    rating += review.rating
                rating /= reviews.count()
                return round(rating, 1)
        except:
            pass
        return rating

    def is_on_bookshelf(self, user, slug):
        on_bookshelf = False
        try:
            if user.bookshelf.books.get(slug=slug):
                on_bookshelf= True
        except:
            print("User has no bookshelf")

        return on_bookshelf

    def add_visitor(self, user):
        if user not in self.visitors.all():
            self.visitors.add(user)

class Review(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)
    rating = models.FloatField(
        blank=False, null=False,
        validators = [MinValueValidator(1), MaxValueValidator(5)]
    )
    content = models.CharField(max_length=1000)
    date_posted = models.DateField(auto_now=True)

    def __unicode__(self):
        return "{}: {}".format(self.user.username, self.book.name)

class BookShelf(models.Model):
    user = models.OneToOneField(User)
    books = models.ManyToManyField(Book)

    def __unicode__(self):
        return self.user.username

    def book_rank(self):
        rank = BookRanking(bookshelf=self)
        rank.populate_related_main()
        rank.evaulate_main_score()
        return rank.ranked_books()

class BookRanking:

    def __init__(self, bookshelf=None):

        self.bookshelf = bookshelf
        self.user = bookshelf.user

    def populate_related_main(self):
        self.book_list = self.bookshelf.books.all()
        self.main_book_dict = {}
        self.main_author_list = []
        self.main_category_list = []
        for book in self.book_list:
            for author_book in book.author.book_set.all():
                if author_book not in self.book_list:
                    self.main_author_list.append(author_book)
            for category in book.category.all():
                for category_book in category.book_set.all():
                    if category_book not in self.book_list:
                        self.main_category_list.append(category_book)

    def evaulate_main_score(self):
        multiplier = 6
        for book in self.main_author_list:
            if book not in self.main_book_dict:
                self.main_book_dict[book] = 0
            self.main_book_dict[book] += book.get_average_rating() * multiplier
            self.main_book_dict[book] += ((book.visitors.count() if book.visitors else 0) * multiplier)
        for book in self.main_category_list:
            if book not in self.main_book_dict:
                self.main_book_dict[book] = 0
            self.main_book_dict[book] += book.get_average_rating() * multiplier
            self.main_book_dict[book] += ((book.visitors.count() if book.visitors else 0) * multiplier)
        self.sorted_books = sorted(self.main_book_dict.items(), key=operator.itemgetter(1), reverse=True)

    def ranked_books(self):
        book_list = []
        for book in self.sorted_books:
            book_list.append(book[0])
        return book_list

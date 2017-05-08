from django.core.wsgi import get_wsgi_application
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'ebook_online.settings'
application = get_wsgi_application()

from datetime import datetime
from random import randrange

def populate_books():
    author_list = Author.objects.all()
    category_list = Category.objects.all()

    for i in range(0, 100):
        author = author_list[randrange(0, author_list.count())]
        category = category_list[randrange(0, author_list.count())]
        book = Book.objects.create(
            name="Generated Book#{}".format(i), author=author,
            date_published=datetime.now()
            )
        book.category.add(category)
        book.save()

def populate_reviews():
    book_list = Book.objects.all()
    user_list = User.objects.all()
    content_list = ["Wow", "Nice work", "Great work", "Hungry for sequels", 
        "It was ok", "Nice book", "One of my favorites", "Will reread this",
        "Page Turner!", "Unique Story!", "Wow, just wow!", "Amazing book",
        "I am addicted", "Relaxing!", "Just Great", "Nice", "Give us more books like this",
        "Worth the wait", "worth reading", "Must have a movie", "Waiting for the movie",
        "Love the work",
        ]

    for book in book_list:
        for i in range(0, 5):
            user = user_list[randrange(0, user_list.count())]
            content = content_list[randrange(0, len(content_list))]
            review = Review.objects.create(
                user=user, book=book, content=content, rating=randrange(1, 6)
            )
            print(review)

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django.settings')
    from book.models import Category, Author, Book, Review
    from django.contrib.auth.models import User
    populate_reviews()

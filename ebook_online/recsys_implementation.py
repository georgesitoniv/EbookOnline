from django.contrib.auth.models import User

from recsys.algorithm.factorize import SVD
from recsys.datamodel.data import Data
import operator

from book.models import Book

class BookRecommendation:
    
    def __init__(self, *args, **kwargs):
        book_dict = {}
        books = Book.objects.all()

        for book in books:
            book_dict[book] = set()
            book_dict[book].add(book.author)
            for category in book.category.all():
                book_dict[book].add(category)
            for visitor in book.visitors.all():
                book_dict[book].add(visitor)
            for bookshelf in book.bookshelf_set.all():
                book_dict[book].add(bookshelf.user)
        
        data = Data()
        VALUE = 1.0
        for book in book_dict:
            for book_attr in book_dict[book]:
                data.add_tuple((VALUE, book, book_attr))

        svd = SVD()
        svd.set_data(data)

        k = 100 # Usually, in a real dataset, you should set a higher number, e.g. 100
        svd.compute(k=k, min_values=3, pre_normalize=None, mean_center=False, post_normalize=True)
        self.svd = svd

    def get_similar_books_list(self, book):
        book_list = []
        book_tuple_list = self.svd.similar(book)
        for book_instance in book_tuple_list:
            if book_instance[0] != book:
                book_list.append(book_instance[0])
        return book_list
    
    def get_similar_books_tuple(self, book):
        book_tuple_list = self.svd.similar(book)
        return [i for i in book_tuple_list if i[0] != book]

    def get_user_recommended_books(self, user):
        book_list = []
        for book in user.bookshelf.books.all():
            book_list.extend(self.svd.similar(book))
        for book in user.book_set.all():
            book_list.extend(self.svd.similar(book))
        sorted_books = sorted(book_list, key=operator.itemgetter(1), reverse=True)
        book_list = list(set([book[0] for book in sorted_books]))
        for book in user.bookshelf.books.all():
            for book_list_book in book_list:
                if book_list_book == book:
                    book_list.remove(book_list_book)
        return book_list

def sort_book_on_ratings(books):
    book_dict = {}
    for book in books:
        book_dict[book] = book.get_average_rating()
    sorted_books = sorted(book_dict.items(), key=operator.itemgetter(1), reverse=True)
    return [book[0] for book in sorted_books]

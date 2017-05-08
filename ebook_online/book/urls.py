from django.conf.urls import include, url

from . import views

apipatterns = [
    url(r'^get_books/$', views.get_books, name='get_books'),
    url(r'^is_on_bookshelf/(?P<slug>[-\w]+)/$', views.is_on_bookshelf, name='is_on_bookshelf'),
    url(r'^add_to_bookshelf/(?P<slug>[-\w]+)/$', views.add_to_bookshelf, name='add_to_bookshelf'),
    url(r'^remove_from_bookshelf/(?P<slug>[-\w]+)/$', views.remove_from_bookshelf, name='remove_from_bookshelf'),
    url(r'^add_review/(?P<slug>[-\w]+)/$', views.add_review, name='add_review'),
    url(r'^get_reviews/(?P<slug>[-\w]+)/$', views.get_reviews, name='get_reviews'),
    url(r'^get_review/(?P<id>[\d]*)/$', views.get_review, name='get_review'),
    url(r'^delete_review/(?P<id>[\d]*)/$', views.delete_review, name='delete_review'),
    url(r'^update_review/(?P<id>[\d]*)/$', views.update_review, name='update_review'),
]

searchpatterns = [
    url(r'^(?P<search_term>[-\w]+)/$', views.SearchList.as_view(), name="search_list"),
    url(r'^books/(?P<search_term>[-\w]+)/$', views.BookSearchListView.as_view(), name="search_books_list"),
    url(r'^categories/(?P<search_term>[-\w]+)/$', views.CategorySearchListView.as_view(), name="search_categories_list"),
    url(r'^authors/(?P<search_term>[-\w]+)/$', views.AuthorSearchListView.as_view(), name="search_authors_list"),
]

urlpatterns = [
    url(r'^$', views.Index.as_view(), name="index"),
    url(r'^book/(?P<slug>[-\w]+)/$', views.BookDetailView.as_view(), name="book_detail"),
    url(r'^book-list/$', views.BookListView.as_view(), name="book_list"),
    url(r'^category/(?P<slug>[-\w]+)/$', views.BookListByCategoryView.as_view(), name="category_detail"),
    url(r'^category-list/$', views.CategoryListView.as_view(), name="category_list"),
    url(r'^author/(?P<slug>[-\w]+)/$', views.BookListByAuthorView.as_view(), name="author_detail"),
    url(r'^author-list/$', views.AuthorListView.as_view(), name="author_list"),
    url(r'^search/', include(searchpatterns)),
    url(r'^api/', include(apipatterns)),
]

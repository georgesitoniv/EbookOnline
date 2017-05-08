from django.shortcuts import render
from django.views.generic import View, DetailView, ListView, TemplateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.template.defaultfilters import slugify
import django.core.exceptions

import json
from braces.views import LoginRequiredMixin

from recsys_implementation import BookRecommendation, sort_book_on_ratings
from . import models
from . import forms

class AuthorListView(LoginRequiredMixin, ListView):
    model = models.Author
    template_name = "book/author_list.html"
    paginate_by = 20

class AuthorSearchListView(AuthorListView):
    def get_context_data(self, **kwargs):
        context = super(AuthorSearchListView, self).get_context_data(**kwargs)
        context["search_term"] = self.kwargs["search_term"]
        return context

    def get_queryset(self):
        return  models.Book.objects.filter(
                    Q(slug__icontains=self.kwargs["search_term"]) |
                    Q(slug__iexact=self.kwargs["search_term"])
                    )

class BookListView(LoginRequiredMixin, ListView):
    model = models.Book
    template_name = "book/book_list.html"
    paginate_by = 20

class BookSearchListView(BookListView):
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context["search_term"] = self.kwargs["search_term"] 
        return context
        
    def get_queryset(self):
        return  models.Book.objects.filter(
                    Q(slug__icontains=self.kwargs["search_term"]) |
                    Q(slug__iexact=self.kwargs["search_term"])
                    )

class BookDetailView(LoginRequiredMixin, DetailView):
    model = models.Book
    template_name = "book/book_detail.html"

    def get(self, request, *args, **kwargs):
        self.book_recommendation = BookRecommendation()
        self.user = request.user
        return super(BookDetailView, self).get(request, *args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context["book"].add_visitor(self.user)
        context["similar_books"] = self.book_recommendation.get_similar_books_list(context["book"])
        context["review_form"] = forms.ReviewForm()
        return context

class BookListByCategoryView(BookListView):
    template_name = "book/category_detail.html"
    paginate_by = 20
    category = None

    def get_queryset(self):
        self.category = models.Category.objects.get(slug=self.kwargs['slug'])
        return models.Book.objects.filter(category=self.category)
        
    def get_context_data(self, **kwargs):
        context = super(BookListByCategoryView, self).get_context_data(**kwargs)
        context["category"] = self.category
        return context

class BookListByAuthorView(BookListView):
    template_name = "book/author_detail.html"
    paginate_by = 20
    author = None

    def get_queryset(self):
        self.author = models.Author.objects.get(slug=self.kwargs['slug'])
        return models.Book.objects.filter(author=self.author)

    def get_context_data(self, **kwargs):
        context = super(BookListByAuthorView, self).get_context_data(**kwargs)
        context["author"] = self.author
        return context

class CategoryListView(LoginRequiredMixin, ListView):
    model = models.Category
    template_name = "book/category_list.html"
    paginate_by = 20

class CategorySearchListView(CategoryListView):
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context["search_term"] = self.kwargs["search_term"]
        return context

    def get_queryset(self):
        return  models.Book.objects.filter(
                    Q(slug__icontains=self.kwargs["search_term"]) |
                    Q(slug__iexact=self.kwargs["search_term"])
                    )
class Index(LoginRequiredMixin, View):
    template_name = "book/index.html"
    
    def get(self, request):
        self.book_recommendation = BookRecommendation()
        if request.GET.get('index_search_books', ""):
            return self.search(request)
        else:
            return self.view_index(request)

    def search(self, request):
        search_term = slugify(request.GET.get('index_search_books', ""))
        search_exact = exact_search(search_term)
        if search_exact:    
            return search_exact
        else:
            return HttpResponseRedirect(reverse_lazy("book:search_list", kwargs={"search_term":search_term}))
            
    def view_index(self, request):
        suggested_books = self.book_recommendation.get_user_recommended_books(request.user)
        books = models.Book.objects.all()
        context = {
            "categories" : models.Category.objects.all(),
            "books": books,
            "suggested_books": suggested_books[:10],
            "top_rated_books": sort_book_on_ratings(books)
        }
        return render(request, self.template_name, context)

class SearchList(LoginRequiredMixin, TemplateView):
    template_name = "book/base_search_results.html"

    def get_context_data(self, **kwargs):
        context = super(SearchList, self).get_context_data(kwargs)
        search_term = self.kwargs["search_term"]
        context["search_term"] = search_term
        context["category_list"] = models.Category.objects.filter(
            Q(slug__icontains=search_term) | Q(slug__iexact=search_term)
            )
        context["book_list"] = models.Book.objects.filter(
            Q(slug__icontains=search_term) | Q(slug__iexact=search_term)
            )
        context["author_list"] = models.Author.objects.filter(
            Q(slug__icontains=search_term) | Q(slug__iexact=search_term)
            )
        divisor = ((1 if context["author_list"].count() > 0  else 0)) + ((1 if context["book_list"].count() > 0  else 0)) + ((1 if context["category_list"].count() > 0  else 0))
        context["column_size"] = (12 / ((divisor if divisor > 0  else 1)))
        context["column_count"] = divisor
        return context

def exact_search(search_term):
    category = models.Category.objects.filter(slug__iexact=search_term)
    if category:
        return HttpResponseRedirect(category[0].get_absolute_url())
    author = models.Author.objects.filter(slug__iexact=search_term)
    if author:
        return HttpResponseRedirect(author[0].get_absolute_url())
    book = models.Book.objects.filter(slug__iexact=search_term)
    if book:
        return HttpResponseRedirect(book[0].get_absolute_url())
    return None

def get_books(request):
    search_term = request.GET.get('search_term')
    results = {}
    model_list = []
    model_list.extend(models.Book.objects.filter(name__icontains=search_term))
    model_list.extend(models.Category.objects.filter(name__icontains=search_term))
    model_list.extend(models.Author.objects.filter(name__icontains=search_term))
    for model in model_list:
        results[model.name] = model.get_absolute_url() + ""
    data = json.dumps(results)
    return HttpResponse(data, content_type="application/json")

def is_on_bookshelf(request, slug):
    context = {
        "is_on_bookshelf": False
        }
    try:
        if request.user.bookshelf.books.get(slug=slug):
            context["is_on_bookshelf"] = True
    except:
        print("User has no bookshelf")

    return HttpResponse(json.dumps(context), content_type="application/json")        

def add_to_bookshelf(request, slug):
    try:
        book = models.Book.objects.get(slug=slug)
        try:            
            request.user.bookshelf.books.add(book)
        except:
            models.BookShelf.objects.create(user=request.user)
            request.user.bookshelf.books.add(book)
    except:
        pass
    context = {}
    return HttpResponse(json.dumps(context), content_type="application/json")  

def remove_from_bookshelf(request, slug):
    try:
        book = request.user.bookshelf.books.get(slug=slug)
        if book:
            request.user.bookshelf.books.remove(book)
    except:
        pass
    context = {}
    return HttpResponse(json.dumps(context), content_type="application/json") 

def add_review(request, slug):
    try:
        book = models.Book.objects.get(slug=slug)
    except:
        pass
    content = request.POST.get('content', '')
    rating = request.POST.get('rating', '')
    models.Review.objects.create(
        user=request.user, book=book, 
        rating=rating, content=content
        )
    context = {}
    return HttpResponse(json.dumps(context), content_type="application/json")

def get_reviews(request, slug):
    try:
        book = models.Book.objects.get(slug=slug)
    except:
        pass
    review_dict = {}
    reviews = models.Review.objects.filter(book=book)
    for review in reviews:
        review_dict[review.id] = {
            "user": "{} {}".format(review.user.first_name, review.user.last_name),
            "rating":review.rating,
            "content":review.content,
            "date_posted":review.date_posted.strftime('%B %d, %Y'),
            "user_image": review.user.userprofile.image_url() + "",
            "user_url": review.user.userprofile.get_absolute_url() + "",
            "is_owner": review.user == request.user,
            "review_id":review.id,
        }
    context = {
        "reviews":review_dict,
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

def get_review(request, id):
    review = models.Review.objects.get(id=id)
    context = {
        "rating":review.rating,
        "content":review.content,
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

def delete_review(request, id):
    review = models.Review.objects.get(id=id)
    review.delete()
    return HttpResponse(json.dumps({}), content_type="application/json")

def update_review(request, id):
    review = models.Review.objects.get(id=id)
    review.content = request.GET.get('content', '')
    review.rating = request.GET.get('rating', '')
    review.save()
    return HttpResponse(json.dumps({}), content_type="application/json")
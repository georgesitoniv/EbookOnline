from django.contrib.auth.models import User
from recommends.providers import RecommendationProvider
from recommends.providers import recommendation_registry
from recommends.algorithms.pyrecsys import RecSysAlgorithm
from book.models import Book, Review

class BookRecommendationProvider(RecommendationProvider):
    algorithm = RecSysAlgorithm()

    def get_users(self):
        return User.objects.filter(is_active=True, votes__isnull=False).distinct()

    def get_items(self):
        return Book.objects.all()

    def get_ratings(self, obj):
        return Review.objects.filter(book=obj)

    def get_rating_score(self, rating):
        return rating.score

    def get_rating_user(self, rating):
        return rating.user

    def get_rating_item(self, rating):
        return rating.product

recommendation_registry.register(Review, [Book], BookRecommendationProvider)

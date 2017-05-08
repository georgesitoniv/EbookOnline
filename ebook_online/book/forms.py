from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

from book.models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.FloatField(
        validators = [MinValueValidator(1), MaxValueValidator(5)] 
    )
    content = forms.CharField(widget=forms.Textarea, max_length=1000)

    class Meta:
        model = Review
        fields = ('rating', 'content')
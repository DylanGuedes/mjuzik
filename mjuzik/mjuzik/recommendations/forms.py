from django import forms
from .models import Recommendation
from mjuzik.genres.models import Genre
from django_markdown.fields import MarkdownFormField
from django_markdown.widgets import MarkdownWidget
from precise_bbcode.fields import BBCodeTextField

class RecommendationForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), required=True)
    description = BBCodeTextField()

    class Meta:
        model = Recommendation
        fields = ('title', 'genres', 'description',)


from django import forms
from .models import Recommendation
from mjuzik.genres.models import Genre
from django_markdown.fields import MarkdownFormField
from django_markdown.widgets import MarkdownWidget

class RecommendationForm(forms.ModelForm):
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), required=True)
    description = forms.CharField(widget=MarkdownWidget())

    class Meta:
        model = Recommendation
        fields = ('title', 'genre', 'description',)


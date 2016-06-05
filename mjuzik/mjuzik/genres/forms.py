from django import forms
from .models import Genre
from precise_bbcode.fields import BBCodeTextField

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        description = BBCodeTextField()
        fields = ('name','description',)

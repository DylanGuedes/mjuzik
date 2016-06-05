from django.db import models
from django.contrib.auth.models import User
from mjuzik.genres.models import Genre
from mjuzik.authentication.models import Profile
from django_markdown.models import MarkdownField

class Recommendation(models.Model):
    title = models.CharField(max_length=150)
    created_by = models.ForeignKey(Profile, related_name='recommendations')
    description = MarkdownField()
    genre = models.ForeignKey(Genre, related_name='recommendations')


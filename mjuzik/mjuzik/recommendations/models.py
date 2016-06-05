from django.db import models
from django.contrib.auth.models import User
from mjuzik.genres.models import Genre
from mjuzik.authentication.models import Profile
from django_markdown.models import MarkdownField
from precise_bbcode.fields import BBCodeTextField

class Recommendation(models.Model):
    title = models.CharField(max_length=150)
    created_by = models.ForeignKey(Profile, related_name='recommendations')
    description = BBCodeTextField(max_length=200)
    genres = models.ManyToManyField(Genre, related_name='recommendations')
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(Profile, related_name='liked_recommendations')
    def __str__(self):
        return self.title


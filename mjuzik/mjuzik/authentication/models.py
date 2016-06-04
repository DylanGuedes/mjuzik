from django.db import models
from django.contrib.auth.models import User
from mjuzik.genres.models import Genre

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following_genres = models.ManyToManyField(Genre)


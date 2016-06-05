from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=200)
    created_by= models.ForeignKey(User)
    def __str__(self):
        return self.name



from django.db import models
from mjuzik.authentication.models import Profile
from precise_bbcode.fields import BBCodeTextField

class Genre(models.Model):
    name = models.CharField(max_length=200)
    description = BBCodeTextField(max_length=1000)
    created_by = models.ForeignKey(Profile)
    followed_by = models.ManyToManyField(Profile, related_name="following_genres")
    def __str__(self):
        return self.name



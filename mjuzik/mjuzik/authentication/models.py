from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to = 'mjuzik/static/img/', default = 'mjuzik/static/no-img.jpg')

    def correct_avatar_path(self):
        wrong_path = self.avatar.url
        if (wrong_path):
            splitted_path = wrong_path.split("/")
            return "/"+str(splitted_path[1])+"/"+str(splitted_path[2])+"/"+str(splitted_path[3])
        else:
            return ""

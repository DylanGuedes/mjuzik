from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to = 'mjuzik/static/img/', default = 'mjuzik/static/no-img.jpg')

    def correct_avatar_path(self):
        if self.avatar:
            wrong_path = self.avatar.url
            if (wrong_path):
                splitted_path = wrong_path.split("/")
                print("len:")
                print(len(splitted_path))
                if len(splitted_path) == 3:
                    return "/"+str(splitted_path[1])+"/"+str(splitted_path[2])
                else:
                    return "/"+str(splitted_path[1])+"/"+str(splitted_path[2])+"/"+str(splitted_path[3])
        return ""

class NewsFeed(models.Model):
    destination = models.ForeignKey(Profile, related_name='news_feeds')
    description = models.CharField(max_length=300)
    readed = models.BooleanField()
    def __str__(self):
        return self.description

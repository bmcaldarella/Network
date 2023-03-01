from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userAuthor")
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Post {self.id} made by {self.user} on {self.timestamp.strftime('%b %d %Y, %H:%M %S')}"

class perfile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    biography=models.CharField(max_length=300)

    def __str__(self):
        return f"Profile {self.user.username}"

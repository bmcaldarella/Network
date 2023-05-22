from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userAuthor")
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Post {self.id} made by {self.user} "
    
    def get_likes_count(self):
     return self.postL.count()

class perfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    biography = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(default='default.jpeg')
    ProfileBanner = models.ImageField(default='bannerDefault.jpeg')

    def __str__(self):
        return f"Profile {self.user.username}"

    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return '/path/to/default/image'
    def get_banner_url(self):
        if self.ProfileBanner and hasattr(self.ProfileBanner, 'url'):
            return self.ProfileBanner.url
        else:
            return '/path/to/default/banner'   


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        perfile.objects.create(user=instance)

class Followers(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.user} following {self.follower}"

class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="userL")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postL")

    def __str__(self):
         return f"{self.user} likePost {self.post}"




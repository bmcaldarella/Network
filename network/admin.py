from django.contrib import admin
from .models import Post,User,Followers,Like,perfile

# Register your models here.
admin.site.register(Post)
admin.site.register(User)
admin.site.register(Followers)
admin.site.register(Like)
admin.site.register(perfile)


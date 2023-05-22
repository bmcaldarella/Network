
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path("NewPost",views.NewPost,name="NewPost"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("follow", views.follow, name="follow"),
    path("followingPeople", views.followingPeople, name="followingPeople"),
    path("update_profile/", views.update_profile, name="update_profile"),
    path("editPost/<int:post_id>", views.editPost, name="editPost"),
    path("deslike/<int:post_id>", views.deslike, name="deslike"),
    path("like/<int:post_id>", views.like, name="like"),
    path("deletePost/<int:post_id>/", views.deletePost, name="deletePost"),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





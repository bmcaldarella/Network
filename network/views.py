from urllib import request
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import perfile
from .forms import PerfileUpdateForm

import json


from .models import User, Post, Followers, Like

from django import template

register = template.Library()


def deslike(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    deleteLike = Like.objects.filter(user=user, post=post)
    deleteLike.delete()
    return JsonResponse({"message": "success like remove"})


def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    nLike = Like(user=user, post=post)
    nLike.save()
    return JsonResponse({"message": "success new like"})


def index(request, user_id=None):
    if user_id is None:
        user = None
    else:
        user = User.objects.get(pk=user_id)

    if request.user.is_authenticated:
        likes = Like.objects.filter(user=request.user)
        liked = likes.values_list('post', flat=True)
    else:
        liked = []

    allpost = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(allpost, 10)
    page_number = request.GET.get('page')
    postPages = paginator.get_page(page_number)

    return render(request, "network/index.html", {
            "allpost": allpost,
            "postPages": postPages,
            "liked": liked,
            "user_profile": perfile.objects.get(user=user) if user else None,
            "username": user.username if user else None,
        })

def NewPost(request):
    if request.method == "POST":
        content = request.POST['content']
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, user=user)
        post.save()
        return HttpResponseRedirect(reverse('index'))
    
def deletePost(request,post_id):
    post=Post.objects.get(id=post_id)
    post.delete()
    return redirect(('index'))

@login_required
def profile(request, user_id):
    # Get the User object of the requested profile.
    user = User.objects.get(pk=user_id)
    # Get the Profile object associated with the requested user.
    profile = perfile.objects.get(user=user)
    # Get all the posts from the user.
    allpost = Post.objects.filter(user=user).order_by("id").reverse()
    #Get the followers and following of the user. 
    following = Followers.objects.filter(user=user)
    followers = Followers.objects.filter(follower=user)
    #Verify if the current user is following the user of the profile.
     
    try:
        trueFollow = followers.filter(user=request.user)
        followingTrue = len(trueFollow) != 0
    except:
        followingTrue = False
    # Get the list of posts liked by the current user.
    liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    # Paginate the posts.
    paginator = Paginator(allpost, 10)
    page_number = request.GET.get('page')
    postPages = paginator.get_page(page_number)
    # Create a dictionary that associates the number of likes with the ID of the post.
    likes_count_dict = {post.id: post.get_likes_count() for post in postPages if post.id in liked_posts}
    #Like a post from another user's profile.
    likes = Like.objects.all()
    liked = []
    try:
        for like in likes:
            if like.user.id == request.user.id:
                liked.append(like.post.id)
    except:
        liked = []
    # Render the template.
    return render(request, "network/profile.html", {
        "allpost": allpost,
        "postPages": postPages,
        "username": user.username,
        "following": following,
        "followers": followers,
        "followingTrue": followingTrue,
        "profileUser": user,
        "liked": liked_posts,
        "likesCount": likes_count_dict,
        "liked": liked,
        "biography": profile.biography,
        'profile': profile
    })

@login_required
def update_profile(request):
    try:
        user_profile = request.user.perfile
    except perfile.DoesNotExist:
        user_profile = perfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = PerfileUpdateForm(
            request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado!')
            return redirect('profile', user_id=request.user.id)
    else:
        form = PerfileUpdateForm(instance=user_profile)
    return render(request,"network/update_profile.html", {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def edit_view(request, id):
    # Here, some logic is performed to update an object in the database.
    # Then, we return a JSON response that contains the updated object.
    updated_object = {'id': id, 'content': request.POST['content']}
    response = JsonResponse(updated_object)
    response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    return response

@login_required
def followingPeople(request):
    user = request.user
    following = user.following.all().values_list('follower', flat=True)
    posts = Post.objects.filter(user__in=following).order_by('-timestamp')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    postPages = paginator.get_page(page_number)

    liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    likes_count_dict = {post.id: post.get_likes_count() for post in postPages if post.id in liked_posts}

    likes = Like.objects.all()
    liked = []
    try:
        for like in likes:
            if like.user.id == request.user.id:
                liked.append(like.post.id)
    except:
        liked = []

    return render(request, 'network/followingPeople.html', {
        'postPages': postPages,
        "liked": liked,
         "likesCount": likes_count_dict
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def follow(request):
    followeruser = request.POST['followeruser']
    userActuality = User.objects.get(pk=request.user.id)
    ufd = User.objects.get(username=followeruser)
    f = Followers(user=userActuality, follower=ufd)
    f.save()
    user_id = ufd.id
    return HttpResponseRedirect(reverse('profile', kwargs={'user_id': user_id}))


def unfollow(request):
    followeruser = request.POST['followeruser']
    userActuality = User.objects.get(pk=request.user.id)
    ufd = User.objects.get(username=followeruser)
    # obtain the object from the existing follower and delete it.
    follows = Followers.objects.filter(user=userActuality, follower=ufd)
    follows.delete()
    user_id = ufd.id
    return HttpResponseRedirect(reverse('profile', kwargs={'user_id': user_id}))



@login_required
def editPost(request, post_id):
    if request.method == "POST":
        text = json.loads(request.body)
        newPostEdit = Post.objects.get(pk=post_id)
        newPostEdit.content = text["content"]
        newPostEdit.save()
        return JsonResponse({"message": "success", "text": text["content"]})




def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            # Save profile and banner images
            profile_image = request.FILES.get('profile_image')
            banner_image = request.FILES.get('banner_image')
            profile = perfile.objects.get(user=user)
            if profile_image:
                profile.image = profile_image
            if banner_image:
                profile.ProfileBanner = banner_image
            profile.save()

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

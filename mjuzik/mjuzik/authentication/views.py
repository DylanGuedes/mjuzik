from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import SignupForm, EditProfileForm
from django.contrib.auth.decorators import login_required
from mjuzik.authentication.models import Profile, NewsFeed

def signin(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('genres.index')
    return render(request, 'authentication/signin.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User()
            user.username = request.POST['username']
            user.email = request.POST['email']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.password = request.POST['password1']
            c = User.objects.create_user(username=user.username, password=user.password, email=user.email)
            Profile(user=c).save()
            log_user = authenticate(username=user.username, password=user.password)
            login(request, log_user)
            return redirect('genres.index')

    return render(request, 'authentication/signup.html')

def signout(request):
    logout(request)
    return redirect('genres.index')

def profile(request):
    if request.user.is_authenticated():
        return render(request, 'authentication/profile.html')
    else:
        return render(request, 'authentication/welcome.html')

@login_required(login_url='/login')
def edit_profile(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        edit_form = EditProfileForm(request.POST, request.FILES, instance=user.profile)
        edit_form.save()
    else:
        edit_form = EditProfileForm(instance=user)
    context = {'form':edit_form}
    return render(request, 'profile/edit.html', context)

@login_required(login_url='/login')
def user_feeds(request):
    context = {'feeds': request.user.profile.news_feeds.filter(readed=False)}
    return render(request, 'profile/user_feeds.html', context)

@login_required(login_url='/login')
def read_feed(request, feed_id):
    feed = NewsFeed.objects.get(pk=feed_id)
    feed.readed = True
    feed.save()
    return user_feeds(request)

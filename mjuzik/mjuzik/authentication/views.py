from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import SignupForm
from django.contrib.auth.decorators import login_required

def signin(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        print("username:")
        print(username)
        print("pass:")
        print(password)
        user = authenticate(username=username, password=password)
        if user is not None:
            print("NOT NULLL")
            login(request, user)
            return redirect('genres.index')
        else:
            print("eh null :(")
    else:
        print("NOT POST :(")
    return render(request, 'authentication/signin.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            print("is valid")
            user = User()
            user.username = request.POST['username']
            user.email = request.POST['email']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.password = request.POST['password']
            User.objects.create_user(username=user.username, password=user.password, email=user.email)
            return redirect('genres.index')

    return render(request, 'authentication/signup.html')

def signout(request):
    logout(request)
    return redirect('genres.index')

@login_required(login_url='/login')
def profile(request):
    return render(request, 'authentication/profile.html')
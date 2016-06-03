from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm

def signin(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
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
            user = form.save(commit=False)
            user.save
            return redirect('genres.index')

    return render(request, 'authentication/signup.html')

def signout(request):
    logout(request)
    return direct('genres.index')


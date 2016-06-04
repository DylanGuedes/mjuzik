from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from mjuzik.genres.models import Genre
from .forms import GenreForm
from django.contrib.auth.models import User

def index(request):
    all_genres = Genre.objects.all()
    context = { 'genres': all_genres }
    return render(request, 'genres/index.html', context)

@login_required(login_url='/login/')
def new_genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            genre = form.save(commit=False)
            genre.save()
        return redirect('genres.index')

    else:
        form = GenreForm()
        return render(request, 'genres/new.html', { 'form': form } )

def genre_detail(request, id):
    genre = Genre.objects.get(pk=id)
    users = User.objects.all()
    return render(request, 'genres/show.html', {'genre': genre, 'users': users})
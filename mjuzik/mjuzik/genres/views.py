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
            genre.created_by = request.user.profile
            genre.save()
        return redirect('genres.index')
    else:
        form = GenreForm()
        return render(request, 'genres/new.html', { 'form': form } )

def genre_detail(request, id):
    genre = Genre.objects.get(pk=id)
    users = User.objects.all()
    return render(request, 'genres/show.html', {'genre': genre, 'users': users})

@login_required(login_url='/login')
def follow_genre(request, genre_id):
    genre = Genre.objects.get(id=genre_id)
    request.user.profile.following_genres.add(genre)
    request.user.profile.save()
    genre.save()
    return redirect('genres.index')

@login_required(login_url='/login')
def unfollow_genre(request, genre_id):
    genre = Genre.objects.get(id=genre_id)
    request.user.profile.following_genres.remove(genre)
    request.user.profile.save()
    genre.save()
    return redirect('genres.index')

@login_required(login_url='/login')
def destroy(request, genre_id):
    genre = Genre.objects.get(id=genre_id)
    if genre.created_by == request.user.profile:
        genre.delete()
    return redirect('genres.index')

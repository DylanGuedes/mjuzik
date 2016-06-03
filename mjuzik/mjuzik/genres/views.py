from django.shortcuts import render
from mjuzik.genres.models import Genre

def index(request):
    all_genres = Genre.objects.all()
    context = { 'genres': all_genres }
    return render(request, 'genres/index.html', context)

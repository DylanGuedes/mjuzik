from django.shortcuts import render, redirect
from mjuzik.recommendations.models import Recommendation
from mjuzik.recommendations.forms import RecommendationForm
from mjuzik.genres.models import Genre
from django.contrib.auth.decorators import login_required

def index(request):
    recommendations = Recommendation.objects.all()
    context = {'recommendations':recommendations}
    return render(request, 'recommendations/index.html', context)

@login_required(login_url='/login')
def new_recommendation(request):
    if request.method == 'POST':
        print("GENRE:")
        print(request.POST)
        form = RecommendationForm(request.POST)
        if form.is_valid():
            recommendation = form.save(commit=False)
            recommendation.created_by = request.user.profile
            print("RECOMMEND:")
            print(recommendation.created_by)
            recommendation.save()
        else:
            print("not valid")
            print(form.errors)
        return redirect('recommendations.index')

    else:
        form = RecommendationForm()
        return render(request, 'recommendations/new.html', { 'form': form } )



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


@login_required(login_url='/login')
def upvote(request, recommendation_id):
    recommendation = Recommendation.objects.get(id=recommendation_id)
    recommendation.likes += 1
    recommendation.liked_by.add(request.user.profile)
    print("antes do save")
    recommendation.save()
    print("lista:")
    print(recommendation.liked_by)
    print("apos o save")
    return redirect('recommendations.index')

@login_required(login_url='/login')
def downvote(request, recommendation_id):
    recommendation = Recommendation.objects.get(id=recommendation_id)
    recommendation.likes -= 1
    recommendation.liked_by.remove(request.user.profile)
    print("antes do save")
    recommendation.save()
    print("apos o save")
    return redirect('recommendations.index')


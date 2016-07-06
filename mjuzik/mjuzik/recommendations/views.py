from django.shortcuts import render, redirect
from mjuzik.recommendations.models import Recommendation
from mjuzik.recommendations.forms import RecommendationForm
from mjuzik.authentication.models import NewsFeed
from mjuzik.genres.models import Genre
from django.contrib.auth.decorators import login_required
from django.core.signals import request_finished
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
# from mjuzik import load_plugin, get_plugins, load_plugin_from_name
from mjuzik.uniquearray import run as transform_into_unique

@login_required(login_url='/login')
def index(request):
    # plugin = load_plugin_from_name("uniquearray")
    genres_ids = request.user.profile.following_genres.all().values_list('id', flat=True)
    recommendations = Recommendation.objects.filter(genres__in=genres_ids).order_by('-created_at')
    # recommendations = plugin.run(recommendations)
    recommendations = transform_into_unique(recommendations)
    context = {'recommendations':recommendations}
    return render(request, 'recommendations/index.html', context)

@login_required(login_url='/login')
def new_recommendation(request):
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            recommendation = form.save(commit=False)
            recommendation.created_by = request.user.profile
            recommendation.save()
            recommendation.genres = request.POST.getlist('genres')
            recommendation.save()
        return redirect('recommendations.index')

    else:
        form = RecommendationForm()
        return render(request, 'recommendations/new.html', { 'form': form } )

@login_required(login_url='/login')
def upvote(request, recommendation_id):
    recommendation = Recommendation.objects.get(id=recommendation_id)
    if not recommendation in request.user.profile.liked_recommendations.all():
        recommendation.likes += 1
        recommendation.liked_by.add(request.user.profile)
        recommendation.save()
    return redirect('recommendations.index')

@login_required(login_url='/login')
def downvote(request, recommendation_id):
    recommendation = Recommendation.objects.get(id=recommendation_id)
    recommendation.likes -= 1
    recommendation.liked_by.remove(request.user.profile)
    recommendation.save()
    return redirect('recommendations.index')

@login_required(login_url='/login')
def destroy(request, recommendation_id):
    recommendation = Recommendation.objects.get(id=recommendation_id)
    if request.user.profile == recommendation.created_by:
        recommendation.delete()
    return redirect('recommendations.index')

@login_required(login_url='/login')
def edit_recommendation(request, recommendation_id):
    recommendation = Recommendation.objects.get(id=recommendation_id)
    if request.user.profile == recommendation.created_by:
        return render(request, 'recommendations/edit.html')
    return redirect('recommendations.index')

@login_required(login_url='/login')
def recommendation_detail(request, recommendation_id):
    recommendation = Recommendation.objects.get(id=recommendation_id)
    context = { 'recommendation':recommendation }
    return render(request, 'recommendations/show.html', context=context)

@receiver(request_finished)
def send_feeds(sender, **kwargs):
    ...

def send_new_recommendation_feed(sender, **kwargs):
    if (kwargs.get("action")=='post_add'):
        idx = kwargs.get("pk_set").pop()
        idx_model = kwargs.get("model").objects.get(id=idx)
        for person in idx_model.followed_by.all():
            nf = NewsFeed()
            nf.destination = person
            nf.description = "A new recommendation for genre %s has been done!" % idx_model
            nf.readed = False
            nf.save()

m2m_changed.connect(send_new_recommendation_feed, sender=Genre.recommendations.through)

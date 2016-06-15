"""mjuzik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from mjuzik.genres import views as genre_views
from mjuzik.authentication import views as authentication_views
from mjuzik.recommendations import views as recommendation_views

urlpatterns = [
    url(r'^$', authentication_views.profile, name='home'),
    url(r'^follow_genre/(?P<genre_id>\d+)$', genre_views.follow_genre, name='genres.follow_genre'),
    url(r'^unfollow_genre/(?P<genre_id>\d+)$', genre_views.unfollow_genre, name='genres.unfollow_genre'),
    url(r'^recommendations/destroy/(?P<recommendation_id>\d+)$', recommendation_views.destroy, name='recommendations.destroy'),
    url(r'^recommendations/upvote/(?P<recommendation_id>\d+)$', recommendation_views.upvote, name='recommendations.upvote'),
    url(r'^recommendations/downvote/(?P<recommendation_id>\d+)$', recommendation_views.downvote, name='recommendations.downvote'),
    url(r'^recommendations/edit/(?P<recommendation_id>\d+)$', recommendation_views.edit_recommendation, name='recommendations.edit_recommendation'),
    url(r'^recommendations/$', recommendation_views.index, name='recommendations.index'),
    url(r'^recommendations/new/$', recommendation_views.new_recommendation, name='recommendations.new'),
    url(r'^recommendations/(?P<recommendation_id>\d+)/$', recommendation_views.recommendation_detail, name='recommendations.show'),
    url(r'^genres/destroy/(?P<genre_id>\d+)$', genre_views.destroy, name='genres.destroy'),
    url(r'^admin/', admin.site.urls),
    url(r'^genres/$', genre_views.index, name='genres.index'),
    url(r'^genres/new/$', genre_views.new_genre, name='genres.new'),
    url(r'^genres/(?P<id>\d+)/$', genre_views.genre_detail, name='genres.show'),
    url(r'^login/$', authentication_views.signin, name='login'),
    url(r'^signup/$', authentication_views.signup, name='signup'),
    url(r'^signout/$', authentication_views.signout, name='signout'),
    url(r'^accounts/profile/$', authentication_views.profile, name='profile'),
    url(r'^profile/edit/$', authentication_views.edit_profile, name='profile.edit'),
    url('^markdown/', include('django_markdown.urls')),
]

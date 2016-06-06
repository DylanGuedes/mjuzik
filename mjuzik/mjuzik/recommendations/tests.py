from mjuzik.genres.models import Genre
from django.test import TestCase, Client, RequestFactory
from mjuzik.recommendations.models import Recommendation
from django.contrib.auth.models import User
from mjuzik.authentication.models import Profile
from django.core.urlresolvers import reverse

class RecommendationsIndexTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username="mytest122", email="mytest@gmail.com", password="botafogo.com")
        self.user.profile = Profile()
        self.user.profile.save()
        self.user.save()

    def test_non_logged_users_must_be_redirected_on_get_index(self):
        response = self.client.get(reverse('recommendations.index'))
        self.assertEqual(response.status_code, 302)

    def test_logged_users_must_not_be_redirected(self):
        self.client.login(username=self.user.username, password="botafogo.com")
        response = self.client.get(reverse('recommendations.index'))
        self.assertEqual(response.status_code, 200)

class NewRecommendationTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username="mytest122", email="mytest@gmail.com", password="botafogo.com")
        self.user.profile = Profile()
        self.user.profile.save()
        self.user.save()
        self.genre = Genre()
        self.genre.created_by = self.user.profile
        self.genre.name = "the best genre ever"
        self.genre.description = "best genre [a] atm[/a]"
        self.genre.save()

    def test_non_logged_users_must_be_redirected(self):
        response = self.client.get(reverse('recommendations.new'))
        self.assertEqual(response.status_code, 302)

    def test_logged_users_must_not_be_redirected(self):
        self.client.login(username=self.user.username, password="botafogo.com")
        response = self.client.get(reverse('recommendations.new'))
        self.assertEqual(response.status_code, 200)

    def test_non_logged_users_must_be_redirected_on_post(self):
        recommendations_count = Recommendation.objects.count()
        recommendation = {'title':'bestsetever', 'description':'thebestdescriptionevah' }
        response = self.client.post(reverse('recommendations.new'), recommendation)
        self.assertEqual(recommendations_count, Recommendation.objects.count())

    def test_logged_users_must_increase_total_number_of_recommendations(self):
        self.client.login(username=self.user.username, password="botafogo.com")
        recommendations_count = Recommendation.objects.count()
        recommendation = {'title':'bestsetever', 'description':'thebestdescriptionevah', 'genres':['1'] }
        response = self.client.post(reverse('recommendations.new'), recommendation)
        self.assertEqual(recommendations_count+1, Recommendation.objects.count())

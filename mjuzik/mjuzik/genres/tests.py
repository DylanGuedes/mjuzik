from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from mjuzik.genres.models import Genre
from django.contrib.auth.models import User
from mjuzik.authentication.models import Profile

class NewGenreTests(TestCase):
    def setUp(self):
        self.genre = Genre()
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username="mytest122", email="mytest@gmail.com", password="botafogo.com")
        self.user.profile = Profile()
        self.user.profile.save()
        self.user.save()

    def test_genres_new_page_should_redirect_non_logged_users(self):
        response = self.client.get(reverse('genres.new'))
        self.assertEqual(response.status_code, 302)

    def test_genres_new_page_should_not_redirect_logged_users(self):
        self.client.login(username="mytest122", password="botafogo.com")
        response = self.client.get(reverse('genres.new'))
        self.assertEqual(response.status_code, 200)

    def test_genres_new_post_should_redirect_even_validated_genres(self):
        genre = {'name': 'bestgenreever', 'description': 'THEBEST[a]genre!![/a]'}
        old_genre_count = Genre.objects.count()
        response = self.client.post(reverse('genres.new'), genre)
        self.assertEqual(Genre.objects.count(), old_genre_count)
        self.assertEqual(response.status_code, 302)

    def test_genres_new_post_should_create_genre_for_logged_users(self):
        old_genre_count = Genre.objects.count()
        self.client.login(username=self.user.username, password="botafogo.com")
        genre = {'name': 'bestgenreever', 'description': 'THEBEST[a]genre!![/a]'}
        response = self.client.post(reverse('genres.new'), genre)
        self.assertEqual(Genre.objects.count(), old_genre_count+1)

    def test_genres_new_post_should_not_create_invalid_genres(self):
        old_genre_count = Genre.objects.count()
        self.client.login(username=self.user.username, password="botafogo.com")
        genre = {'description': 'THEBEST[a]genre!![/a]'}
        response = self.client.post(reverse('genres.new'), genre)
        self.assertEqual(Genre.objects.count(), old_genre_count)

class IndexGenreTests(TestCase):
    def setUp(self):
        self.genre = Genre()
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username="mytest122", email="mytest@gmail.com", password="botafogo.com")
        self.user.profile = Profile()
        self.user.profile.save()
        self.user.save()

    def test_genres_index_page_should_work_for_non_logged_users(self):
        response = self.client.get(reverse('genres.index'))
        self.assertEqual(response.status_code, 200)

class GenreDetailTests(TestCase):
    def setUp(self):
        self.genre = Genre()
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username="mytest122", email="mytest@gmail.com", password="botafogo.com")
        self.user.profile = Profile()
        self.user.profile.save()
        self.user.save()

    def test_genres_detail_should_work_even_for_non_logged_users(self):
        genre = Genre()
        genre.name = "areallynicename"
        genre.description = "[a]this genre rlz[/a]"
        genre.created_by = self.user.profile
        genre.save()
        response = self.client.get(reverse('genres.show', kwargs = {'id':genre.id} ))
        self.assertEqual(response.status_code, 200)

class FollowGenreTests(TestCase):
    def setUp(self):
        self.genre = Genre()
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username="mytest122", email="mytest@gmail.com", password="botafogo.com")
        self.user.profile = Profile()
        self.user.profile.save()
        self.user.save()

    def test_non_logged_users_must_be_redirected_if_get_follow_genre(self):
        genre = Genre()
        genre.name = "areallynicename"
        genre.description = "[a]this genre rlz[/a]"
        genre.created_by = self.user.profile
        genre.save()
        followed_genres_count = self.user.profile.following_genres.count()
        response = self.client.get(reverse('genres.follow_genre', kwargs = {'genre_id':genre.id} ))
        self.assertEqual(followed_genres_count, self.user.profile.following_genres.count())

    def test_logged_users_must_get_new_followed_genre(self):
        self.client.login(username="mytest122", password="botafogo.com")
        genre = Genre()
        genre.name = "areallynicename"
        genre.description = "[a]this genre rlz[/a]"
        genre.created_by = self.user.profile
        genre.save()
        followed_genres_count = self.user.profile.following_genres.count()
        response = self.client.get(reverse('genres.follow_genre', kwargs = {'genre_id':genre.id} ))
        self.assertEqual(followed_genres_count+1, self.user.profile.following_genres.count())

class UnfollowGenreTests(TestCase):
    def setUp(self):
        self.genre = Genre()
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username="mytest122", email="mytest@gmail.com", password="botafogo.com")
        self.user.profile = Profile()
        self.user.profile.save()
        self.user.save()

    def test_non_logged_users_must_be_redirected_if_get_unfollow_genre(self):
        genre = Genre()
        genre.name = "areallynicename"
        genre.description = "[a]this genre rlz[/a]"
        genre.created_by = self.user.profile
        genre.save()
        followed_genres_count = self.user.profile.following_genres.count()
        response = self.client.get(reverse('genres.unfollow_genre', kwargs = {'genre_id':genre.id} ))
        self.assertEqual(followed_genres_count, self.user.profile.following_genres.count())

    def test_logged_users_must_get_less_one_followed_genre(self):
        self.client.login(username="mytest122", password="botafogo.com")
        genre = Genre()
        genre.name = "areallynicename"
        genre.description = "[a]this genre rlz[/a]"
        genre.created_by = self.user.profile
        genre.save()
        response = self.client.get(reverse('genres.follow_genre', kwargs = {'genre_id':genre.id} ))
        initial_genres_count = 1
        self.assertEqual(self.user.profile.following_genres.count(), initial_genres_count)
        response = self.client.get(reverse('genres.unfollow_genre', kwargs = {'genre_id':genre.id} ))
        self.assertEqual(self.user.profile.following_genres.count(), initial_genres_count-1)

    def test_unfollow_must_not_affect_non_followed_genre(self):
        self.client.login(username="mytest122", password="botafogo.com")
        genre = Genre()
        genre.name = "areallynicename"
        genre.description = "[a]this genre rlz[/a]"
        genre.created_by = self.user.profile
        genre.save()
        initial_genres_count = 0
        self.assertEqual(self.user.profile.following_genres.count(), initial_genres_count)
        response = self.client.get(reverse('genres.unfollow_genre', kwargs = {'genre_id':genre.id} ))
        self.assertEqual(self.user.profile.following_genres.count(), initial_genres_count)



from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from mjuzik.authentication.models import Profile
from django.core.urlresolvers import reverse

class SigninTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username="mytest122", email="mytest@gmail.com", password="botafogo.com")
        self.user.profile = Profile()
        self.user.profile.save()
        self.user.save()

    def test_get_signin_should_work(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_signin_must_authenticate_user(self):
        myuser = {'username': 'mytest122', 'password': 'botafogo.com' }
        response = self.client.post(reverse('login'), myuser)
        self.assertEqual(self.user.is_authenticated(), True)

class SignupTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username="mytest122", email="mytest@gmail.com", password="botafogo.com")
        self.user.profile = Profile()
        self.user.profile.save()
        self.user.save()

    def test_get_signup_should_work(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_with_correct_data_should_increase_total_number_of_users(self):
        old_user_count = User.objects.count()
        myuser = {'username': 'mytest1224', 'password1': 'mynewawezomepass', 'password2': 'mynewawezomepass', 'email': 'djmggzzzz@gmail.com', 'first_name': 'thebestfirstname', 'last_name': 'thebestlastname' }
        response = self.client.post(reverse('signup'), myuser)
        self.assertEqual(User.objects.count(), old_user_count+1)

    def test_signup_with_incorrect_data_should_not_increase_total_number_of_users(self):
        old_user_count = User.objects.count()
        myuser = {'username': '', 'email': 'mytest@gmail.com', 'first_name': 'thebestfirstname', 'last_name': 'thebestlastname' }
        response = self.client.post(reverse('signup'), myuser)
        self.assertEqual(User.objects.count(), old_user_count)

    def test_signup_with_correct_data_should_also_signin_user(self):
        myuser = {'username': '', 'email': 'mytest@gmail.com', 'first_name': 'thebestfirstname', 'last_name': 'thebestlastname' }
        response = self.client.post(reverse('signup'), myuser)
        self.assertEqual(User.objects.last().is_authenticated(), True)


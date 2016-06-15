from django import forms
from django.contrib.auth.models import User
from mjuzik.authentication.models import Profile
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    pass

class EditProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('avatar',)


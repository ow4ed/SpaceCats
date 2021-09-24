from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator, MinValueValidator

from .models import User, Galaxy, Star
from space.models import Post, Comment

class AccountRegisterForm(UserCreationForm):
    email = forms.EmailField()
    cats = forms.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])

    class Meta:
        model = User
        fields = ['username', 'cats', 'email', 'password1', 'password2']

class PostGalaxyForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content']

class PostStarsForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['stars', 'title', 'image']

class AccountUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    cats = forms.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])

    class Meta:
        model = User
        fields = ['cats', 'email']

class GalaxyUpdateForm(forms.ModelForm):

    class Meta:
        model = Galaxy
        fields = ['image']

class StarUpdateForm(forms.ModelForm):

    class Meta:
        model = Star
        fields = ['name', 'image']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']

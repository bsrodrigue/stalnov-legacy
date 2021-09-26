from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import StallionUser, Novel

class CommentForm(forms.Form):
    content = forms.CharField()

class NovelForm(forms.Form):
    title = forms.CharField(label="Titre", max_length=100)
    cover = forms.ImageField(required=False)
    description = forms.CharField(label="Description")
    genre = forms.ChoiceField(choices=Novel.GENRES)
    public = forms.BooleanField(label="Rendre public", required=False)
    default_cover = forms.CharField(label='Couverture par defaut', required=False)

class ChapterForm(forms.Form):
    title = forms.CharField(label="Titre", max_length=100)
    content = forms.CharField(label="Contenu")
    public = forms.BooleanField(label="Rendre public", required=False)
    order = forms.IntegerField(label="Ordre")

class StallionUserCreationForm(UserCreationForm):
    class Meta:
        model = StallionUser
        fields = ("firstname", "lastname", "username",
                  "email", "bio", "gender")


class StallionUserChangeForm(UserChangeForm):
    class Meta:
        model = StallionUser
        fields = ("username", "email")

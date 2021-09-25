from django import forms
from .models import Novel

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
    order = forms.IntegerField(label="Ordre", required=True)

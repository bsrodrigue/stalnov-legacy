from django.db import models
from . import Novel

class NovelGenre(models.Model):
    title = models.CharField(max_length=256, default='Inconnu')

    def get_novels(self):
        return Novel.objects.filter(genre=self)

    def __str__(self):
        return self.title

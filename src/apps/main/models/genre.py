from django.db import models

class NovelGenre(models.Model):
    title = models.CharField(max_length=256, default='Inconnu')

    def __str__(self):
        return self.title

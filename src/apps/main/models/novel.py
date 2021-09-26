from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from .chapter import Chapter
from ..managers import AccessibleNovelManager

class Novel(models.Model):
    class Meta:
        ordering = ['publication_date']

    GENRES = [
        ("Inconnu", "Inconnu"),
        ("Fantasy", "Fantasy"),
        ("Aventure", "Aventure"),
        ("Romance", "Romance"),
        ("Horreur", "Horreur"),
        ("Action", "Action"),
        ("Historique", "Historique"),
        ("Nouvelles", "Nouvelles"),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    cover = models.ImageField(
        upload_to="novel_covers", default="novel_covers/defaults/default1.png"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateField(blank=True, null=True)
    mature = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    genre = models.CharField(choices=GENRES, max_length=30, default="Inconnu")
    objects = models.Manager()
    accessible_novels = AccessibleNovelManager()

    def get_readers(self):
        return get_user_model().objects.filter(library=self)

    def get_chapters(self):
        chapters = Chapter.objects.filter(novel=self)
        return chapters

    def get_chapter_count(self):
        return self.get_chapters().count()

    def get_public_chapters(self):
        chapters = Chapter.objects.filter(public=True, novel=self)
        return chapters

    def get_likes(self):
        chapters = self.get_chapters()
        likes = 0
        for chapter in chapters:
            likes += chapter.get_likes()
        return likes

    def get_comment_count(self):
        chapters = self.get_chapters()
        comments = 0
        for chapter in chapters:
            comments += chapter.get_comments().count()
        return comments

    def is_accessible(self):
        return self.public and self.get_public_chapters().exists()

    def __str__(self):
        return self.title



from django.db import models
from django.conf import settings


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chapter = models.ForeignKey("Chapter", on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"User '{self.author.username}' commented Chapter '{self.chapter.title}' from Novel '{self.chapter.novel.title}'"

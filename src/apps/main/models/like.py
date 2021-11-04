from django.db import models
from django.conf import settings


class Like(models.Model):
    liker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    chapter = models.ForeignKey(
        "Chapter",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.liker.username} likes {self.chapter.title} from {self.chapter.novel.title}"

from django.db import models
from .like import Like
from .comment import Comment
from django.contrib.auth import get_user_model


class Chapter(models.Model):
    class Meta:
        ordering = ["order"]

    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    publication_date = models.DateField(blank=True, null=True)
    reads = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)
    public = models.BooleanField(default=False)

    novel = models.ForeignKey(
        "Novel",
        on_delete=models.CASCADE,
    )

    def get_likes(self):
        likes = Like.objects.filter(chapter=self)
        return likes.count()

    def is_liked_by(self, user_id):
        user = get_user_model().objects.get(pk=user_id)
        return Like.objects.filter(liker=user, chapter=self).exists()

    def get_comments(self):
        comments = Comment.objects.filter(chapter=self)
        return comments

    def is_accessible(self):
        return self.public and self.novel.public

    def __str__(self):
        return f"{self.novel}:{self.title}"

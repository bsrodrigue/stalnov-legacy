from django import template
from ..models import Novel, Chapter, Like
from django.contrib.auth import get_user_model

register = template.Library()


@register.filter(name="is_already_in_library")
def is_already_in_library(novelId, userId):
    user = get_user_model().objects.get(pk=userId)
    return user.library.filter(pk=novelId).exists()


@register.filter(name="is_my_novel")
def is_my_novel(novelId, userId):
    novel = Novel.objects.get(pk=novelId)
    author = novel.author
    return author.id == userId


@register.filter(name="novel_likes")
def novel_likes(novelId):
    novel = Novel.objects.get(pk=novelId)
    return novel.get_likes()


@register.filter(name="chapter_likes")
def chapter_likes(chapter_id):
    chapter = Chapter.objects.get(pk=chapter_id)
    return chapter.get_likes()


@register.filter(name="chapter_comments")
def chapter_comments(chapter_id):
    chapter = Chapter.objects.get(pk=chapter_id)
    return chapter.get_comments().count()


@register.filter(name="novel_chapters")
def novel_chapters(novelId):
    novel = Novel.objects.get(pk=novelId)
    return novel.get_chapter_count()


@register.filter(name="novel_public_chapters")
def novel_public_chapters(novelId):
    novel = Novel.objects.get(pk=novelId)
    return novel.get_public_chapters().count()


@register.filter(name="novel_comments")
def novel_comments(novelId):
    novel = Novel.objects.get(pk=novelId)
    return novel.get_comment_count()


@register.filter(name="is_already_liked")
def is_already_liked(chapter_id, user_id):
    return Like.objects.filter(chapter=chapter_id, liker=user_id).exists()

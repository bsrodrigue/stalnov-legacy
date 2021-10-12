from django.db import models
from django.views.generic.base import View
from .chapter import Chapter
from .novel import Novel
from .like import Like
from .comment import Comment
from django.contrib.auth.models import AbstractUser
from apps.main.decorators import *


class StallionUser(AbstractUser):
    GENDERS = (
        ("H", "Homme"),
        ("F", "Femme"),
    )

    firstname = models.CharField(max_length=256, default="", blank=True)
    lastname = models.CharField(max_length=256, default="", blank=True)
    bio = models.CharField(max_length=512, default="", blank=True)
    gender = models.CharField(
        max_length=256, choices=GENDERS, default="Homme", blank=True)
    library = models.ManyToManyField('Novel', blank=True)

    def get_works(self):
        return Novel.objects.filter(author=self)

    def create_novel(self, **kwargs):
        return Novel.objects.create(author=self, **kwargs)
    
    def __str__(self):
        return self.username

    @must_be_the_author('Novel')
    @notify_readers('delete_novel')
    def delete_novel(self, novel_id):
        novel = Novel.objects.get(pk=novel_id)
        novel.delete()

    @must_be_the_author('Novel')
    @notify_readers('edit_novel')
    def edit_novel(self, novel_id, **kwargs):
        novel = Novel.objects.get(pk=novel_id)
        novel.title = kwargs.get("title", novel.title)
        novel.description = kwargs.get(
            "description", novel.description
        )
        novel.genre = kwargs.get("genre", novel.genre)
        novel.public = kwargs.get("public", novel.public)
        novel.mature = kwargs.get("mature", novel.mature)

        if kwargs.get('cover'):
            novel.cover = kwargs.get('cover')

        novel.save()
        return novel

    @must_be_the_author('Novel')
    @notify_readers('publish_novel')
    def publish_novel(self, novel_id):
        novel = Novel.objects.get(pk=novel_id)
        novel.public = True
        novel.save()
        return novel

    @must_be_the_author('Novel')
    @notify_readers('unpublish_novel')
    def unpublish_novel(self, novel_id):
        novel = Novel.objects.get(pk=novel_id)
        novel.public = False
        novel.save()
        return novel

    @must_be_the_author('Chapter')
    @notify_readers('publish_chapter')
    def publish_chapter(self, chapter_id):
        chapter = Chapter.objects.get(pk=chapter_id)
        chapter.public = True
        chapter.save()
        return chapter

    @must_be_the_author('Chapter')
    @notify_readers('unpublish_chapter')
    def unpublish_chapter(self, chapter_id):
        chapter = Chapter.objects.get(pk=chapter_id)
        chapter.public = False
        chapter.save()
        return chapter

    @must_be_public('Novel')
    def add_to_library(self, novel_id):
        novel = Novel.objects.get(pk=novel_id)
        if novel in self.library.all():
            raise AlreadyInLibraryException

        self.library.add(novel)
        self.save()

    def remove_from_library(self, novel_id):
        novel = Novel.objects.get(pk=novel_id)
        if novel not in self.library.all():
            raise NotInLibraryException
        self.library.remove(novel)
        self.save()

    @must_be_the_author('Novel')
    def create_chapter(self, novel_id, **kwargs):
        novel = Novel.objects.get(pk=novel_id)
        new_chapter = Chapter.objects.create(
            novel=novel, **kwargs
        )
        new_chapter.reads = 0
        new_chapter.save()
        return new_chapter

    @must_be_the_author('Chapter')
    @notify_readers('delete_chapter')
    def delete_chapter(self, chapter_id):
        chapter = Chapter.objects.get(pk=chapter_id)
        chapter.delete()

    @must_be_the_author('Chapter')
    @notify_readers('edit_chapter')
    def edit_chapter(self, chapter_id, **kwargs):
        chapter = Chapter.objects.get(pk=chapter_id)
        chapter.title = kwargs.get("title", chapter.title)
        chapter.public = kwargs.get("public", chapter.public)
        chapter.content = kwargs.get("content", chapter.content)
        chapter.order = kwargs.get("order", chapter.order)
        chapter.save()
        return chapter

    @must_be_public('Chapter')
    @notify_author('like')
    def like_chapter(self, chapter_id):
        chapter = Chapter.objects.get(pk=chapter_id)
        if Like.objects.filter(liker=self, chapter=chapter).exists():
            raise AlreadyLikedException
        Like.objects.create(liker=self, chapter=chapter)

    @must_be_public('Chapter')
    @notify_author('unlike')
    def unlike_chapter(self, chapter_id):
        chapter = Chapter.objects.get(pk=chapter_id)
        if not Like.objects.filter(liker=self, chapter=chapter).exists():
            raise NotLikedYetException
        like = Like.objects.get(liker=self, chapter=chapter)
        like.delete()

    @must_be_public('Chapter')
    @notify_author('comment')
    def comment_chapter(self, chapter_id, message):
        chapter = Chapter.objects.get(pk=chapter_id)
        comment = Comment.objects.create(
            author=self, chapter=chapter, content=message)
        return comment

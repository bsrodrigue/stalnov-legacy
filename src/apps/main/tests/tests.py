from django.test import TestCase
from ..models import StallionUser as User, Novel, Chapter, Like
from notifications.models import Notification

# Exceptions
from ..exceptions import NotYourNovelException, AlreadyInLibraryException, IsNotPublicException, AlreadyLikedException, NotLikedYetException, NotInLibraryException

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            username="john",
            password="l33tPa55word",
            email="john@ecorp.com",
            bio="Just a sweet person",
            firstname="john",
            lastname="doe",
            gender="Homme",
        )

    def test_user_creation(self):
        user = User.objects.get(username="john")
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.username, "john")
        self.assertEqual(user.email, "john@ecorp.com")
        self.assertEqual(user.bio, "Just a sweet person")
        self.assertEqual(user.firstname, "john")
        self.assertEqual(user.lastname, "doe")
        self.assertEqual(user.gender, "Homme")

class NotificationTestCase(TestCase):
    def setUp(self):
        self.john = User.objects.create(username='john')
        self.ismael = User.objects.create(username='ismael')

    def test_author_is_notified_when_chapter_is_liked(self):
        novel = self.john.create_novel(title='Novel', public=True)
        chapter = self.john.create_chapter(
            novel.id, title='Chapter', public=True)
        self.ismael.like_chapter(chapter.id)
        self.assertTrue(Notification.objects.filter(recipient=chapter.novel.author,
                                                    verb=f"{self.ismael.username} aime votre chapitre {chapter.title}").exists())

    def test_author_is_notified_when_chapter_is_unliked(self):
        novel = self.john.create_novel(title='Novel', public=True)
        chapter = self.john.create_chapter(
            novel.id, title='Chapter', public=True)
        self.ismael.like_chapter(chapter.id)
        self.ismael.unlike_chapter(chapter.id)
        self.assertTrue(Notification.objects.filter(recipient=chapter.novel.author,
                                                    verb=f"{self.ismael.username} n'aime plus votre chapitre {chapter.title}").exists())

    def test_author_is_notified_when_chapter_commented(self):
        novel = self.john.create_novel(title='Novel', public=True)
        chapter = self.john.create_chapter(
            novel.id, title='Chapter', public=True)
        self.ismael.comment_chapter(chapter.id, "This chapter was fire!!!!")
        self.assertTrue(Notification.objects.filter(recipient=chapter.novel.author,
                                                    verb=f"{self.ismael.username} a commente votre chapitre {chapter.title}").exists())

    def test_user_is_notified_when_library_novel_is_updated(self):
        novel = self.john.create_novel(title='Novel', public=True)
        chapter = self.john.create_chapter(
            novel.id, title='Chapter', public=True)
        self.ismael.add_to_library(novel.id)
        novel = self.john.edit_novel(novel.id, title='New Title')
        self.assertTrue(Notification.objects.filter(recipient=self.ismael,
                                                    verb=f"L'auteur {self.john.username} a modifie les informations sur son livre {novel.title}").exists())

    def test_user_is_notified_when_library_novel_is_deleted(self):
        novel = self.john.create_novel(title='Novel', public=True)
        chapter = self.john.create_chapter(
            novel.id, title='Chapter', public=True)
        self.ismael.add_to_library(novel.id)
        self.john.delete_novel(novel.id)
        self.assertTrue(Notification.objects.filter(recipient=self.ismael,
                                                    verb=f"L'auteur {self.john.username} a supprime son livre {novel.title}").exists())

    def test_user_is_notified_when_library_novel_is_republished(self):
        novel = self.john.create_novel(title='Novel', public=True)
        chapter = self.john.create_chapter(
            novel.id, title='Chapter', public=True)
        self.ismael.add_to_library(novel.id)
        self.john.unpublish_novel(novel.id)
        self.john.publish_novel(novel.id)
        self.assertTrue(Notification.objects.filter(recipient=self.ismael,
                                                    verb=f"L'auteur {self.john.username} a rendu public son livre {novel.title}").exists())

    def test_user_is_notified_when_library_novel_is_unpublished(self):
        novel = self.john.create_novel(title='Novel', public=True)
        chapter = self.john.create_chapter(
            novel.id, title='Chapter', public=True)
        self.ismael.add_to_library(novel.id)
        self.john.unpublish_novel(novel.id)
        self.assertTrue(Notification.objects.filter(recipient=self.ismael,
                                                    verb=f"L'auteur {self.john.username} a rendu non-public son livre {novel.title}").exists())

    def test_user_is_notified_when_library_novel_chapter_is_updated(self):
        novel = self.john.create_novel(title='Novel', public=True)
        chapter = self.john.create_chapter(
            novel.id, title='Chapter', public=True)
        self.ismael.add_to_library(novel.id)
        chapter = self.john.edit_chapter(chapter.id, title='New Title')
        self.assertTrue(Notification.objects.filter(recipient=self.ismael,
                                                    verb=f"L'auteur {self.john.username} a modifie les informations sur le chapitre {chapter.title} de son livre {novel.title}").exists())

    def test_user_is_notified_when_library_novel_chapter_is_deleted(self):
        novel = self.john.create_novel(title='Novel', public=True)
        chapter = self.john.create_chapter(
            novel.id, title='Chapter', public=True)
        self.ismael.add_to_library(novel.id)
        self.john.delete_chapter(chapter.id)
        self.assertTrue(Notification.objects.filter(recipient=self.ismael,
                                                    verb=f"L'auteur {self.john.username} a supprime le chapitre {chapter.title} de son livre {novel.title}").exists())

    def test_user_is_notified_when_library_novel_chapter_is_published(self):
        novel = self.john.create_novel(title='Novel', public=True)
        chapter = self.john.create_chapter(
            novel.id, title='Chapter', public=True)
        chapter2 = self.john.create_chapter(novel.id, title='Chapter2')
        self.ismael.add_to_library(novel.id)
        self.john.publish_chapter(chapter2.id)
        self.assertTrue(Notification.objects.filter(recipient=self.ismael,
                                                    verb=f"L'auteur {self.john.username} a rendu public le chapitre {chapter2.title} de son livre {novel.title}").exists())

    def test_user_is_notified_when_library_novel_chapter_is_unpublished(self):
        novel = self.john.create_novel(title='Novel', public=True)
        chapter = self.john.create_chapter(
            novel.id, title='Chapter', public=True)
        self.ismael.add_to_library(novel.id)
        self.john.unpublish_chapter(chapter.id)
        self.assertTrue(Notification.objects.filter(recipient=self.ismael,
                                                    verb=f"L'auteur {self.john.username} a rendu non-public le chapitre {chapter.title} de son livre {novel.title}").exists())

    def test_user_not_notified_when_unaccessible_novel_is_updated(self):
        novel = self.john.create_novel(title='Novel', public=True)
        chapter = self.john.create_chapter(
            novel.id, title='Chapter', public=True)
        self.ismael.add_to_library(novel.id)
        self.john.unpublish_novel(novel.id)
        novel = self.john.edit_novel(novel.id, title='New Title')
        self.assertFalse(Notification.objects.filter(recipient=self.ismael,
                                                     verb=f"L'auteur {self.john.username} a modifie les informations sur son livre {novel.title}").exists())

    def test_user_not_notified_when_unaccessible_chapter_is_updated(self):
        novel = self.john.create_novel(title='Novel', public=True)
        chapter = self.john.create_chapter(
            novel.id, title='Chapter', public=True)
        chapter2 = self.john.create_chapter(
            novel.id, title='Chapter', public=True)
        self.ismael.add_to_library(novel.id)
        self.john.unpublish_chapter(chapter2.id)
        novel = self.john.edit_chapter(chapter2.id, title='New Title')
        self.assertFalse(Notification.objects.filter(recipient=self.ismael,
                                                     verb=f"L'auteur {self.john.username} a rendu public le chapitre {chapter2.title} de son livre {novel.title}").exists())


class PublishingTestCase(TestCase):
    def setUp(self):
        self.john = User.objects.create(username='john')
        self.ismael = User.objects.create(username='ismael')

    def test_novel_is_published(self):
        novel = self.john.publish_novel(
            self.john.create_novel(title='Johnas').id)
        self.assertTrue(novel.public)

    def test_novel_is_unpublished(self):
        novel = self.john.unpublish_novel(
            self.john.create_novel(title='Johnas', public=True).id)
        self.assertFalse(novel.public)

    def test_chapter_is_published(self):
        novel = self.john.create_novel(title='Title', public=True)
        chapter = self.john.publish_chapter(
            self.john.create_chapter(novel.id, title='Chapter').id)
        self.assertTrue(chapter.public)

    def test_chapter_is_unpublished(self):
        novel = self.john.create_novel(title='Title', public=True)
        chapter = self.john.unpublish_chapter(
            self.john.create_chapter(novel.id, title='Chapter', public=True).id)
        self.assertFalse(chapter.public)

    def test_chapters_of_unpublished_novel_are_not_accessible(self):
        novel = self.john.create_novel(title='Novel', public=True)
        self.john.create_chapter(novel.id, title='Chapter', public=True)
        self.john.create_chapter(novel.id, title='Chapter', public=True)
        self.john.create_chapter(novel.id, title='Chapter', public=True)
        self.john.unpublish_novel(novel.id)
        chapters = Chapter.objects.filter(novel=novel)
        for chapter in chapters:
            self.assertFalse(chapter.is_accessible())

    def test_novel_is_not_accessible_when_all_chapters_are_not_public(self):
        novel = self.john.create_novel(title='Novel', public=True)
        self.john.create_chapter(novel.id, title='Chapter')
        self.john.create_chapter(novel.id, title='Chapter')
        self.john.create_chapter(novel.id, title='Chapter')
        self.assertFalse(novel.is_accessible())

    def test_novel_is_accessible_when_public_and_one_chapter_at_least_public(self):
        novel = self.john.create_novel(title='Novel', public=True)
        self.john.create_chapter(novel.id, title='Chapter')
        self.john.create_chapter(novel.id, title='Chapter')
        self.john.create_chapter(novel.id, title='Chapter', public=True)
        self.assertTrue(novel.is_accessible())

    def test_chapter_is_accessible_when_public_and_novel_public(self):
        novel = self.john.create_novel(title='Novel', public=True)
        self.john.create_chapter(novel.id, title='Chapter')
        self.john.create_chapter(novel.id, title='Chapter')
        self.assertTrue(self.john.create_chapter(
            novel.id, title='Chapter', public=True).is_accessible())

    def test_cannot_publish_or_unpublish_other_people_novel(self):
        johns_novel = self.john.create_novel(title='Johnas')
        with self.assertRaises(NotYourNovelException):
            self.ismael.publish_novel(johns_novel.id)
            self.ismael.unpublish_novel(johns_novel.id)

    def test_cannot_publish_or_unpublish_other_people_chapter(self):
        johns_novel = self.john.create_novel(title='Novel', public=True)
        chapter = self.john.create_chapter(
            johns_novel.id, title='Chapter', public=True)
        with self.assertRaises(NotYourNovelException):
            self.ismael.publish_chapter(chapter.id)
            self.ismael.unpublish_chapter(chapter.id)


class ChapterTestCase(TestCase):
    def setUp(self):
        john = User.objects.create(username='john')
        ismael = User.objects.create(username='ismael')

        john.create_novel(title='Johnas')
        ismael.create_novel(title='Ismaelas')

    def test_chapter_creation_integrity(self):
        john = User.objects.get(username='john')
        johns_novel = Novel.objects.get(title='Johnas')

        # Chapter Data
        title = 'Chapter I: The Omen'
        content = 'Sorry...'
        public = True

        chapter = john.create_chapter(
            johns_novel.id, title=title, content=content, public=public)

        self.assertEqual(title, chapter.title)
        self.assertEqual(content, chapter.content)
        self.assertEqual(public, chapter.public)

    def test_cannot_create_chapter_with_more_or_less_than_zero_reads(self):
        john = User.objects.get(username='john')
        johns_novel = Novel.objects.get(title='Johnas')

        chapter = john.create_chapter(johns_novel.id, reads=20)

        self.assertEqual(0, chapter.reads)

    def test_created_chapter_is_assigned_to_correct_novel(self):
        john = User.objects.get(username='john')
        johns_novel = Novel.objects.get(title='Johnas')
        chapter = john.create_chapter(johns_novel.id)
        novel = Novel.objects.get(pk=johns_novel.id)

        self.assertEqual(novel, chapter.novel)

    def test_cannot_create_chapter_for_other_people_novel(self):
        john = User.objects.get(username='john')
        ismael = User.objects.get(username='ismael')
        johns_novel = Novel.objects.get(title='Johnas')

        with self.assertRaises(NotYourNovelException):
            # Ismael is attempting to create a chapter in John's novel
            ismaels_chapter = ismael.create_chapter(
                johns_novel.id, title='The Chapter of Ismael')

    def test_like_chapter(self):
        john = User.objects.get(username='john')
        ismael = User.objects.get(username='ismael')
        johns_novel = Novel.objects.get(title='Johnas')
        johns_novel = john.publish_novel(johns_novel.id)
        johns_chapter = john.create_chapter(
            johns_novel.id, title='Chapter John', public=True)
        ismael.like_chapter(johns_chapter.id)

        self.assertTrue(Like.objects.filter(
            chapter=johns_chapter, liker=ismael).exists())

    def test_cannot_like_not_public_chapter(self):
        john = User.objects.get(username='john')
        ismael = User.objects.get(username='ismael')
        johns_novel = Novel.objects.get(title='Johnas')
        johns_novel = john.publish_novel(johns_novel.id)
        johns_chapter = john.create_chapter(
            johns_novel.id, title='Chapter John')

        with self.assertRaises(IsNotPublicException):
            ismael.like_chapter(johns_chapter.id)

    def test_cannot_like_chapter_more_than_once(self):
        john = User.objects.get(username='john')
        ismael = User.objects.get(username='ismael')
        johns_novel = Novel.objects.get(title='Johnas')
        johns_novel = john.publish_novel(johns_novel.id)
        johns_chapter = john.create_chapter(
            johns_novel.id, title='Chapter John', public=True)

        with self.assertRaises(AlreadyLikedException):
            ismael.like_chapter(johns_chapter.id)
            ismael.like_chapter(johns_chapter.id)
            ismael.like_chapter(johns_chapter.id)

    def test_cannot_unlike_not_public_chapter(self):
        john = User.objects.get(username='john')
        ismael = User.objects.get(username='ismael')
        johns_novel = Novel.objects.get(title='Johnas')
        johns_novel = john.publish_novel(johns_novel.id)
        johns_chapter = john.create_chapter(
            johns_novel.id, title='Chapter John')

        with self.assertRaises(IsNotPublicException):
            ismael.unlike_chapter(johns_chapter.id)

    def test_cannot_unlike_chapter_that_has_not_been_liked(self):
        john = User.objects.get(username='john')
        ismael = User.objects.get(username='ismael')
        johns_novel = Novel.objects.get(title='Johnas')
        johns_novel = john.publish_novel(johns_novel.id)
        johns_chapter = john.create_chapter(
            johns_novel.id, title='Chapter John', public=True)

        with self.assertRaises(NotLikedYetException):
            ismael.unlike_chapter(johns_chapter.id)

    def test_like_is_removed_when_unliked(self):
        john = User.objects.get(username='john')
        ismael = User.objects.get(username='ismael')
        johns_novel = Novel.objects.get(title='Johnas')
        johns_novel = john.publish_novel(johns_novel.id)
        johns_chapter = john.create_chapter(
            johns_novel.id, title='Chapter John', public=True)

        ismael.like_chapter(johns_chapter.id)
        ismael.unlike_chapter(johns_chapter.id)

        self.assertFalse(Like.objects.filter(
            chapter=johns_chapter, liker=ismael).exists())


class LibraryTestCase(TestCase):
    def setUp(self):
        self.john = User.objects.create(username="john")
        self.ismael = User.objects.create(username="ismael")

    def test_can_add_novel_to_library(self):
        johns_novel = self.john.create_novel(
            title="The Book of John", public=True)
        self.john.create_chapter(johns_novel.id, title='Chapter', public=True)
        self.ismael.add_to_library(johns_novel.id)
        self.assertIn(johns_novel, self.ismael.library.all())

    def test_cannot_add_not_public_novel_to_library(self):
        john = User.objects.get(username="john")
        ismael = User.objects.get(username="ismael")
        johns_novel = john.create_novel(title="The Book of John")
        john.create_chapter(johns_novel.id, title='Chapter', public=True)
        with self.assertRaises(IsNotPublicException):
            ismael.add_to_library(johns_novel.id)

    def test_removed_novel_is_not_in_the_library(self):
        john = User.objects.get(username="john")
        ismael = User.objects.get(username="ismael")
        johns_novel = john.create_novel(title="The Book of John", public=True)
        john.create_chapter(johns_novel.id, title='Chapter', public=True)

        ismael.add_to_library(johns_novel.id)
        ismael.remove_from_library(johns_novel.id)

        self.assertNotIn(johns_novel, ismael.library.all())

    def test_cannot_remove_a_novel_if_not_in_library(self):
        john = User.objects.get(username="john")
        ismael = User.objects.get(username="ismael")
        johns_novel = john.create_novel(title="The Book of John", public=True)

        with self.assertRaises(NotInLibraryException):
            ismael.remove_from_library(johns_novel.id)

    def test_cannot_access_library_novel_that_is_not_in_library(self):
        john = User.objects.get(username="john")
        ismael = User.objects.get(username="ismael")
        johns_novel = john.create_novel(title="The Book of John", public=True)

        # Nobody placed a novel in his library

        self.assertNotIn(johns_novel, ismael.library.all())
        self.assertNotIn(johns_novel, john.library.all())

    def test_cannot_add_novel_more_than_once_in_library(self):
        john = User.objects.get(username="john")
        ismael = User.objects.get(username="ismael")
        johns_novel = john.create_novel(title="The Book of John", public=True)
        john.create_chapter(johns_novel.id, title='Chapter', public=True)

        # Ismael placed it once in his library
        ismael.add_to_library(johns_novel.id)

        # He is now placing it more than once
        with self.assertRaises(AlreadyInLibraryException):
            ismael.add_to_library(johns_novel.id)
            ismael.add_to_library(johns_novel.id)
            ismael.add_to_library(johns_novel.id)


class NovelTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            username="john", email="john@gmail.com", password="l33tPa55word"
        )
        User.objects.create(
            username="ismael", email="ismael@gmail.com", password="l33tPa55word"
        )

    def test_user_created_novel_is_his_own(self):
        user = User.objects.get(username="john")
        novel = user.create_novel()

        self.assertEqual(user, novel.author)

    def test_novel_creation_data_is_same(self):
        user = User.objects.get(username="john")
        title = "The Book of John"
        description = "Do not read it."
        public = True
        mature = True
        genre = "Gore"
        novel = user.create_novel(
            title=title,
            description=description,
            public=public,
            mature=mature,
            genre=genre,
        )

        self.assertEqual(novel.title, title)
        self.assertEqual(novel.description, description)
        self.assertEqual(novel.public, public)
        self.assertEqual(novel.mature, mature)
        self.assertEqual(novel.genre, genre)

    def test_cannot_edit_other_people_novel(self):
        john = User.objects.get(username="john")
        ismael = User.objects.get(username="ismael")

        johns_novel = john.create_novel()

        with self.assertRaises(NotYourNovelException):
            ismael.edit_novel(johns_novel.id)

    def test_cannot_delete_other_people_novel(self):
        john = User.objects.get(username="john")
        ismael = User.objects.get(username="ismael")

        johns_novel = john.create_novel()

        with self.assertRaises(NotYourNovelException):
            ismael.delete_novel(johns_novel.id)

    def test_deleted_novel_does_not_exist_anymore(self):
        user = User.objects.get(username="john")
        novel = user.create_novel()
        user.delete_novel(novel.id)

        with self.assertRaises(Exception):
            novel = Novel.objects.get(pk=novel.id)

    def test_chapters_of_deleted_novels_are_gone(self):
        pass

    def test_novel_edited_data_is_applied(self):
        user = User.objects.get(username="john")
        novel = user.create_novel(
            title="The Book of John",
            description="Never read this Book",
            genre="Erotique",
        )

        # New data
        title = "The New Book of Not John"
        description = "You can read it now"
        genre = "Action"

        # Let's edit the fields
        novel = user.edit_novel(
            novel.id, title=title, description=description, genre=genre
        )
        self.assertEqual(novel.title, title)
        self.assertEqual(novel.description, description)
        self.assertEqual(novel.genre, genre)

    def test_novel_non_edited_data_is_like_before(self):
        user = User.objects.get(username="john")
        novel = user.create_novel(
            title="The Book of John",
            description="Never read this Book",
            genre="Erotique",
        )

        # New data
        title = "The New Book of Not John"

        # Old Data
        description = novel.description
        genre = novel.genre
        publication_date = novel.publication_date
        public = novel.public
        mature = novel.mature

        # Let's edit the fields
        novel = user.edit_novel(novel.id, title=title)
        self.assertEqual(novel.description, description)
        self.assertEqual(novel.publication_date, publication_date)
        self.assertEqual(novel.genre, genre)
        self.assertEqual(novel.public, public)
        self.assertEqual(novel.mature, mature)

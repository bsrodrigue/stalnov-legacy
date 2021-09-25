from apps.novels.models import Novel, Chapter
from apps.novels.exceptions import NotYourNovelException, IsNotPublicException
from notifications.signals import notify

def notify_readers_about_novel(author, novel_id, action_message, edit=False):
    novel = Novel.objects.get(pk=novel_id)
    if edit and not novel.is_accessible():
        return
    notify.send(
        author,
        recipient=novel.get_readers(),
        verb=f"L'auteur {author.username} a {action_message} son livre {novel.title}",
        )

def notify_readers_about_chapter(author, chapter_id, action_message, edit=False):
    chapter = Chapter.objects.get(pk=chapter_id)
    novel = chapter.novel
    if edit and not chapter.is_accessible():
        return
    notify.send(
        author,
        recipient=novel.get_readers(),
        verb=f"L'auteur {author.username} a {action_message} le chapitre {chapter.title} de son livre {novel.title}",
        )

def notify_readers(action):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if action == 'delete_novel':
                notify_readers_about_novel(args[0], args[1], "supprime")
                result = func(*args, **kwargs)
            elif action == 'delete_chapter':
                notify_readers_about_chapter(args[0], args[1], "supprime")
                result = func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
                if action == "publish_novel":
                    notify_readers_about_novel(args[0], args[1], "rendu public")
                elif action == 'unpublish_novel':
                    notify_readers_about_novel(args[0], args[1], "rendu non-public")
                elif action == 'edit_novel':
                    notify_readers_about_novel(args[0], args[1], "modifie les informations sur", edit=True)
                elif action == "publish_chapter":
                    notify_readers_about_chapter(args[0], args[1], "rendu public")
                elif action == 'unpublish_chapter':
                    notify_readers_about_chapter(args[0], args[1], "rendu non-public")
                elif action == 'edit_chapter':
                    notify_readers_about_chapter(args[0], args[1], "modifie les informations sur", edit=True)
            return result
        return wrapper
    return decorator

def notify_author(action):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if action == "like":
                chapter = Chapter.objects.get(pk=args[1])
                notify.send(
                    args[0],
                    recipient=chapter.novel.author,
                    verb=f"{args[0].username} aime votre chapitre {chapter.title}",
                )
            elif action == "unlike":
                chapter = Chapter.objects.get(pk=args[1])
                notify.send(
                    args[0],
                    recipient=chapter.novel.author,
                    verb=f"{args[0].username} n'aime plus votre chapitre {chapter.title}",
                )
            elif action == "comment":
                chapter = Chapter.objects.get(pk=args[1])
                notify.send(
                    args[0],
                    recipient=chapter.novel.author,
                    verb=f"{args[0].username} a commente votre chapitre {chapter.title}",
                )
            return result
        return wrapper
    return decorator


def must_be_the_author(model):
    def decorator(func):
        def wrapper(*args, **kwargs):
            obj = None
            if model.__name__ == "Chapter":
                obj = Chapter.objects.get(pk=args[1])
                if obj.novel.author != args[0]:
                    raise NotYourNovelException
            elif model.__name__ == "Novel":
                obj = Novel.objects.get(pk=args[1])
                if obj.author != args[0]:
                    raise NotYourNovelException
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


def must_be_public(model):
    def decorator(func):
        def wrapper(*args, **kwargs):
            obj = None
            if model.__name__ == "Chapter":
                obj = Chapter.objects.get(pk=args[1])
            elif model.__name__ == "Novel":
                obj = Novel.objects.get(pk=args[1])
            if not obj.is_accessible():
                raise IsNotPublicException
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

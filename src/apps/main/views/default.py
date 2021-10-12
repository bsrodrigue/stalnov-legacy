import readtime
import copy
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.shortcuts import render
from ..models import Novel, Chapter, Comment
from ..forms import StallionUserCreationForm, ChapterForm, CommentForm

class SignUpView(CreateView):
    form_class = StallionUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/forms/auth/register.html"
    context = {"page_title": "Inscription", "page_hero_title": "Inscription",
               "page_hero_description": "Rejoignez la meilleure plateforme de lecture de l'Afrique de l'Ouest"}

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form, **self.context})


def notifications(request):
    user = request.user
    notifications = user.notifications.all()
    notifications = copy.copy(notifications)
    paginator = Paginator(notifications, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user.notifications.mark_all_as_read()
    return render(
        request, "accounts/lists/notifications.html", {"page_title": "notifications",
                                                       "page_hero_title": "Notifications",
                                                       "page_hero_description": "Lisez vos notifications",
                                                       "page_obj": page_obj,
                                                       }
    )


class ProfileView(View):
    template_name = "accounts/pages/profile.html"
    context = {
        "page_title": "Mon profil"
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)


@login_required
def add_to_library(request, novel_id):
    request.user.add_to_library(novel_id)
    return HttpResponseRedirect(reverse_lazy("my_library"))


@login_required
def remove_from_library(request, novel_id):
    request.user.remove_from_library(novel_id)
    return HttpResponseRedirect(reverse_lazy("my_library"))


@login_required
def my_library(request):
    library_novels = request.user.library.all()
    return render(
        request,
        "novels/lists/my_library.html",
        {
            "page_title": f"Ma Bibliothèque",
            "library_novels": library_novels,
            "page_hero_title": f"Ma Bibliothèque",
            "page_hero_description": f"Gérez votre proptre bibliothèque!",
        },
    )


@login_required
def comment_chapter(request, chapter_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        request.user.comment_chapter(chapter_id, form.cleaned_data["content"])
        return HttpResponseRedirect(reverse_lazy("home"))
    else:
        return HttpResponse("Error while commenting")


@login_required
def unlike_chapter(request, chapter_id):
    request.user.unlike_chapter(chapter_id)
    return HttpResponseRedirect(reverse_lazy("home"))


@login_required
def like_chapter(request, chapter_id):
    request.user.like_chapter(chapter_id)
    return HttpResponseRedirect(reverse_lazy("home"))


def search(request):
    search_term = request.GET.get("search")
    search_term = search_term.lower()
    found_novels = [
        novel for novel in Novel.accessible_novels.all() if search_term in novel.title.lower()
    ]
    return render(
        request,
        "novels/lists/search_result.html",
        {
            "page_title": "Recherche",
            "novels": found_novels,
        },
    )


@login_required
def novel_dashboard(request, novel_id):
    novel = Novel.objects.get(pk=novel_id)
    chapters = Chapter.objects.filter(novel=novel_id)

    return render(
        request,
        "novels/pages/novel_dashboard.html",
        {
            "page_title": f"{novel.title}",
            "novel": novel,
            "chapters": chapters,
            "page_hero_title": f"{novel.title}",
            "page_hero_description": f"{novel.description}",
        },
    )


@login_required
def delete_chapter(request, chapter_id):
    request.user.delete_chapter(chapter_id)
    return HttpResponseRedirect(reverse_lazy("my_creations"))


@login_required
def delete_novel(request, novel_id):
    request.user.delete_novel(novel_id)
    return HttpResponseRedirect(reverse_lazy("my_creations"))




@login_required
def my_creations(request):
    novels = Novel.objects.filter(author=request.user.id)
    return render(
        request,
        "novels/lists/my_creations.html",
        {
            "page_title": "Mes Créations",
            "novels": novels,
            "page_hero_title": "Mes créations",
            "page_hero_description": "",
        },
    )

class HomeView(View):
    template_name = "novels/pages/home.jinja"

    def get(self, request, *args, **kwargs):
        novels = Novel.accessible_novels.all()
        extra_context = { 'novels' : novels }
        return render(request, self.template_name, {**extra_context})


def genre(request, genre_name):
    requested_genre_novels = Novel.objects.filter(genre__title=genre_name).order_by(
        "-created_at"
    )
    return render(
        request,
        "novels/lists/genre.html",
        {
            "requested_genre_novels": requested_genre_novels,
        },
    )


def preview_chapter(request, novel_id, chapter_index):
    novel = Novel.objects.get(pk=novel_id)
    chapters = Chapter.objects.filter(novel=novel_id)
    paginator = Paginator(chapters, 1)
    page_number = request.GET.get("page")
    target_page_number = page_number or chapter_index
    page_obj = paginator.get_page(target_page_number)
    current_chapter = page_obj[0]
    reading_time = readtime.of_html(current_chapter.content)

    return render(
        request,
        "novels/pages/chapter.html",
        {
            "page_title": f"{current_chapter.title}",
            "novel": novel,
            "chapters": chapters,
            "page_obj": page_obj,
            "current_chapter": current_chapter,
            "reading_time": reading_time.minutes,
            "page_hero_title": f"{current_chapter.title}",
            "page_hero_description": f"Bonne lecture",
        },
    )


def chapter(request, novel_id, chapter_index):
    novel = Novel.objects.get(pk=novel_id)
    chapters = Chapter.objects.filter(novel=novel_id, public=True)

    paginator = Paginator(chapters, 1)

    page_number = request.GET.get("page")
    target_page_number = page_number or chapter_index

    page_obj = paginator.get_page(target_page_number)
    current_chapter = page_obj[0]
    comments = Comment.objects.filter(chapter=current_chapter.id)
    reading_time = readtime.of_html(current_chapter.content)

    return render(
        request,
        "novels/pages/chapter.html",
        {
            "page_title": f"{current_chapter.title}",
            "novel": novel,
            "chapters": chapters,
            "comments": comments,
            "page_obj": page_obj,
            "current_chapter": current_chapter,
            "reading_time": reading_time.minutes,
            "page_hero_title": f"{current_chapter.title}",
            "page_hero_description": f"Bonne lecture",
        },
    )


def novel(request, novel_id):
    novel = Novel.objects.get(pk=novel_id)
    chapters = Chapter.objects.filter(novel=novel_id, public=True)

    return render(
        request,
        "novels/pages/novel.html",
        {
            "page_title": f"{novel.title}",
            "novel": novel,
            "chapters": chapters,
            "page_hero_title": f"{novel.title}",
            "page_hero_description": f"{novel.description}",
        },
    )

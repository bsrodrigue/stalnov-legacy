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
from .models import Novel, Chapter, Comment
from .forms import *

# TODO: Find a way to make this more scalable
genres_mapping = {
    "Inconnu": "Inconnu",
    "Fantasy": "Fantasy",
    "Aventure": "Aventure",
    "Romance": "Romance",
    "Historique": "Historique",
    "Horreur": "Horreur",
    "Nouvelles": "Nouvelles",
    "Action": "Action",
}

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


def profile(request):
    return render(request, "accounts/profile.html", {"page_title": "profile"})


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
    search_term = request.GET.get("search_term")
    found_novels = [
        novel for novel in Novel.accessible_novels.all() if search_term in novel.title
    ]
    return render(
        request,
        "novels/lists/search_result.html",
        {
            "page_title": "Recherche",
            "found_novels": found_novels,
            "page_hero_title": "Résultats de recherche",
            "page_hero_description": "Lisez, écrivez et partagez des Webnovels Africains",
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


@method_decorator(login_required, name='dispatch')
class ChapterCreationView(View):
    form_class = ChapterForm
    template_name = 'novels/forms/chapter_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        extra_context = {'novel_id': kwargs.get(
            'novel_id'), 'new_chapter': 'new_chapter'}
        return render(request, self.template_name, {'form': form, **extra_context})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        novel_id = kwargs.get('novel_id')
        if form.is_valid():
            chapter = request.user.create_chapter(
                **{x: form.cleaned_data[x] for x in form.cleaned_data if x not in {'public'}})
            if form.cleaned_data['public']:
                request.user.publish_chapter(chapter.id)
                return HttpResponseRedirect(reverse_lazy('novel_dashboard', kwargs={'novel_id': novel_id}))
        extra_context = {'novel_id': novel_id, 'new_chapter': 'new_chapter'}
        return render(request, self.template_name, {'form': form, **extra_context})


@login_required
def edit_chapter(request, chapter_id):
    if request.method == "POST":
        form = ChapterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            chapter = request.user.edit_chapter(
                chapter_id,
                title=data["title"],
                content=data["content"],
                order=data["order"],
            )
            if data["public"]:
                request.user.publish_chapter(chapter_id)
            else:
                request.user.unpublish_chapter(chapter_id)
            return HttpResponseRedirect(
                reverse_lazy("novel_dashboard", kwargs={
                             "novel_id": chapter.novel.id})
            )
        else:
            return HttpResponse("Formulaire invalide")

    chapter_to_be_edited = Chapter.objects.get(pk=chapter_id)
    return render(
        request,
        "novels/forms/chapter_form.html",
        {
            "chapter_id": chapter_id,
            "chapter": chapter_to_be_edited,
            "edit_chapter": "edit_chapter",
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
def edit_novel(request, novel_id):
    if request.method == "POST":
        form = NovelForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            request.user.edit_novel(
                novel_id, title=data["title"], description=data["description"]
            )
            if data["public"]:
                request.user.publish_novel(novel_id)
            else:
                request.user.unpublish_novel(novel_id)
            return HttpResponseRedirect(reverse_lazy("my_creations"))

    novel_to_be_edited = Novel.objects.get(pk=novel_id)
    form = NovelForm(
        initial={
            "genre": novel_to_be_edited.genre,
        }
    )

    return render(
        request,
        "novels/forms/novel_form.html",
        {
            "form": form,
            "edit_novel": "edit_novel",
            "novel": novel_to_be_edited,
        },
    )


@login_required
def new_novel(request):
    if request.method == "POST":
        form = NovelForm(request.POST, request.FILES)
        if form.is_valid():
            cover = f"novel_covers/default/default{form.cleaned_data['default_cover']}.jpg" if form.cleaned_data.get(
                "default_cover", '') else form.cleaned_data.get("cover")
            request.user.create_novel(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                public=form.cleaned_data["public"],
                genre=genres_mapping[form.cleaned_data["genre"]],
                cover=cover,
            )
            return HttpResponseRedirect(reverse_lazy("my_creations"))
        else:
            print(form.errors)
    else:
        form = NovelForm()

    return render(
        request,
        "novels/forms/novel_form.html",
        {
            "page_title": "Nouveau roman",
            "page_hero_title": "Nouveau roman",
            "page_hero_description": "Inspirez des milliers de lecteurs avec une nouvelle histoire!",
            "form": form,
            "new_novel": "new_novel",
        },
    )


@login_required
def my_creations(request):
    my_created_novels = Novel.objects.filter(author=request.user.id)
    return render(
        request,
        "novels/lists/my_creations.html",
        {
            "page_title": "Mes Créations",
            "my_created_novels": my_created_novels,
            "page_hero_title": "Mes créations",
            "page_hero_description": "",
        },
    )


def home(request):
    latest_novels = Novel.accessible_novels.all()
    return render(
        request,
        "novels/pages/home.html",
        {
            "page_title": "Stallion Novels",
            "latest_novels": latest_novels,
            "page_hero_title": "Bienvenue sur Stallion Novels",
            "page_hero_description": "La plateforme africaine #1 d'écriture et de lecture de romans en ligne!",
        },
    )


def genre(request, genre_name):
    genres_mapping = {
        "Inconnu": [
            "Autres",
            "Des histoires probablement trop originales pour etre categorisees.",
        ],
        "Fantasy": [
            "Fantasy",
            "Plongez dans des univers fantastiques où votre imagination est la seule limite.",
        ],
        "Aventure": [
            "Aventure",
            "Échappez à la routine et vivez de grandes aventures.",
        ],
        "Romance": [
            "Romance",
            "Vous croyez en l'amour? Laissez votre coeur s'emballer avec notre collection d'histoires roses.",
        ],
        "Action": ["Action", "Laissez l'Adrenaline prendre le dessus!"],
        "Horreur": ["Horreur", "Des histoires a vous glacer le sang..."],
        "Historique": [
            "Historique",
            "Decouvrez des histoires basees sur des faits reel",
        ],
        "Nouvelles": ["Nouvelles", "Lisez des collections d'histoires courtes."],
    }
    requested_genre = genres_mapping[genre_name]

    requested_genre_novels = Novel.objects.filter(genre=genre_name).order_by(
        "-created_at"
    )
    return render(
        request,
        "novels/lists/genre.html",
        {
            "page_title": f"Genre {requested_genre[0]}",
            "requested_genre_novels": requested_genre_novels,
            "page_hero_title": f"Collection {requested_genre[0]}",
            "page_hero_description": f"{requested_genre[1]}",
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

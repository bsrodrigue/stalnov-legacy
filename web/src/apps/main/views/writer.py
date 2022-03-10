import json
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render
from ..models import Novel, Chapter
from ..forms import NovelForm, ChapterForm

# TODO: Combine pagination with reordering or remove pagination

NOVEL_PAGINATION_SIZE = 10
CHAPTER_PAGINATION_SIZE = 100


@method_decorator(login_required, name="dispatch")
class ChapterReorderView(View):
    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
        if is_ajax:
            data = json.load(request)
            reordering = data.get("payload")
            for new_order, chapter_id in reordering.items():
                request.user.edit_chapter(chapter_id, order=new_order)
            return JsonResponse({"status": "Chapter Reordered successfuly"})
        else:
            return HttpResponseBadRequest("Invalid Request")


def setup_novel_cover(form):
    cover = form.cleaned_data["cover"]
    if cover == "" or form.cleaned_data["default_cover"] != "":
        cover = f"novel_covers/defaults/default{form.cleaned_data['default_cover']}.jpg"
    return cover


def handleAction(action, content_type, request, selected_items):
    if action == "delete":
        if content_type == "novel":
            for item_id in selected_items:
                request.user.delete_novel(item_id)
        elif content_type == "chapter":
            for item_id in selected_items:
                request.user.delete_chapter(item_id)
    elif action == "publish":
        if content_type == "novel":
            for item_id in selected_items:
                request.user.publish_novel(item_id)
        elif content_type == "chapter":
            for item_id in selected_items:
                request.user.publish_chapter(item_id)
    elif action == "unpublish":
        if content_type == "novel":
            for item_id in selected_items:
                request.user.unpublish_novel(item_id)
        elif content_type == "chapter":
            for item_id in selected_items:
                request.user.unpublish_chapter(item_id)


@method_decorator(login_required, name="dispatch")
class BulkActionView(View):
    POSSIBLE_ACTIONS = ("delete", "publish", "unpublish")

    def post(self, request, *args, **kwargs):
        try:
            content_type = request.POST["content_type"]
            action = request.POST["action"]
            selected_items = request.POST.getlist("selected-items")
        except:
            return HttpResponse("Error while processing action and selected novels")
        if action not in self.POSSIBLE_ACTIONS:
            return HttpResponse("Error: cannot perform this kind of action")
        if len(selected_items) == 0:
            return HttpResponse("Error: No novels to act upon")
        handleAction(action, content_type, request, selected_items)
        return HttpResponseRedirect(reverse_lazy("my_creations"))


class NovelDashboard(View):
    template_name = "novels/lists/dashboard.jinja"

    def get(self, request, *args, **kwargs):
        novels = request.user.get_works()
        paginator = Paginator(novels, NOVEL_PAGINATION_SIZE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        extra_context = {"page_obj": page_obj, "dashboard": "novel"}
        return render(request, self.template_name, {**extra_context})


class ChapterDashboard(View):
    template_name = "novels/lists/dashboard.jinja"

    def get(self, request, *args, **kwargs):
        novel_id = kwargs.get("novel_id")
        chapters = Novel.objects.get(pk=novel_id).get_chapters()
        paginator = Paginator(chapters, CHAPTER_PAGINATION_SIZE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        extra_context = {
            "page_obj": page_obj,
            "dashboard": "chapter",
            "novel_id": novel_id,
            "sortable": True,
        }
        return render(request, self.template_name, {**extra_context})


@method_decorator(login_required, name="dispatch")
class NovelCreationView(View):
    form_class = NovelForm
    template_name = "novels/forms/novel_form.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        extra_context = {"new_novel": "new_novel"}
        return render(request, self.template_name, {"form": form, **extra_context})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            novel = request.user.create_novel(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                genre=form.cleaned_data["genre"],
                cover=setup_novel_cover(form),
            )
            if form.cleaned_data["public"]:
                request.user.publish_novel(novel.id)
            return HttpResponseRedirect(reverse_lazy("my_creations"))
        extra_context = {"new_novel": "new_novel"}
        return render(request, self.template_name, {"form": form, **extra_context})


@method_decorator(login_required, name="dispatch")
class NovelEditionView(View):
    form_class = NovelForm
    template_name = "novels/forms/novel_form.html"

    def get(self, request, *args, **kwargs):
        novel_id = kwargs["novel_id"]
        novel = Novel.objects.get(pk=novel_id)
        form = self.form_class(
            initial={
                "genre": novel.genre,
            }
        )
        extra_context = {"edit_novel": "edit_novel", "novel": novel}
        return render(request, self.template_name, {"form": form, **extra_context})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            novel_id = kwargs["novel_id"]
            novel = request.user.edit_novel(
                novel_id,
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                genre=form.cleaned_data["genre"],
                cover=setup_novel_cover(form),
            )
            if form.cleaned_data["public"]:
                request.user.publish_novel(novel_id)
            else:
                request.user.unpublish_novel(novel_id)
            return HttpResponseRedirect(reverse_lazy("my_creations"))
        novel_id = kwargs["novel_id"]
        novel = Novel.objects.get(pk=novel_id)
        extra_context = {"edit_novel": "edit_novel", "novel": novel}
        return render(request, self.template_name, {"form": form, **extra_context})


@method_decorator(login_required, name="dispatch")
class ChapterCreationView(View):
    form_class = ChapterForm
    template_name = "novels/forms/chapter_form.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        extra_context = {
            "novel_id": kwargs.get("novel_id"),
            "new_chapter": "new_chapter",
        }
        return render(request, self.template_name, {"form": form, **extra_context})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        novel_id = kwargs.get("novel_id")
        if form.is_valid():
            chapter = request.user.create_chapter(
                novel_id,
                **{
                    x: form.cleaned_data[x]
                    for x in form.cleaned_data
                    if x not in {"public"}
                },
            )
            if form.cleaned_data["public"]:
                request.user.publish_chapter(chapter.id)
            return HttpResponseRedirect(reverse_lazy("my_creations"))
        extra_context = {"novel_id": novel_id, "new_chapter": "new_chapter"}
        return render(request, self.template_name, {"form": form, **extra_context})


@method_decorator(login_required, name="dispatch")
class ChapterEditionView(View):
    form_class = ChapterForm
    template_name = "novels/forms/chapter_form.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        chapter_id = kwargs.get("chapter_id")
        chapter = Chapter.objects.get(pk=chapter_id)
        extra_context = {
            "chapter_id": chapter_id,
            "edit_chapter": "edit_chapter",
            "chapter": chapter,
        }
        return render(request, self.template_name, {"form": form, **extra_context})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        chapter_id = kwargs.get("chapter_id")
        chapter = Chapter.objects.get(pk=chapter_id)
        if form.is_valid():
            chapter = request.user.edit_chapter(
                chapter_id,
                **{
                    x: form.cleaned_data[x]
                    for x in form.cleaned_data
                    if x not in {"public"}
                },
            )
            if form.cleaned_data["public"]:
                request.user.publish_chapter(chapter.id)
                return HttpResponseRedirect(reverse_lazy("my_creations"))
        extra_context = {
            "edit_chapter": "edit_chapter",
            "chapter_id": chapter_id,
            "chapter": chapter,
        }
        return render(request, self.template_name, {"form": form, **extra_context})


@method_decorator(login_required, name="dispatch")
class ChapterListView(View):
    template_name = "novels/lists/dashboard_chapters.html"

    def get(self, request, *args, **kwargs):
        novel_id = kwargs["novel_id"]
        novel = Novel.objects.get(pk=novel_id)
        chapters = novel.get_chapters()
        extra_context = {"novel": novel, "chapters": chapters}
        return render(request, self.template_name, {**extra_context})

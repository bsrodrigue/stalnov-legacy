from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls.conf import include
from . import views
from .views import default, novel

LOGIN_PAGE_CONTEXT = {
    'page_title': 'Connexion',
    'page_hero_title': 'Connexion',
    'page_hero_description': 'Bon retour parmi nous!',
}

home_urlpatterns = [
    path('', default.home, name='home'),
]

auth_urlpatterns = [
    path("signup/", default.SignUpView.as_view(), name="signup"),
    path("login/", auth_views.LoginView.as_view(extra_context=LOGIN_PAGE_CONTEXT,
                                                template_name='accounts/forms/auth/login.html'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]

account_urlpatterns = [
    path(
        "novel_dashboard/<int:novel_id>",
        default.novel_dashboard,
        name="novel_dashboard",
    ),
    path("notifications", default.notifications, name="notifications"),
    path("my_profile", default.ProfileView.as_view(), name="my_profile"),
]


reader_urlpatterns = [
    path("my_library", default.my_library, name="my_library"),

    path("novel/<int:novel_id>", default.novel, name="novel"),
    path("chapter/<int:novel_id>/<int:chapter_index>",
         default.chapter, name="chapter"),

    path("genre/<str:genre_name>", default.genre, name="genre"),
    path("search", default.search, name="search"),

    path(
        "add_to_library/<int:novel_id>",
        default.add_to_library,
        name="add_to_library",
    ),
    path(
        "remove_from_library/<int:novel_id>",
        default.remove_from_library,
        name="remove_from_library",
    ),

    path("like_chapter/<int:chapter_id>",
         default.like_chapter, name="like_chapter"),
    path(
        "unlike_chapter/<int:chapter_id>", default.unlike_chapter, name="unlike_chapter"
    ),
    path(
        "comment_chapter/<int:chapter_id>",
        default.comment_chapter,
        name="comment_chapter",
    ),
]

writer_urlpatterns = [
    path("my_creations", default.my_creations, name="my_creations"),

    path("new_novel", novel.NovelCreationView.as_view(), name="new_novel"),
    path("edit_novel/<int:novel_id>",
         novel.NovelEditionView.as_view(), name="edit_novel"),
    path(
        "delete_novel/<int:novel_id>", default.delete_novel, name="delete_novel"
    ),

    path("new_chapter/<int:novel_id>",
         default.ChapterCreationView.as_view(), name="new_chapter"),
    path(
        "edit_chapter/<int:chapter_id>", default.edit_chapter, name="edit_chapter"
    ),
    path(
        "delete_chapter/<int:chapter_id>",
        default.delete_chapter,
        name="delete_chapter",
    ),

    path(
        "preview_chapter/<int:novel_id>/<int:chapter_index>",
        default.preview_chapter,
        name="preview_chapter",
    ),
]


urlpatterns = [
    path('', include(home_urlpatterns)),
    path('auth/', include(auth_urlpatterns)),
    path('writer/', include(writer_urlpatterns)),
    path('reader/', include(reader_urlpatterns)),
    path('account/', include(account_urlpatterns)),
]

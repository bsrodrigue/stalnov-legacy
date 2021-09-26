from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import StallionUser, Novel, Chapter, Like, Comment
from .forms import StallionUserCreationForm, StallionUserChangeForm

admin.site.register(Novel)
admin.site.register(Chapter)
admin.site.register(Like)
admin.site.register(Comment)

class StallionUserAdmin(UserAdmin):
    add_form = StallionUserCreationForm
    form = StallionUserChangeForm
    model = StallionUser
    list_display = [
        "email",
        "username",
        "firstname",
        "lastname",
        "bio",
        "gender",
    ]

admin.site.register(StallionUser, StallionUserAdmin)


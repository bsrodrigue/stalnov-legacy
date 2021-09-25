from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import StallionUserCreationForm, StallionUserChangeForm
from .models import StallionUser


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

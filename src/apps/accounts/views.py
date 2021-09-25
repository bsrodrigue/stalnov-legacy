import copy
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render
from .forms import StallionUserCreationForm

class SignUpView(CreateView):
    form_class = StallionUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    context = {"page_title": "Inscription", "page_hero_title": "Inscription", "page_hero_description": "Rejoignez la meilleure plateforme de lecture de l'Afrique de l'Ouest"} 

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
        request, "accounts/notifications.html", {"page_title": "notifications",
                                                 "page_hero_title": "Notifications",
                                                 "page_hero_description": "Lisez vos notifications",
                                                 "page_obj": page_obj,
                                                 }
    )


def profile(request):
    return render(request, "accounts/profile.html", {"page_title": "profile"})

from django.http import HttpResponse
from django.shortcuts import render


def welcome(request):
    return render(
        request,
        "core/pages/welcome.html",
        {
            "page_title": "Bienvenue",
        },
    )

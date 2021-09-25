from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
]
urlpatterns += [
    path("notifications", views.notifications, name="notifications"),
]
urlpatterns += [
    path("profile", views.profile, name="profile"),
]

from django.urls import path

from .views import HomeView, InviteView, Opponent, SelectTrainersView


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("invite/", InviteView.as_view(), name="invite"),
    path("opponent/", Opponent.as_view(), name="opponent"),
    path("trainers", SelectTrainersView.as_view(), name="select_trainers"),
]

from django.urls import path
from . import views as home

app_name = "home_app"
urlpatterns = [
    path("", home.index.as_view(), name="home.index"),
]

from django.urls import path
from . import views as home

app_name = "home"
urlpatterns = [
    path("", home.index.as_view(), name="index"),
]

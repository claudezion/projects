from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("edit", views.edit, name="edit"),
    path("re_new", views.re_new, name="re_new"),
    path("random_page", views.random_page, name="random_page"),
    path("<str:word>", views.title, name="title")
]

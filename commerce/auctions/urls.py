from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("close", views.close, name="close"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("list", views.list, name="list"),
    path("<int:id>", views.listing, name="listing"),
    path("comment", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("category", views.category, name="category")
]

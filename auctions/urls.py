from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("all", views.all, name="all"),
    path("newproduct", views.newproduct, name="newproduct"),
    path("detail/<int:id>", views.detail, name="detail"),
    path("category", views.category, name="category"),
    path("search/<str:name>", views.search, name="search"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("watchlist/<int:pk>", views.watchlist, name="watchlist"),
    path("watch", views.watch, name="watch"),
    path("close/<int:itemId>", views.close, name="close"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
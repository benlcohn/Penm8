from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("uploader/", views.uploader, name="uploader"),
    path("pieces/", views.pieces_index, name="index"),
    path("pieces/<slug:slug>/", views.document_detail, name="document_detail"), 
]
from django.urls import path
from . import views

urlpatterns = [
    path("uploader/", views.uploader, name="uploader"),
    path("pieces/", views.pieces_index, name="pieces_index"),
    path("piece/<slug:slug>/", views.document_detail, name="document_detail"),
]
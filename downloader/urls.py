from django.urls import path
from . import views

app_name="downloader"
urlpatterns=[
path("", views.index, name="index"),
path("download", views.download, name="download"),
path("downloading", views.download3, name="download3"),
path("suggestions", views.suggestions, name="suggestions"),
path("features", views.features, name="features"),
path("downloading_MP3", views.download2, name="download2"),
path("suggestionform", views.suggestionform, name="suggestionform")
]
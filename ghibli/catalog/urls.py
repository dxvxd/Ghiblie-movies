from django.urls import path
from django.views.generic import TemplateView
from .views import FilmListView


urlpatterns = [
    path('movies/', FilmListView.as_view(), name='film-list'),
    path('', TemplateView.as_view(template_name="index.html")),
]

from django.views.generic import ListView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.conf import settings

from .models import Film
from .service import refresh_data


@method_decorator(cache_page(
    60 * settings.CACHE_TIMEOUT_IN_MINUTES
), name='get')
class FilmListView(ListView):
    model = Film

    def get(self, request, *args, **kwargs):
        refresh_data()
        return super().get(request, *args, **kwargs)

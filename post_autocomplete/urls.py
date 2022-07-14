from django.urls import path

from post_autocomplete.views import *

urlpatterns = [
    path('post/search-buildings', SearchBuildingsView.as_view(), name='api-search-buildings'),
]

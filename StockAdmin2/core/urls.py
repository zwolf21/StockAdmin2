from django.urls import path, include

from .views import *

app_name = 'core'
urlpatterns = [
    path('autocomplete/', include('core.autocomplete.urls', 'autocomplete')),
]
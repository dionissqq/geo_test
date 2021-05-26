from django.urls import path
from .views import add_score_change

urlpatterns = [
    path('', add_score_change)
]
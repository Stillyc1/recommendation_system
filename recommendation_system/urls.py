from django.urls import path

from recommendation_system.apps import RecommendationSystemConfig
from recommendation_system.views import FilmRetrieveAPIView

app_name = RecommendationSystemConfig.name

urlpatterns = [
    path('film/<int:pk>/', FilmRetrieveAPIView.as_view(), name='film'),
]

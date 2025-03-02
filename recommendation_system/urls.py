from django.urls import path

from recommendation_system.apps import RecommendationSystemConfig
from recommendation_system.views import FilmRetrieveAPIView, PreferenceCreateAPIView, RecommendationAPIView, \
    RecommendationStatisticsAPIView, HomePageView, FilmDetailView

app_name = RecommendationSystemConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('film_detail/<int:pk>/', FilmDetailView.as_view(), name='film_detail'),

    path('film/<int:pk>/', FilmRetrieveAPIView.as_view(), name='film'),
    path('add_preference/', PreferenceCreateAPIView.as_view(), name='add-preference'),
    path('recommendation/', RecommendationAPIView.as_view(), name='recommendation'),
    path('recommendation/statistics/', RecommendationStatisticsAPIView.as_view(), name='recommendation'),
]

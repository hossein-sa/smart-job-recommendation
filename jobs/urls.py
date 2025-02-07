from django.urls import path
from .views import JobListCreateView, JobDetailView, JobRecommendationView

urlpatterns = [
    path('jobs/', JobListCreateView.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('jobs/recommendations/', JobRecommendationView.as_view(), name='job-recommendations'),
]

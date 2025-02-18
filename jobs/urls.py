from django.urls import path
from .views import JobListCreateView, JobDetailView, JobRecommendationView


"""
    URL patterns for job-related views.

    This URL configuration provides the following routes:
    - 'jobs/': List all jobs and allow recruiters to create new job postings.
    - 'jobs/<int:pk>/': Retrieve, update, or delete a specific job posting identified by its primary key (pk).
    - 'jobs/recommendations/': Retrieve job recommendations for authenticated job seekers based on their profile skills.

    Paths:
        - 'jobs/': Maps to the JobListCreateView, which handles both viewing and creating jobs.
        - 'jobs/<int:pk>/': Maps to the JobDetailView, which allows detailed view and management of a specific job.
        - 'jobs/recommendations/': Maps to the JobRecommendationView, which generates job recommendations for job seekers.

    Names:
        - 'job-list-create': The name for the URL pattern that lists and creates jobs.
        - 'job-detail': The name for the URL pattern to view, update, or delete a job.
        - 'job-recommendations': The name for the URL pattern that provides job recommendations.
    """
urlpatterns = [

    path('jobs/', JobListCreateView.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('jobs/recommendations/', JobRecommendationView.as_view(), name='job-recommendations'),
]

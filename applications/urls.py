from django.urls import path
from .views import ApplyForJobView

urlpatterns = [
    path('jobs/<int:job_id>/apply/', ApplyForJobView.as_view(), name='apply-job'),
]

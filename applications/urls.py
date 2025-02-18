from django.urls import path
from .views import ApplyForJobView
"""
    URL pattern for applying to a job.

    This URL pattern maps the 'apply' action for a specific job identified by its job ID.

    Path:
        - 'jobs/<int:job_id>/apply/': The URL accepts an integer `job_id` as part of the URL to specify which job the user is applying for.

    View:
        - ApplyForJobView: The view that handles the logic for applying to the job.

    Name:
        - 'apply-job': The name for this URL pattern, which can be used for reverse URL resolution.
    """
urlpatterns = [

    path('jobs/<int:job_id>/apply/', ApplyForJobView.as_view(), name='apply-job'),
]

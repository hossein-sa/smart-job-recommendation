from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, JobSeekerProfileUpdateView, RecruiterProfileUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/job-seeker/', JobSeekerProfileUpdateView.as_view(), name='job-seeker-profile'),
    path('profile/recruiter/', RecruiterProfileUpdateView.as_view(), name='recruiter-profile'),
]

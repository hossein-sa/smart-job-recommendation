from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, JobSeekerProfileUpdateView, RecruiterProfileUpdateView


"""
    URL patterns for user-related views in the 'users' app.

    This configuration defines the following routes for user registration, login, and profile management:
    - 'register/': Allows the creation of a new user.
    - 'login/': Allows a user to log in and obtain JWT tokens.
    - 'profile/': Allows authenticated users to retrieve their profile.
    - 'profile/job-seeker/': Allows authenticated job seekers to retrieve and update their job seeker profile.
    - 'profile/recruiter/': Allows authenticated recruiters to retrieve and update their recruiter profile.

    Paths:
        - 'register/': Maps to RegisterView for user registration.
        - 'login/': Maps to LoginView for user login and JWT token generation.
        - 'profile/': Maps to UserProfileView for viewing the current user's profile.
        - 'profile/job-seeker/': Maps to JobSeekerProfileUpdateView for viewing and updating job seeker profile.
        - 'profile/recruiter/': Maps to RecruiterProfileUpdateView for viewing and updating recruiter profile.

    Names:
        - 'register': The name for the URL pattern for user registration.
        - 'login': The name for the URL pattern for user login.
        - 'user-profile': The name for the URL pattern to view the user's profile.
        - 'job-seeker-profile': The name for the URL pattern to manage job seeker profiles.
        - 'recruiter-profile': The name for the URL pattern to manage recruiter profiles.
    """
urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/job-seeker/', JobSeekerProfileUpdateView.as_view(), name='job-seeker-profile'),
    path('profile/recruiter/', RecruiterProfileUpdateView.as_view(), name='recruiter-profile'),
]

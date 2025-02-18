"""
URL configuration for job_recommendation project.

This file maps URL paths to corresponding views in the project. It includes routes for various functionalities such as authentication,
job management, and job applications. The urlpatterns list is configured to handle HTTP requests and direct them to the appropriate views.

For more information on URL routing in Django, see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/

Examples:
    Function views:
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.home, name='home')
    Class-based views:
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    Including another URLconf:
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include


"""
    Main URL patterns for the project.

    This configuration routes incoming requests to the appropriate app's URL patterns, such as authentication, jobs, and applications.

    Paths:
        - 'admin/': The admin panel for managing the project.
        - 'api/auth/': The URL path for handling authentication-related API requests (registration, login, etc.).
        - 'api/': The URL path for job-related API requests (listing, posting jobs).
        - 'api/': The URL path for job application-related API requests (applying for jobs).
    """
urlpatterns = [

    path('admin/', admin.site.urls),  # Admin panel for managing the site
    path('api/auth/', include('users.urls')),  # Authentication APIs (registration, login, etc.)
    path('api/', include('jobs.urls')),  # Job-related APIs (job listing, job posting)
    path('api/', include('applications.urls')),  # Application-related APIs (apply for jobs)
]

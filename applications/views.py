from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import JobApplication
from jobs.models import Job
from .serializers import JobApplicationSerializer


class ApplyForJobView(generics.CreateAPIView):
    """
    View to handle the process of applying for a job.

    This view allows authenticated users to apply for a specific job. It performs the following:
    - Validates that the user is authenticated and has the role of 'job_seeker'.
    - Ensures the job exists.
    - Checks that the user has not already applied for the job.
    - Creates a new job application.
    - Sends an email notification to the recruiter.

    Attributes:
        serializer_class (JobApplicationSerializer): Serializer to validate and represent job application data.
        permission_classes (list): Permission class to ensure only authenticated users can apply.

    Methods:
        create(request, *args, **kwargs): Handles the job application creation, validation, and email notification.
    """

    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Handles the creation of a job application and sends an email notification to the recruiter.

        This method performs the following:
        - Retrieves the job using the job ID provided in the URL.
        - Checks if the user is a job seeker.
        - Verifies that the user has not already applied for the job.
        - Creates a job application and sends a notification email to the recruiter.

        Args:
            request (Request): The incoming HTTP request containing the user's data and job application details.
            *args (tuple): Additional positional arguments.
            **kwargs (dict): Keyword arguments, including the job ID.

        Returns:
            Response: A response containing the job application data and the status code.
        """
        job_id = kwargs.get("job_id")
        job = Job.objects.filter(id=job_id).first()

        if not job:
            return Response({"error": "Job not found"}, status=404)

        if request.user.role != "job_seeker":
            return Response({"error": "Only job seekers can apply"}, status=403)

        existing_application = JobApplication.objects.filter(job_seeker=request.user, job=job).first()
        if existing_application:
            return Response({"error": "You have already applied for this job"}, status=400)

        application = JobApplication.objects.create(job_seeker=request.user, job=job)
        serializer = self.get_serializer(application)

        # Send Email Notification to Recruiter
        subject = f"New Job Application for {job.title}"
        message = f"Hello {job.recruiter.username},\n\n" \
                  f"{request.user.username} has applied for the position: {job.title}.\n" \
                  f"Login to your account to review the application.\n\n" \
                  f"Best Regards,\nSmart Job Recommendation Team"

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [job.recruiter.email],
            fail_silently=False,
        )

        return Response(serializer.data, status=201)

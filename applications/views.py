from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import JobApplication
from jobs.models import Job
from .serializers import JobApplicationSerializer


class ApplyForJobView(generics.CreateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
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

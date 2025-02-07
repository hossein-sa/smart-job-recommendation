from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import JobApplication
from .serializers import JobApplicationSerializer
from jobs.models import Job

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
        return Response(serializer.data, status=201)

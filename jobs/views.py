from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer

class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != "recruiter":
            return Response({"error": "Only recruiters can post jobs"}, status=403)
        serializer.save(recruiter=self.request.user)

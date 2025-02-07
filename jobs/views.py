from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied  # ✅ Fix: Import from exceptions

from .models import Job
from .serializers import JobSerializer


class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != "recruiter":
            raise PermissionDenied("Only recruiters can post jobs.")  # ✅ Now correctly raises PermissionDenied
        serializer.save(recruiter=self.request.user)


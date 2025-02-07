from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response

from .serializers import (
    UserSerializer, LoginSerializer,
    JobSeekerProfileSerializer, RecruiterProfileSerializer
)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class JobSeekerProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.job_seeker_profile

class RecruiterProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = RecruiterProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.recruiter_profile

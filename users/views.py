from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response

from .serializers import (
    UserSerializer, LoginSerializer,
    JobSeekerProfileSerializer, RecruiterProfileSerializer
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    View to register a new user.

    This view handles the creation of a new user based on the data provided in the request. It uses the UserSerializer
    to validate and save the user data.

    Attributes:
        queryset (QuerySet): The queryset to retrieve all users.
        serializer_class (UserSerializer): The serializer used to validate and save user data.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(generics.GenericAPIView):
    """
    View to handle user login and return JWT tokens.

    This view processes user login by validating the provided credentials, then generates and returns JWT tokens (access and refresh).

    Attributes:
        serializer_class (LoginSerializer): The serializer used to validate the user's login credentials.

    Methods:
        post(self, request, *args, **kwargs): Handles the POST request to validate login and return tokens.
    """

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Handles the login process, validating credentials and generating JWT tokens.

        Args:
            request (Request): The incoming HTTP request with the user's login data.

        Returns:
            Response: A response containing the validated JWT tokens for the user.

        Raises:
            ValidationError: If the provided credentials are invalid.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class UserProfileView(generics.RetrieveAPIView):
    """
    View to retrieve the currently authenticated user's profile.

    This view allows the authenticated user to retrieve their own profile information. It uses the UserSerializer
    to serialize the user data.

    Attributes:
        serializer_class (UserSerializer): The serializer used to represent the user's profile data.
        permission_classes (list): The permission class that ensures only authenticated users can access their profile.

    Methods:
        get_object(self): Returns the current authenticated user.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Returns the current authenticated user.

        This method ensures that the profile data returned is that of the currently logged-in user.

        Returns:
            User: The current authenticated user instance.
        """
        return self.request.user


class JobSeekerProfileUpdateView(generics.RetrieveUpdateAPIView):
    """
    View to retrieve and update the job seeker profile of the authenticated user.

    This view allows the authenticated job seeker to update their profile information. It uses the
    JobSeekerProfileSerializer to serialize and validate the profile data.

    Attributes:
        serializer_class (JobSeekerProfileSerializer): The serializer used to represent and validate job seeker profile data.
        permission_classes (list): The permission class that ensures only authenticated users can update their profile.

    Methods:
        get_object(self): Returns the current authenticated user's job seeker profile.
    """

    serializer_class = JobSeekerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Returns the job seeker profile for the authenticated user.

        Returns:
            JobSeekerProfile: The job seeker profile associated with the current authenticated user.
        """
        return self.request.user.job_seeker_profile


class RecruiterProfileUpdateView(generics.RetrieveUpdateAPIView):
    """
    View to retrieve and update the recruiter profile of the authenticated user.

    This view allows the authenticated recruiter to update their profile information. It uses the
    RecruiterProfileSerializer to serialize and validate the profile data.

    Attributes:
        serializer_class (RecruiterProfileSerializer): The serializer used to represent and validate recruiter profile data.
        permission_classes (list): The permission class that ensures only authenticated users can update their profile.

    Methods:
        get_object(self): Returns the current authenticated user's recruiter profile.
    """

    serializer_class = RecruiterProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Returns the recruiter profile for the authenticated user.

        Returns:
            RecruiterProfile: The recruiter profile associated with the current authenticated user.
        """
        return self.request.user.recruiter_profile

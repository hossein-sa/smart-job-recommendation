from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import JobSeekerProfile, RecruiterProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model to handle user creation, login, and profile information.

    This serializer includes user authentication details, profile information for job seekers and recruiters,
    and validation for password during user creation.

    Attributes:
        password (CharField): The password field is write-only to ensure it's not exposed in responses.
        job_seeker_profile (SerializerMethodField): A field to serialize the associated job seeker's profile.
        recruiter_profile (SerializerMethodField): A field to serialize the associated recruiter's profile.

    Methods:
        create(self, validated_data): Handles the creation of a new user, ensuring the password is hashed.
        get_job_seeker_profile(self, obj): Serializes the job seeker profile if available.
        get_recruiter_profile(self, obj): Serializes the recruiter profile if available.
    """

    password = serializers.CharField(write_only=True, required=True)  # Ensure password is included
    job_seeker_profile = serializers.SerializerMethodField()
    recruiter_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'job_seeker_profile', 'recruiter_profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Creates a new user and ensures the password is hashed.

        Args:
            validated_data (dict): The validated data used to create the user.

        Returns:
            user (User): The newly created user instance.
        """
        password = validated_data.pop('password', None)  # Ensure password is removed before passing to create_user
        if not password:
            raise serializers.ValidationError({"password": "This field is required."})

        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=password,
            role=validated_data.get('role', 'job_seeker')
        )
        return user

    def get_job_seeker_profile(self, obj):
        """
        Retrieves and serializes the job seeker profile if available.

        Args:
            obj (User): The user instance whose job seeker profile is being retrieved.

        Returns:
            dict or None: The serialized job seeker profile data or None if not available.
        """
        if hasattr(obj, 'job_seeker_profile'):
            return JobSeekerProfileSerializer(obj.job_seeker_profile).data
        return None

    def get_recruiter_profile(self, obj):
        """
        Retrieves and serializes the recruiter profile if available.

        Args:
            obj (User): The user instance whose recruiter profile is being retrieved.

        Returns:
            dict or None: The serialized recruiter profile data or None if not available.
        """
        if hasattr(obj, 'recruiter_profile'):
            return RecruiterProfileSerializer(obj.recruiter_profile).data
        return None


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login, including username and password validation.

    This serializer is used to authenticate users based on their credentials and generate a JWT token pair.

    Attributes:
        username (CharField): The username of the user attempting to log in.
        password (CharField): The password of the user attempting to log in.

    Methods:
        validate(self, data): Validates the user credentials and returns a JWT token pair if valid.
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validates the user's credentials and generates a JWT token pair.

        Args:
            data (dict): The user credentials (username and password).

        Returns:
            dict: A dictionary containing 'refresh' and 'access' tokens for the user.

        Raises:
            ValidationError: If the credentials are invalid.
        """
        user = User.objects.filter(username=data['username']).first()
        if user and user.check_password(data['password']):
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        raise serializers.ValidationError("Invalid credentials")


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the JobSeekerProfile model to represent the job seeker's additional profile data.

    This serializer allows the serialization of job seeker details, including resume, skills, experience, and preferred location.

    Methods:
        None (standard ModelSerializer behavior)
    """

    class Meta:
        model = JobSeekerProfile
        fields = '__all__'
        read_only_fields = ['user']


class RecruiterProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the RecruiterProfile model to represent the recruiter's additional profile data.

    This serializer allows the serialization of recruiter details, including company name, website, and description.

    Methods:
        None (standard ModelSerializer behavior)
    """

    class Meta:
        model = RecruiterProfile
        fields = '__all__'
        read_only_fields = ['user']

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import JobSeekerProfile, RecruiterProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)  # Ensure password is included
    job_seeker_profile = serializers.SerializerMethodField()
    recruiter_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'job_seeker_profile', 'recruiter_profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
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
        if hasattr(obj, 'job_seeker_profile'):
            return JobSeekerProfileSerializer(obj.job_seeker_profile).data
        return None

    def get_recruiter_profile(self, obj):
        if hasattr(obj, 'recruiter_profile'):
            return RecruiterProfileSerializer(obj.recruiter_profile).data
        return None


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.filter(username=data['username']).first()
        if user and user.check_password(data['password']):
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        raise serializers.ValidationError("Invalid credentials")

class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = '__all__'
        read_only_fields = ['user']

class RecruiterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruiterProfile
        fields = '__all__'
        read_only_fields = ['user']

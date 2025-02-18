from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    """
    Serializer for the Job model to convert job data to and from JSON format.

    This serializer is responsible for serializing the job details, including the recruiter’s username (read-only).
    It ensures that the job data can be easily represented and validated when sending or receiving data via the API.

    Attributes:
        recruiter (ReadOnlyField): The username of the recruiter who posted the job (read-only).

    Meta:
        model (Job): The model that the serializer is based on.
        fields (list): List of fields to include in the serialized output. The value '__all__' indicates all fields from the model are included.
        read_only_fields (list): Specifies the fields that should be read-only (i.e., not editable by the client).

    Methods:
        __str__(self): Provides a string representation of the Job object using its attributes.
    """

    recruiter = serializers.ReadOnlyField(source='recruiter.username')

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['recruiter', 'posted_at']

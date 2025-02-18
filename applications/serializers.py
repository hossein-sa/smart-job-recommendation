from rest_framework import serializers
from .models import JobApplication


class JobApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer for the JobApplication model, providing an easy way to represent and validate job application data.

    Attributes:
        job_seeker (ReadOnlyField): The username of the job seeker who applied for the job.
        job_title (ReadOnlyField): The title of the job for which the application was made.

    Meta:
        model (JobApplication): The model to be serialized.
        fields (list): List of fields to be included in the serialized output. The value '__all__' indicates all fields from the model are included.
        read_only_fields (list): List of fields that should be read-only (i.e., not editable by the client).
    """

    job_seeker = serializers.ReadOnlyField(source='job_seeker.username')
    job_title = serializers.ReadOnlyField(source='job.title')

    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['job_seeker', 'job', 'applied_at', 'status']

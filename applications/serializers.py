from rest_framework import serializers
from .models import JobApplication

class JobApplicationSerializer(serializers.ModelSerializer):
    job_seeker = serializers.ReadOnlyField(source='job_seeker.username')
    job_title = serializers.ReadOnlyField(source='job.title')

    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['job_seeker', 'job', 'applied_at', 'status']

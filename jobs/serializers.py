from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    recruiter = serializers.ReadOnlyField(source='recruiter.username')

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['recruiter', 'posted_at']

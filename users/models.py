from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('job_seeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='job_seeker')

    def __str__(self):
        return self.username

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="job_seeker_profile")
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    skills = models.TextField(blank=True)
    experience = models.IntegerField(default=0)
    preferred_location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username} - Job Seeker"

class RecruiterProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="recruiter_profile")
    company_name = models.CharField(max_length=255, blank=True)
    company_website = models.URLField(blank=True, null=True)
    company_description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - Recruiter"

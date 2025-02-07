from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, JobSeekerProfile, RecruiterProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'job_seeker':
            JobSeekerProfile.objects.create(user=instance)
        elif instance.role == 'recruiter':
            RecruiterProfile.objects.create(user=instance)

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, JobSeekerProfile, RecruiterProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a user profile upon the creation of a CustomUser.

    This function listens for the `post_save` signal from the `CustomUser` model. When a new user is created, it
    automatically creates the appropriate profile (either `JobSeekerProfile` or `RecruiterProfile`) based on the user's role.

    Args:
        sender (Model): The model that sent the signal, which is the `CustomUser` model.
        instance (CustomUser): The instance of the user being saved.
        created (bool): A flag indicating whether the user instance was newly created.
        **kwargs: Additional keyword arguments passed to the receiver function.

    Returns:
        None: This function does not return any value, but creates the appropriate profile.
    """
    if created:
        if instance.role == 'job_seeker':
            JobSeekerProfile.objects.create(user=instance)
        elif instance.role == 'recruiter':
            RecruiterProfile.objects.create(user=instance)

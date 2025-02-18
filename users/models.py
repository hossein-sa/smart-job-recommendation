from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model that extends the default AbstractUser to include a 'role' field.

    The 'role' field distinguishes between 'job_seeker' and 'recruiter' roles, allowing us to handle different
    user types in the system. By default, users are assigned the 'job_seeker' role.

    Attributes:
        ROLE_CHOICES (list): A list of possible roles for the user (job seeker or recruiter).
        role (CharField): The role of the user (job seeker or recruiter).

    Methods:
        __str__(self): Returns the username of the user.
    """

    ROLE_CHOICES = [
        ('job_seeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='job_seeker')

    def __str__(self):
        """
        Returns the username of the user.

        Returns:
            str: The username of the user.
        """
        return self.username


class JobSeekerProfile(models.Model):
    """
    Profile model for job seekers that stores additional details related to job seeker information.

    This model stores a job seeker's resume, skills, experience, and preferred location. It is linked to the
    CustomUser model through a one-to-one relationship.

    Attributes:
        user (OneToOneField): The user associated with this profile (job seeker).
        resume (FileField): A file field for uploading the job seeker's resume.
        skills (TextField): A field to store the job seeker's skills.
        experience (IntegerField): A field to store the job seeker's years of experience.
        preferred_location (CharField): A field for the job seeker's preferred job location.

    Methods:
        __str__(self): Returns a string representation of the job seeker profile, including the username.
    """

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="job_seeker_profile")
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    skills = models.TextField(blank=True)
    experience = models.IntegerField(default=0)
    preferred_location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        """
        Returns a string representation of the job seeker profile.

        Returns:
            str: A string in the format "{user.username} - Job Seeker".
        """
        return f"{self.user.username} - Job Seeker"


class RecruiterProfile(models.Model):
    """
    Profile model for recruiters that stores additional details related to recruiter information.

    This model stores a recruiter's company name, website, and description. It is linked to the CustomUser model
    through a one-to-one relationship.

    Attributes:
        user (OneToOneField): The user associated with this profile (recruiter).
        company_name (CharField): The name of the recruiter's company.
        company_website (URLField): The website URL for the recruiter's company.
        company_description (TextField): A description of the recruiter's company.

    Methods:
        __str__(self): Returns a string representation of the recruiter profile, including the username.
    """

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="recruiter_profile")
    company_name = models.CharField(max_length=255, blank=True)
    company_website = models.URLField(blank=True, null=True)
    company_description = models.TextField(blank=True)

    def __str__(self):
        """
        Returns a string representation of the recruiter profile.

        Returns:
            str: A string in the format "{user.username} - Recruiter".
        """
        return f"{self.user.username} - Recruiter"

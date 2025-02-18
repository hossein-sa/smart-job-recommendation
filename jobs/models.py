from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Job(models.Model):
    """
    Represents a job posting made by a recruiter.

    This model stores details about a job listing, including the recruiter who posted it, job title, company, location,
    salary range, required skills, and the experience required for the position. It also records the date and time the job
    was posted.

    Attributes:
        recruiter (ForeignKey): The user who posted the job (typically a recruiter).
        title (CharField): The title of the job.
        company (CharField): The company offering the job.
        location (CharField): The location of the job.
        salary_range (CharField): The salary range for the job.
        required_skills (TextField): The skills required to perform the job.
        experience_required (IntegerField): The minimum years of experience required for the job.
        posted_at (DateTimeField): The date and time when the job was posted.

    Methods:
        __str__(self): Returns a string representation of the job including the job title and company name.
    """

    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=50)
    required_skills = models.TextField()
    experience_required = models.IntegerField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the job posting.

        The string includes the job title and the company name.

        Returns:
            str: A string in the format "{title} - {company}".
        """
        return f"{self.title} - {self.company}"

from django.db import models
from django.contrib.auth import get_user_model
from jobs.models import Job

User = get_user_model()


class JobApplication(models.Model):
    """
    Represents a job application made by a job seeker for a specific job.

    Attributes:
        job_seeker (ForeignKey): The user applying for the job.
        job (ForeignKey): The job to which the application is made.
        status (CharField): The current status of the job application, which can be 'pending', 'accepted', or 'rejected'.
        applied_at (DateTimeField): The timestamp when the application was created.

    Methods:
        __str__(self): Returns a string representation of the job application showing the job seeker and the job title.
    """

    job_seeker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the job application.

        The string includes the job seeker's username and the job title.

        Returns:
            str: A string of the form "{job_seeker.username} applied for {job.title}".
        """
        return f"{self.job_seeker.username} applied for {self.job.title}"

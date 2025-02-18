from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from users.models import JobSeekerProfile, CustomUser
from jobs.models import Job


class Command(BaseCommand):
    """
    Django management command to send weekly job alerts to job seekers.

    This command retrieves the latest 5 job postings and sends a weekly email to each job seeker with a list of new jobs.
    It is intended to notify job seekers about job opportunities based on the latest posts.

    Attributes:
        help (str): A brief description of the command's purpose.

    Methods:
        handle(*args, **kwargs): Retrieves job seeker profiles and the latest jobs, then sends an email with job alerts.
    """

    help = "Send weekly job alerts to job seekers"

    def handle(self, *args, **kwargs):
        """
        Handles the sending of weekly job alert emails to job seekers.

        The method performs the following steps:
        - Retrieves all job seekers and the latest 5 jobs posted.
        - If no new jobs are available, outputs a warning.
        - For each job seeker with an email, constructs and sends a job alert email containing the latest jobs.

        Args:
            *args (tuple): Additional positional arguments passed to the command.
            **kwargs (dict): Keyword arguments passed to the command.

        Outputs:
            Writes a success or warning message to the console.
        """
        job_seekers = JobSeekerProfile.objects.all()
        new_jobs = Job.objects.order_by('-posted_at')[:5]  # Get last 5 jobs

        if not new_jobs.exists():
            self.stdout.write(self.style.WARNING("No new jobs available."))
            return

        job_list = "\n".join([f"- {job.title} at {job.company} ({job.location})" for job in new_jobs])

        for seeker in job_seekers:
            user = seeker.user
            if not user.email:
                continue  # Skip users without email

            subject = "Weekly Job Alert: New Jobs Available!"
            message = f"Hello {user.username},\n\n" \
                      f"Here are some new job postings that might interest you:\n\n" \
                      f"{job_list}\n\n" \
                      f"Visit our platform to apply now!\n\n" \
                      f"Best Regards,\nSmart Job Recommendation Team"

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

        self.stdout.write(self.style.SUCCESS("Job alerts sent successfully!"))

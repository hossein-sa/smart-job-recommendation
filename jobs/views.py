from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

from .models import Job
from users.models import JobSeekerProfile
from .serializers import JobSerializer

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')


# ✅ Job List & Create View (Only Recruiters Can Create Jobs)
class JobListCreateView(generics.ListCreateAPIView):
    """
    View to list all jobs and create new job postings.

    This view allows authenticated users (with the 'recruiter' role) to create job postings,
    and allows all authenticated users to view the list of jobs.

    Attributes:
        queryset (QuerySet): A queryset to retrieve all job listings, optimized with select_related for the recruiter.
        serializer_class (JobSerializer): Serializer to represent job data in JSON format.
        permission_classes (list): A list of permission classes to control access to the view.

    Methods:
        perform_create(self, serializer): Ensures that only recruiters can post jobs by checking the user's role.
    """

    queryset = Job.objects.select_related("recruiter").all()  # Optimized query
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Handles the creation of a new job posting.

        This method ensures that only users with the 'recruiter' role are allowed to post jobs.

        Args:
            serializer (JobSerializer): The serializer instance to validate and save the job posting.
        """
        if self.request.user.role != "recruiter":
            raise PermissionDenied("Only recruiters can post jobs.")
        serializer.save(recruiter=self.request.user)


# ✅ Job Detail View (View, Update, Delete Job - Only the Recruiter Who Posted It)
class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, and delete a job posting.

    This view allows authenticated users to view a job posting. It ensures that only the recruiter
    who posted the job can update or delete it.

    Attributes:
        queryset (QuerySet): A queryset to retrieve the job and its associated recruiter.
        serializer_class (JobSerializer): Serializer to represent the job data.
        permission_classes (list): A list of permission classes to control access to the view.

    Methods:
        perform_update(self, serializer): Ensures only the recruiter who posted the job can update it.
        perform_destroy(self, instance): Ensures only the recruiter who posted the job can delete it.
    """

    queryset = Job.objects.select_related("recruiter").all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """
        Handles the update of a job posting.

        Ensures that only the recruiter who posted the job can update it.

        Args:
            serializer (JobSerializer): The serializer instance to validate and save the updated job data.
        """
        if self.request.user != serializer.instance.recruiter:
            raise PermissionDenied("Only the recruiter who posted this job can update it.")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Handles the deletion of a job posting.

        Ensures that only the recruiter who posted the job can delete it.

        Args:
            instance (Job): The job instance to be deleted.
        """
        if self.request.user != instance.recruiter:
            raise PermissionDenied("Only the recruiter who posted this job can delete it.")
        instance.delete()


# ✅ Job Recommendation View (For Job Seekers Only)
class JobRecommendationView(APIView):
    """
    View to recommend jobs to job seekers based on their profile skills.

    This view calculates job recommendations for authenticated job seekers based on their
    skills profile, using cosine similarity between the job seeker's skills and job requirements.

    Attributes:
        permission_classes (list): A list of permission classes to ensure only authenticated users can access the recommendations.

    Methods:
        get(self, request): Fetches recommended jobs for the authenticated job seeker.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Handles the retrieval of job recommendations for the authenticated job seeker.

        This method performs the following:
        - Ensures the user has the 'job_seeker' role.
        - Retrieves the job seeker's skills from their profile.
        - Fetches job listings and computes cosine similarity between job seeker's skills and job descriptions.
        - Returns a list of the top 5 recommended jobs.

        Args:
            request (Request): The incoming HTTP request containing the user's details.

        Returns:
            Response: A response containing the list of recommended jobs or an error message.
        """
        user = request.user

        # Ensure only job seekers can get recommendations
        if user.role != "job_seeker":
            return Response({"error": "Only job seekers can receive job recommendations."}, status=403)

        # Get job seeker's profile
        try:
            job_seeker_profile = user.job_seeker_profile
        except JobSeekerProfile.DoesNotExist:
            return Response({"error": "Job seeker profile not found."}, status=404)

        # Extract skills from job seeker profile
        job_seeker_skills = job_seeker_profile.skills.lower()

        # Fetch all job listings
        jobs = Job.objects.all()
        job_data = pd.DataFrame(list(jobs.values("id", "required_skills")))

        if job_data.empty:
            return Response({"message": "No jobs available at the moment."})

        # Preprocess job seeker skills & job descriptions
        stop_words = set(stopwords.words('english'))

        def preprocess(text):
            tokens = word_tokenize(text.lower())
            tokens = [word for word in tokens if word not in stop_words and word not in string.punctuation]
            return " ".join(tokens)

        job_seeker_skills = preprocess(job_seeker_skills)
        job_data["processed_skills"] = job_data["required_skills"].apply(lambda x: preprocess(x.lower()))

        # Convert skills into vectorized format using TF-IDF
        vectorizer = TfidfVectorizer()
        job_vectors = vectorizer.fit_transform(job_data["processed_skills"])
        seeker_vector = vectorizer.transform([job_seeker_skills])

        # Compute cosine similarity between job seeker and job descriptions
        similarity_scores = cosine_similarity(seeker_vector, job_vectors)

        # Rank jobs by similarity
        job_data["similarity"] = similarity_scores[0]
        top_matches = job_data.sort_values(by="similarity", ascending=False).head(5)

        # Get job details for top matches
        recommended_jobs = Job.objects.filter(id__in=top_matches["id"].tolist())
        serializer = JobSerializer(recommended_jobs, many=True)

        return Response(serializer.data)

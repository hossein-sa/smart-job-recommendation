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
    queryset = Job.objects.select_related("recruiter").all()  # Optimized query
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != "recruiter":
            raise PermissionDenied("Only recruiters can post jobs.")
        serializer.save(recruiter=self.request.user)


# ✅ Job Detail View (View, Update, Delete Job - Only the Recruiter Who Posted It)
class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.select_related("recruiter").all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.recruiter:
            raise PermissionDenied("Only the recruiter who posted this job can update it.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.recruiter:
            raise PermissionDenied("Only the recruiter who posted this job can delete it.")
        instance.delete()


# ✅ Job Recommendation View (For Job Seekers Only)
class JobRecommendationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
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

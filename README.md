# Smart Job Recommendation System

A Django & Machine Learning-powered job recommendation system where recruiters can post jobs and job seekers can apply for them. The system provides personalized job recommendations using TF-IDF & Cosine Similarity.

---

## Features
- User Authentication (Register/Login with JWT)
- Job Listings (Recruiters can post, update, delete jobs)
- Job Applications (Job Seekers can apply for jobs)
- Smart Job Recommendations (ML-based matching using TF-IDF & Cosine Similarity)
- Email Notifications (Recruiters get alerts when a job seeker applies)
- REST API with DRF (Test via Postman)
- Secure & Optimized (Rate limiting, pagination, optimized queries)

---

## Technologies Used
- Django, Django REST Framework (DRF)
- PostgreSQL
- Scikit-Learn, NLTK
- JWT Authentication (Simple JWT)
- SMTP Email (Gmail, SendGrid)
- Environment Variables (`python-dotenv`)
- Rate Limiting & Pagination (DRF)

---

## Installation & Setup

### 1. Clone the Repository
```sh
git clone https://github.com/hossein-sa/smart-job-recommendation.git
cd smart-job-recommendation
```

### 2. Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Setup PostgreSQL Database
- Create a database named `job_recommendation`
- Update `.env` file with your database credentials:
```
DB_NAME=job_recommendation
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Apply Migrations
```sh
python manage.py makemigrations users jobs applications
python manage.py migrate
```

### 6. Create a Superuser
```sh
python manage.py createsuperuser
```
Follow the prompts to set up an admin user.

### 7. Run the Development Server
```sh
python manage.py runserver
```
The API is now running at: `http://127.0.0.1:8000/`

---

## API Endpoints

### Authentication
| Method | Endpoint              | Description             |
|--------|-----------------------|-------------------------|
| POST   | `/api/auth/register/` | Register a new user     |
| POST   | `/api/auth/login/`    | Log in and get JWT token |
| GET    | `/api/auth/profile/`  | Get user profile       |

### Job Listings
| Method | Endpoint          | Description                   |
|--------|-------------------|-------------------------------|
| GET    | `/api/jobs/`      | Get all jobs (paginated)      |
| POST   | `/api/jobs/`      | Create a new job (Recruiter)  |
| GET    | `/api/jobs/{id}/` | Get details of a job          |
| PUT    | `/api/jobs/{id}/` | Update a job (Recruiter Only) |
| DELETE | `/api/jobs/{id}/` | Delete a job (Recruiter Only) |

### Job Applications
| Method | Endpoint                  | Description                      |
|--------|---------------------------|----------------------------------|
| POST   | `/api/jobs/{id}/apply/`    | Apply for a job (Job Seeker)     |
| GET    | `/api/jobs/{id}/applications/` | Get all applications (Recruiter Only) |

### Job Recommendations
| Method | Endpoint                     | Description                         |
|--------|------------------------------|-------------------------------------|
| GET    | `/api/jobs/recommendations/` | Get recommended jobs (Job Seeker)  |

Use JWT Token for Authenticated Requests  
Example (Postman):
```sh
Authorization: Bearer your-access-token
```

---

## Email Notifications
- Recruiters receive an email when a job seeker applies.
- Job Seekers receive a weekly job alert with new job postings.

### Manually Send Job Alerts
```sh
python manage.py send_job_alerts
```

---

## Environment Variables
Create a `.env` file in the project root:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DB_NAME=job_recommendation
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=gmail-address
EMAIL_HOST_PASSWORD=your-app-password
```
Make sure to keep `.env` secure and add it to `.gitignore`.

---

## Project Structure
```
job-recommendation-system/
│── users/               # User Authentication & Profiles
│── jobs/                # Job Listings & Recommendations
│── applications/        # Job Applications
│── templates/           # Email Templates (if needed)
│── static/              # Static Files
│── manage.py            # Django CLI
│── requirements.txt     # Dependencies
│── .env                 # Environment Variables (Not Pushed to GitHub)
│── README.md            # Project Documentation
```

---

## Contributing
Contributions are welcome! Follow these steps:  
1. Fork the repository  
2. Create a new branch (`git checkout -b feature-name`)  
3. Commit your changes (`git commit -m "Added new feature"`)  
4. Push to your fork (`git push origin feature-name`)  
5. Submit a Pull Request  

---

## License
This project is licensed under the **MIT License**.

---

## Contact
Email: sadeghi.ho@hotmail.com  
GitHub: [Hossein Sadeghi](https://github.com/hossein-sa)  

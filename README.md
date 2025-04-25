# globant-data-engineering-challenge
Coding challenge for a Data Engineering position at Globant – REST API + SQL analysis.

# Description
This project is a solution to the Globant Data Engineering Challenge. The goal of this application is to create an API for managing employee data, importing CSV files into a database, generating reports based on specific queries, and providing batch insertion functionality for hired employees.
The API is built using FastAPI, and the database is handled with SQLAlchemy. The project also includes Docker containerization and automated testing to ensure the robustness of the application.

# Features
# API Endpoints:
/: A simple endpoint that returns a welcome message.

/upload-csv/: Allows uploading CSV files containing employee, department, or job data.

/report/hires-per-quarter/: Returns a report of hires per department for each quarter in the year 2021.

/report/above-average-hires/: Provides a list of departments that have more hires than the average for the year 2021.

/batch-insert-employees/: Allows batch insertion of employee records (up to 1000 at once).

# Database:
Uses SQLite to store employee, department, and job information.

Supports dynamic CSV imports to populate the relevant tables.

# Prerequisites
Python 3.10 or higher
Docker (optional, but recommended for containerization)
Git (to clone the repository)

# Installation
`git clone https://github.com/your-username/globant-data-engineering-challenge.git`
`cd globant-data-engineering-challenge`
`python -m venv venv`
`venv\Scripts\activate`
`pip install -r requirements.txt`

# Running the Application locally
`uvicorn app.main:app --reload`

# Running Tests
`pytest -v tests/test_main.py`

# Running the Application with Docker
`docker build -t globant-data-engineering-challenge .`
`docker run -d -p 8000:8000 globant-data-engineering-challenge`

# Deployment
The application is deployed on Vercel and can be accessed at the following URL:
https://globant-data-engineering-challenge.vercel.app/

# Conclusion
This project demonstrates the ability to create an API with FastAPI, integrate a database with SQLAlchemy, provide batch processing functionality, and deploy the application both locally and in the cloud (Vercel). Additionally, the application has been containerized with Docker for easy deployment and testing.
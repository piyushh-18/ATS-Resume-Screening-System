# ATS Resume Screening System

This project is a simple Applicant Tracking System built using Flask and MySQL.
The goal is to understand how resumes can be matched with a job description using basic NLP techniques.

I created this project to practice:
- Flask REST APIs
- MySQL integration
- Text similarity using TF-IDF and cosine similarity

## What this project does

- Uploads resumes (text-based)
- Stores resume content in MySQL
- Accepts a job description from HR
- Calculates match percentage between resume and job description
- Ranks multiple resumes based on relevance


## Tech Used

- Python
- Flask
- MySQL
- scikit-learn (TF-IDF, Cosine Similarity)


## How matching works (in simple words)

- Resume text and job description are converted into vectors using TF-IDF
- Cosine similarity is used to measure how similar they are
- Higher similarity means better match



## Project Structure

app.py -> Flask APIs
test_upload.py -> Tests resume upload
test_match.py -> Tests job matching
test_rank.py -> Tests resume ranking
data/ -> Sample resume files


## Resume Format

Currently supports '.txt' resumes for simplicity.
PDF/DOCX parsing can be added later.



## Author

Piyush kumar 
GitHub: https://github.com/piyushh-18
LinkedIn: https://www.linkedin.com/in/piyush-kumar-0533b139b/

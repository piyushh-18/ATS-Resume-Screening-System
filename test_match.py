import requests

url = "http://127.0.0.1:5000/match"

data = {
    "job_description": """
    Looking for a Data Scientist with Python, Machine Learning,
    NLP, SQL, Flask and MySQL experience.
    """
}

response = requests.post(url, json=data)
print(response.json())

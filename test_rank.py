import requests

url = "http://127.0.0.1:5000/rank"

data = {
    "job_description": """
    Looking for a Python developer with ML, NLP,
    Flask, SQL, and data analysis skills.
    """
}

response = requests.post(url, json=data)
print(response.json())

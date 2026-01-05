import requests

url = "http://127.0.0.1:5000/upload"

files = {
    'resume': open('data/sample_resume.txt', 'rb')
}

response = requests.post(url, files=files)

try:
    print(response.json())
except Exception as e:
    print("Response content:", response.text)
    print("Error:", e)


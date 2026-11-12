import requests

api_url = "https://jsonplaceholder.typicode.com/users"

response = requests.get(api_url)

print(response)

print("Status Code : ", response.status_code)
print(response.text)


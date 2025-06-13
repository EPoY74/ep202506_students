import json

import httpx

data = {
    "first_name": "eugenii_1",
    "last_name": "petrov_1",
    "email": "eugenii_2@eugenii.ru",
    "status": "activate",
    }

response = httpx.post("http://0.0.0.0:8000/users/", json=data)
print(response.status_code, response.json())
print(json.dumps(response.json(), indent=4, ensure_ascii=False))

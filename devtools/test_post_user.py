
import json

import httpx

data = {
    "first_name": "eugenii_3",
    "last_name": "petrov_3",
    "email": "eugenii_3@eugenii.ru",
    "date_of_birth": "1980-11-26",
    "status_code": "active",
    }

response = httpx.post("http://0.0.0.0:8000/create_user/", json=data)
print()
print(response.status_code, response.json())
print("-" * 30)
print(json.dumps(response.json(), indent=4, ensure_ascii=False))

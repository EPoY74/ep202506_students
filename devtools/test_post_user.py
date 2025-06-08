import json

import httpx

data = {"name": "eugenii_2", "email": "eugenii_2@eugenii.ru"}

response = httpx.post("http://0.0.0.0:8000/users/", json=data)
print(response.status_code, response.json())
print(json.dumps(response.json(), indent=4, ensure_ascii=False))

import json

import httpx

data = {"name": "eugenii_3", "email": "eugenii_3@eugenii.ru"}

response = httpx.post("http://localhost:8000/users/", json=data)
print(response.status_code, response.json())
print(json.dumps(response.json(), indent=4, ensure_ascii=False))


from datetime import datetime
import json

import httpx

# date_str = "26-11-1980"
# date_obj = datetime.strptime(date_str, "%d-%m-%Y").date()

data = {
    "first_name": "eugenii_2",
    "last_name": "petrov_2",
    "email": "eugenii_2@eugenii.ru",
    "date_of_birth": "1980-11-26",
    "status_code": "active",
    }

response = httpx.post("http://0.0.0.0:8000/create_user/", json=data)
print()
print(response.status_code, response.json())
print("-" * 30)
print(json.dumps(response.json(), indent=4, ensure_ascii=False))

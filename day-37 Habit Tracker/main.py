import requests
from datetime import datetime
import os
import dotenv

dotenv.load_dotenv()

USERNAME ="yaboiamai"
TOKEN = os.environ.get("TOKEN")
GRAPH_ID = "graph1"

pixela_endpoint = "https://pixe.la/v1/users"

user_params =  {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

graph_config = {
    "id": GRAPH_ID,
    "name": "Coding Graph",
    "unit": "Day",
    "type": "int",
    "color": "sora"
}

headers = {
    "X-USER-TOKEN": TOKEN
}

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"
# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)

# graph_config = {
#     "unit": "minutes",
# }
#
# response = requests.put(url=graph_endpoint, json=graph_config, headers=headers)

today = datetime(year=2026, month=7, day=3)
# print(today.strftime("%Y%m%d"))

pixel_params = {
    "date": today.strftime("%Y%m%d"),
    "quantity": "150"
}

# response = requests.post(url=graph_endpoint, json=pixel_params, headers=headers)

previous_date_pixel_endpoint = f"{graph_endpoint}/20260701"

new_pixel_data = {
    "quantity": "180"
}

# response = requests.put(url=previous_date_pixel_endpoint, headers=headers, json=new_pixel_data)

delete_pixel_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime("%Y%m%d")}"

response = requests.delete(url=delete_pixel_endpoint, headers=headers)

print(response.text)

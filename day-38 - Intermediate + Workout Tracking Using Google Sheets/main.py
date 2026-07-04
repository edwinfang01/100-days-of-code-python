import os
import dotenv
import requests
from datetime import datetime
dotenv.load_dotenv()

APP_ID = os.environ.get("APP_ID")
APP_KEY = os.environ.get("APP_KEY")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")


base_url = "https://app.100daysofpython.dev"
exercise_stats_endpoint = f"{base_url}/v1/nutrition/natural/exercise"
sheety_endpoint = "https://api.sheety.co/cddab770c97795aab868c1d1a85414db/workoutTracking/workouts"

exercise_api_headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY
}

input_exercises = input("Tell me which exercise you did: ").split("and")

for exercise in input_exercises:
    body = {
        "query": exercise
    }
    response = requests.post(url=exercise_stats_endpoint, headers=exercise_api_headers, json=body)
    exercise_data = response.json()["exercises"][0]
    now = datetime.now()

    sheety_json = {
        "workout": {
            'date': now.strftime("%d/%m/%Y"),
            'time': now.strftime("%H:%M:%S"),
            'exercise': exercise_data["name"].title(),
            'duration': exercise_data['duration_min'],
            'calories': exercise_data['nf_calories']
        }
    }

    sheety_headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    response = requests.post(url=sheety_endpoint, json=sheety_json, headers=sheety_headers)
    print(response.text)
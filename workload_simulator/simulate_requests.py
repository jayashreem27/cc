import requests
import time
import random

LEVELS = ["INFO", "WARNING", "ERROR"]
API_URL = "http://localhost:8000/log/"

def simulate_requests():
    while True:
        level = random.choice(LEVELS)
        message = f"Log Message - {level}"
        response = requests.post(API_URL, params={"level": level, "message": message})
        print(response.json())
        time.sleep(2)

if __name__ == "__main__":
    simulate_requests()

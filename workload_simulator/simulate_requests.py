# File: /cc/workload_simulator/simulate_requests.py
import requests
import time
import random
import os

LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG", "CRITICAL"]
API_URL = os.getenv("API_URL", "http://api:8000/log/")

def generate_log_message(level: str) -> str:
    messages = {
        "INFO": "System operational",
        "WARNING": "High memory usage detected",
        "ERROR": "Failed to connect to database",
        "DEBUG": "Processing request ID: 12345",
        "CRITICAL": "Server out of memory!"
    }
    return messages.get(level, f"Log event: {level}")

def simulate_requests():
    while True:
        level = random.choice(LEVELS)
        message = generate_log_message(level)
        
        try:
            print(f"Attempting to send to {API_URL}...", flush=True)
            response = requests.post(
                API_URL,
                json={"level": level, "message": message},  # Using json parameter
                timeout=5
            )
            print(f"Sent {level} log: {message}", flush=True)
            print(f"Response: {response.status_code} - {response.text}\n", flush=True)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}", flush=True)
        
        time.sleep(random.uniform(0.5, 2.5))

if __name__ == "__main__":
    simulate_requests()


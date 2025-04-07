import requests
import random
import time

API_URL = "http://localhost:8000"

# Predefined log messages per level
log_data = {
    "info": ["System is up", "User logged in", "Health check passed"],
    "debug": ["Debugging module loaded", "Variable x = 42", "Cache miss"],
    "error": ["Error while connecting to DB", "Null pointer exception", "Disk read failure"],
    "warning": ["Disk usage above 90%", "Memory nearing limit", "High latency detected"],
    "custom": ["This is a custom level log", "Something unusual happened"]
}

def send_log(level, message):
    if level in ["info", "debug", "error", "warning"]:
        url = f"{API_URL}/log/{level}"
        data = {"message": message}
    else:
        url = f"{API_URL}/log/"
        data = {"level": level, "message": message}

    response = requests.post(url, json=data)  # <-- send JSON body
    print(f"Sent {level.upper()} log: {message} | Status Code: {response.status_code}")

def simulate_requests(count=20, delay=1):
    for _ in range(count):
        level = random.choice(list(log_data.keys()))
        message = random.choice(log_data[level])
        send_log(level, message)
        time.sleep(delay)

if __name__ == "__main__":
    simulate_requests()

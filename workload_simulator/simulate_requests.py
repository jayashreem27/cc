# workload_simulator/simulate_requests.py
import requests, time, random

LEVELS = ["info", "warning", "error", "debug", "custom"]
API_URL  = "http://localhost:8000/log"   # no trailing slash

def simulate_requests():
    while True:
        lvl = random.choice(LEVELS)
        msg = f"Auto log → {lvl}"
        if lvl in ["info", "warning", "error", "debug"]:
            url  = f"{API_URL}/{lvl}"
            body = {"message": msg}
        else:
            url  = f"{API_URL}"
            body = {"level": lvl, "message": msg}

        resp = requests.post(url, json=body)
        print(resp.status_code, resp.json())
        time.sleep(2)

if __name__=="__main__":
    simulate_requests()


# File: cc/docker1/api/producer_loop.py
import time
import random
from api.producer import send_log

LEVELS = ["INFO", "WARNING", "ERROR"]

def generate_messages():
    while True:
        level = random.choice(LEVELS)
        message = f"Automatically generated message with level: {level}"
        send_log(level, message)
        time.sleep(2)  # Adjust the delay as needed

if __name__ == "__main__":
    generate_messages()


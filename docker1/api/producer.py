from kafka import KafkaProducer
import json
import time
import os

# Get Kafka server from environment variable (Docker)
KAFKA_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

def get_kafka_producer():
    retries = 10
    while retries > 0:
        try:
            print(f"Connecting to Kafka at {KAFKA_SERVER}...")
            return KafkaProducer(
                bootstrap_servers=KAFKA_SERVER,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
        except Exception as e:
            print(f"Kafka connection failed: {e}. Retrying in 5 seconds... ({retries} retries left)")
            time.sleep(5)
            retries -= 1
    raise Exception("Failed to connect to Kafka after multiple attempts")

producer = get_kafka_producer()

def send_log(level: str, message: str):
    try:
        producer.send("logs", {"level": level, "message": message})
        producer.flush()
        print(f"Log sent: {level} - {message}")
    except Exception as e:
        print(f"Failed to send log: {e}")

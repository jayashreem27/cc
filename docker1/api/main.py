from fastapi import FastAPI
import requests
from kafka import KafkaProducer
import json
import os
import time

app = FastAPI()

# Kafka and Prometheus configuration
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "prometheus_data")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://prometheus:9090")

# Initialize Kafka Producer with retry logic
def get_kafka_producer():
    retries = 10
    while retries > 0:
        try:
            print(f"Trying to connect to Kafka at {KAFKA_BOOTSTRAP_SERVERS}...")
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            print("✅ Kafka Producer connected.")
            return producer
        except Exception as e:
            print(f"❌ Kafka connection failed: {e}. Retrying in 5 seconds... ({retries} retries left)")
            time.sleep(5)
            retries -= 1
    raise Exception("❌ Failed to connect to Kafka after multiple attempts")

producer = get_kafka_producer()

# Function to fetch data from Prometheus
def fetch_prometheus_data():
    query = 'up'  # Modify query if needed
    try:
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={"query": query})
        response.raise_for_status()
        result = response.json()
        metrics = result.get("data", {}).get("result", [])
        print(f"📊 Fetched {len(metrics)} metrics from Prometheus.")
        return metrics
    except Exception as e:
        print(f"❌ Error fetching from Prometheus: {e}")
        return []

# API endpoint to fetch + send to Kafka
@app.get("/fetch_prometheus_data")
async def fetch_and_send():
    metrics = fetch_prometheus_data()
    for metric in metrics:
        try:
            print(f"📤 Sending to Kafka: {metric}")
            producer.send(KAFKA_TOPIC, metric)
        except Exception as e:
            print(f"❌ Error sending metric to Kafka: {e}")
    producer.flush()
    return {"status": "Sent to Kafka", "count": len(metrics)}

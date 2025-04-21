from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import json
import os
import time

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "prometheus_data")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "prometheus-consumer-group")

# Retry logic in case Kafka isn't ready yet
consumer = None
for attempt in range(10):
    try:
        print(f"Attempt {attempt+1}: Connecting to Kafka at {KAFKA_BOOTSTRAP_SERVERS}...")
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=KAFKA_GROUP_ID,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        print("Connected to Kafka successfully!")
        break
    except NoBrokersAvailable:
        print("Kafka broker not available yet. Retrying in 5 seconds...")
        time.sleep(5)

if consumer is None:
    print("Failed to connect to Kafka after multiple attempts. Exiting.")
    exit(1)

print(f"Listening to Kafka topic: {KAFKA_TOPIC}...")

for message in consumer:
    data = message.value
    print(f"Received metric: {data}")

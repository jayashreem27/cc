from kafka import KafkaConsumer
import json
import time
import os

KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "logs")
GROUP_ID = os.getenv("KAFKA_GROUP_ID", "consumer-group")  # 👈 Add this

print(f"🔍 Consumer connecting to Kafka at {KAFKA_BROKER}, Topic: {TOPIC}...")

# Function to wait for Kafka readiness
def wait_for_kafka():
    while True:
        try:
            consumer = KafkaConsumer(
                TOPIC,
                bootstrap_servers=KAFKA_BROKER,
                group_id=GROUP_ID,  # 👈 Required to track offsets
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                value_deserializer=lambda x: json.loads(x.decode("utf-8"))
            )
            print(f"✅ Kafka is available! Consumer connected to topic: {TOPIC}")
            return consumer
        except Exception as e:
            print(f"⏳ Waiting for Kafka... Error: {e}")
            time.sleep(5)

# Initialize Kafka Consumer
consumer = wait_for_kafka()

def consume_logs():
    print(f"📡 Listening for messages on topic '{TOPIC}'...")
    try:
        for message in consumer:
            print(f"📩 Received log: {message.value}")
    except Exception as e:
        print(f"❌ Error in consumer: {e}")

if __name__ == "__main__":
    consume_logs()

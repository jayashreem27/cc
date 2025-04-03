from kafka import KafkaConsumer
import json
import time

KAFKA_BROKER = "kafka:9092"
TOPIC = "logs"

# Function to wait for Kafka to be ready
def wait_for_kafka():
    while True:
        try:
            consumer = KafkaConsumer(
                TOPIC,
                bootstrap_servers=KAFKA_BROKER,
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                group_id='kafka-consumer-1-group',
                value_deserializer=lambda x: json.loads(x.decode("utf-8"))
            )
            print("✅ Kafka is available! Starting Consumer...")
            return consumer
        except Exception as e:
            print(f"⏳ Waiting for Kafka... Error: {e}")
            time.sleep(5)  # Retry after 5 seconds

# Initialize Kafka Consumer when Kafka is ready
consumer = wait_for_kafka()

def consume_logs():
    print("Listening for messages...")
    for message in consumer:
        print(f"Received log: {message.value}")

if __name__ == "__main__":
    consume_logs()

from kafka import KafkaConsumer
import json
import time

KAFKA_BROKER = "kafka:9092"
TOPIC = "logs"

def wait_for_kafka():
    while True:
        print("Waiting for kafka", flush=True)
        try:
            consumer = KafkaConsumer(
                TOPIC,
                bootstrap_servers=KAFKA_BROKER,
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                group_id='kafka-consumer-1-group',
                value_deserializer=lambda x: json.loads(x.decode("utf-8"))
            )
            print("✅ Kafka is available! Starting Consumer...", flush=True)
            return consumer
        except Exception as e:
            print(f"⏳ Waiting for Kafka... Error: {e}", flush=True)
            time.sleep(5)

consumer = wait_for_kafka()
print("Started Kafka", flush=True)

def consume_logs():
    print("Listening for messages...", flush=True)
    for message in consumer:
        print(f"Received log: {message.value}", flush=True)

if __name__ == "__main__":
    consume_logs()


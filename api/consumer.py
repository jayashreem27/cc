from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "logs",
    bootstrap_servers="kafka:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

def consume_logs():
    for message in consumer:
        print(f"Received log: {message.value}")

if __name__ == "__main__":
    consume_logs()

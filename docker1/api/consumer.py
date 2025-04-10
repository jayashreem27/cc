from kafka import KafkaConsumer
import json
import time
import os
import mysql.connector

KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "logs")
GROUP_ID = os.getenv("KAFKA_GROUP_ID", "log-consumer-group")

MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql-db")
MYSQL_USER = os.getenv("MYSQL_USER", "loguser")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "logpass")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "logsdb")

print(f"🔍 Consumer connecting to Kafka at {KAFKA_BROKER}, Topic: {TOPIC}...")

def wait_for_kafka():
    while True:
        try:
            consumer = KafkaConsumer(
                TOPIC,
                bootstrap_servers=KAFKA_BROKER,
                group_id=GROUP_ID,
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                value_deserializer=lambda x: json.loads(x.decode("utf-8"))
            )
            print(f"✅ Kafka is available! Connected to topic: {TOPIC}")
            return consumer
        except Exception as e:
            print(f"⏳ Waiting for Kafka... Error: {e}")
            time.sleep(5)

def connect_db():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

def insert_log_to_db(log):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "INSERT INTO logs (timestamp, level, message, service) VALUES (%s, %s, %s, %s)"
        values = (
            log.get("timestamp"),
            log.get("level", "INFO"),
            log.get("message"),
            log.get("service", "unknown")
        )
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        print("📝 Log inserted into database.")
    except Exception as e:
        print(f"❌ Failed to insert log into DB: {e}")

def consume_logs():
    print(f"📡 Listening for messages on topic '{TOPIC}'...")
    try:
        for message in consumer:
            log = message.value
            print(f"📩 Received log: {log}")
            insert_log_to_db(log)
    except Exception as e:
        print(f"❌ Error in consumer: {e}")

if __name__ == "__main__":
    consumer = wait_for_kafka()
    consume_logs()

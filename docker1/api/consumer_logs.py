import os, json, time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import mysql.connector
from datetime import datetime

# Kafka config
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "logs")
BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
GROUP_ID = os.getenv("KAFKA_GROUP_ID", "mysql-log-group")

# MySQL config
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql-db")
MYSQL_DB = os.getenv("MYSQL_DB", "logsdb")
MYSQL_USER = os.getenv("MYSQL_USER", "loguser")
MYSQL_PWD  = os.getenv("MYSQL_PASSWORD", "logpass")

def get_mysql_conn(retries=5, delay=5):
    for _ in range(retries):
        try:
            return mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PWD,
                database=MYSQL_DB
            )
        except mysql.connector.Error as e:
            print(f"MySQL connect failed: {e}, retrying in {delay}s…")
            time.sleep(delay)
    raise SystemExit("Could not connect to MySQL")

def get_kafka_consumer(retries=10, delay=5):
    for i in range(retries):
        try:
            return KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=BOOTSTRAP,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id=GROUP_ID,
                value_deserializer=lambda m: json.loads(m.decode())
            )
        except NoBrokersAvailable:
            print("Waiting for Kafka…")
            time.sleep(delay)
    raise SystemExit("Could not connect to Kafka")

def main():
    consumer = get_kafka_consumer()
    conn     = get_mysql_conn()
    cursor   = conn.cursor()
    print(f"⏳ Listening on {KAFKA_TOPIC}…")
    for msg in consumer:
        rec = msg.value
        ts  = datetime.now()
        lvl = rec.get("level")
        msg_txt = rec.get("message")
        svc = rec.get("service")
        sql = ("INSERT INTO logs (timestamp, level, message, service) "
               "VALUES (%s,%s,%s,%s)")
        cursor.execute(sql, (ts, lvl, msg_txt, svc))
        conn.commit()
        print(f"✔️  Stored {lvl}@{ts}: {msg_txt}")

if __name__ == "__main__":
    main()


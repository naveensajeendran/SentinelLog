import json
import time
from kafka import KafkaConsumer, KafkaProducer
import redis
import psycopg2
from datetime import datetime


consumer = KafkaConsumer(
    "sentinel.events.detected",
    bootstrap_servers="kafka:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
)

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

redis_client = redis.Redis(host="redis", port=6379, db=0)

conn = psycopg2.connect(
    dbname="sentinel", user="sentinel", password="password", host="db"
)
cursor = conn.cursor()


def store_detection(event):
    cursor.execute(
        """
        INSERT INTO detections (timestamp, threat, source, line)
        VALUES (%s, %s, %s, %s)
        """,
        (
            datetime.utcnow(),
            event["threat"],
            event["source"],
            event["line"],
        ),
    )
    conn.commit()


def update_realtime_metrics(event):
    threat = event["threat"]
    redis_client.hincrby("threat_counts", threat, 1)


def detect_spike(event):
    threat = event["threat"]
    count = redis_client.hget("threat_counts", threat)
    if count and int(count) > 50:
        spike_alert = {
            "alert": "SpikeDetected",
            "threat": threat,
            "count": int(count),
            "time": str(datetime.utcnow())
        }
        producer.send("sentinel.analytics", spike_alert)


def main():
    print("Analytics engine running...")

    for message in consumer:
        event = message.value

        store_detection(event)
        update_realtime_metrics(event)
        detect_spike(event)

        print(f"[Analytics] Processed event: {event}")


if __name__ == "__main__":
    main()
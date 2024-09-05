# shared/kafka_utils.py

from kafka import KafkaProducer, KafkaConsumer
import json

KAFKA_BROKER_URL = "localhost:9092"
TOPIC = "notifications"

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER_URL],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[KAFKA_BROKER_URL],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='notification-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)


def publish_to_kafka(topic, message):
    producer.send(topic, message)
    producer.flush()


def consume_from_kafka():
    for message in consumer:
        yield message.value

from kafka import KafkaProducer
import json
from data import get_registered_user
import time

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=json_serializer)

if __name__ == "__main__":
    for i in range(10):
        registered_user = get_registered_user()
        print(registered_user)
        producer.send("registered_user", value=registered_user)
        time.sleep(5)
        
    producer.close()
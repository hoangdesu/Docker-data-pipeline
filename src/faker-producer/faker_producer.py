"""Produce fake content to 'faker' kafka topic."""
import asyncio
import configparser
import os
import time
from collections import namedtuple
from kafka import KafkaProducer
from faker import Faker
import json
import random

fake = Faker()

# Tutorial
# def get_registered_user():
#     return {
#         "name": fake.name(),
#         "address": fake.address(),
#         "year": fake.year()
#     }

# Assignment 1
def get_registered_user():
    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "age": random.randint(21, 50),
        "ssn": fake.ssn(),
        "email": fake.email(),
        "phonenumber": fake.phone_number(),
        "address": fake.address(),
        "job": fake.job(),
        "company": fake.company(),
        "year": int(fake.year())
    }



KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 5))

def run():
    iterator = 0
    print("Setting up Faker producer at {}".format(KAFKA_BROKER_URL))
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        # Encode all values as JSON
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    )

    while True: 
        # adding prints for debugging in logs
        print("Sending new faker data iteration - {}".format(iterator))
        registered_user = get_registered_user()
        print(registered_user)
        producer.send(TOPIC_NAME, value=registered_user)
        print("New Faker data sent")
        time.sleep(SLEEP_TIME)
        print("Waking up!")
        iterator += 1


if __name__ == "__main__":
    run()

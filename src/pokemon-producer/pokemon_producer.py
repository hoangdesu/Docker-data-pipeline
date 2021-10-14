"""Produce pokemon content to 'pokemon' kafka topic."""
import asyncio
import configparser
import os
import time
from collections import namedtuple
from kafka import KafkaProducer
import json
import random
import requests

url = 'https://pokeapi.co/api/v2/pokemon/'

# Assignment 1
def get_new_pokemon():
    randomID = str(random.randint(1, 200))
    content = requests.get(url + randomID)
    data = content.json()
    return {
        "id": data["id"],
        "name": data["name"],
        "type": data["types"][0]["type"]["name"],
        "weight": data["weight"],
        "height": data["height"]
    }



KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 5))

def run():
    iterator = 0
    print("Setting up Pokemon producer at {}".format(KAFKA_BROKER_URL))
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        # Encode all values as JSON
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    )

    while True: 
        # adding prints for debugging in logs
        print("Sending new pokemon data iteration - {}".format(iterator))
        pokemon = get_new_pokemon()
        print(pokemon)
        producer.send(TOPIC_NAME, value=pokemon)
        print("New Pokemon sent!")
        time.sleep(SLEEP_TIME)
        iterator += 1


if __name__ == "__main__":
    run()

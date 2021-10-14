This is a step by step guide to include Faker API into the built data pipeline from previous tutorial here: https://github.com/vnyennhi/docker-kafka-cassandra

The full solution is here

https://github.com/vnyennhi/docker-kafka-cassandra-faker-api

Note: if the tag "--build" not helping, add another tag "--force-recreate"

1.  Setting up Cassandra

Look at "faker-api/data.py", we can see the script to generate the fake data. We will worry about how to correctly set up the producer correctly later. There are 3 fields: name, address and year. We will set up Cassandra folder with this info.

Add these to a new schema file "cassandra/schema-faker.cql"

```
USE kafkapipeline;
CREATE TABLE IF NOT EXISTS fakerdata (
  name TEXT,
  address TEXT,
  year INT,
  PRIMARY KEY (name, address)
);
```


Now, add that file to the Dockerfile COPY line accordingly and rebuild the docker container Cassandra with the tag --build

```
docker-compose -f cassandra/docker-compose.yml up -d --build
```

Then go inside the Cassandra container and run 

```
cqlsh -f schema-faker.cql
```

To check the current database

```bash
$ cqlsh --cqlversion=3.4.4 127.0.0.1 #make sure you use the correct cqlversion

cqlsh> use kafkapipeline; #keyspace name

cqlsh:kafkapipeline> select * from twitterdata;

cqlsh:kafkapipeline> select * from weatherreport;

cqlsh:kafkapipeline> select * from fakerdata;

```

2. Setting up Kafka Connect

In the folder "kafka", add this to the "connect/create-cassandra-sink.sh"

```

echo "Starting Faker Sink"
curl -s \
     -X POST http://localhost:8083/connectors \
     -H "Content-Type: application/json" \
     -d '{
  "name": "fakersink",
  "config": {
    "connector.class": "com.datastax.oss.kafka.sink.CassandraSinkConnector",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",  
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable":"false",
    "tasks.max": "10",
    "topics": "faker",
    "contactPoints": "cassandradb",
    "loadBalancing.localDc": "datacenter1",
    "topic.faker.kafkapipeline.fakerdata.mapping": "name=value.name, address=value.address, year=value.year",
    "topic.faker.kafkapipeline.fakerdata.consistencyLevel": "LOCAL_QUORUM"
  }
}'
echo "Done."
```

Now, rebuild the docker container kafka with the tag --build

```
docker-compose -f kafka/docker-compose.yml up -d --build
```

Repeat the same steps in previous tutorial to run the script inside "kafka-connect" container and create cluster on the UI.

3. Setting up faker-producer

Duplicate the "own-producer" folder to get us some guiding code, rename it to "faker-producer". Inside that folder, delete the "openweathermap_service.cfg" since we don't need it anymore, rename the python file to "faker_producer.py". Now let's update each file one by one.

3.1. "faker-producer.py": 
- delete line 14-30 and 45-52
- add all from "faker-api/data.py" in
- update the file to make the program run correctly
- remove dataprep package
- here is the complete code for you reference:

```
"""Produce openweathermap content to 'faker' kafka topic."""
import asyncio
import configparser
import os
import time
from collections import namedtuple
from kafka import KafkaProducer
from faker import Faker
import json

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 5))

fake = Faker()

def get_registered_user():
    return {
        "name": fake.name(),
        "address": fake.address(),
        "year": fake.year()
    }

def run():
    iterator = 0
    print("Setting up Faker producer at {}".format(KAFKA_BROKER_URL))
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        # Encode all values as JSON
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    )

    while True:
        sendit = get_registered_user()
        # adding prints for debugging in logs
        print("Sending new faker data iteration - {}".format(iterator))
        producer.send(TOPIC_NAME, value=sendit)
        print("New faker data sent")
        time.sleep(SLEEP_TIME)
        print("Waking up!")
        iterator += 1


if __name__ == "__main__":
    run()

```

3.2. "requirements.txt": 
Replace dataprep with faker since we need the faker Python package

3.3. "Dockerfile": 
Rename python file to "faker_producer.py"

3.4. "docker-compose.yml":
- update line 4,5, and 9 to faker
- update SLEEP_TIME to 5

Now, build the new faker producer

```
docker-compose -f faker-producer/docker-compose.yml up -d
```

4. Setting up consumers

4.1. "faker_consumer.py": 

Duplicate the file "consumers/python/weather_consumer.py", rename it to "faker_consumer.py"

- Update multiple lines in there to clean up old "weather" code
- The two most important one is changing TOPIC_NAME = os.environ.get("FAKER_TOPIC_NAME", "faker") and encode('utf-8). Full code below

```
from kafka import KafkaConsumer
import os, json


if __name__ == "__main__":
    print("Starting Faker Consumer")
    TOPIC_NAME = os.environ.get("FAKER_TOPIC_NAME", "faker")
    KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL", "localhost:9092")
    CASSANDRA_HOST = os.environ.get("CASSANDRA_HOST", "localhost")
    CASSANDRA_KEYSPACE = os.environ.get("CASSANDRA_KEYSPACE", "kafkapipeline")

    print("Setting up Kafka consumer at {}".format(KAFKA_BROKER_URL))
    consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_BROKER_URL])
    
    print('Waiting for msg...')
    for msg in consumer:
        msg = msg.value.decode('utf-8')
        jsonData=json.loads(msg)
        # add print for checking
        print(jsonData)
  
  
```

4.2. "consumers/docker-compose.yml"

Add these in

```
  fakerconsumer:
    container_name: fakerconsumer
    image: twitterconsumer
    environment:
      KAFKA_BROKER_URL: broker:9092
      TOPIC_NAME: faker
      CASSANDRA_HOST: cassandradb
      CASSANDRA_KEYSPACE: kafkapipeline
    command: ["python", "-u","python/faker_consumer.py"]
```

Now, rebuild the consumers with tag --build

```
docker-compose -f consumers/docker-compose.yml up --build
```

5. Repeat the steps to check data in Cassandra

6. Setting up data-vis:

- Add this to "data-vis/docker-compose.yml"

```
FAKER_TABLE: fakerdata
```

- Copy the new "data-vis/python/cassandrautils.py" from the solution GitHub repo (I updated too many things to remember. Plus this is in Python now, you should be able to debug them YOURSELF on Jupyter Lab later)

https://github.com/vnyennhi/docker-kafka-cassandra-faker-api

To put up the data-vis container

```
docker-compose -f data-vis/docker-compose.yml up -d
```


7. Follow the solution GitHub repo instruction for tear down.
# Data Pipeline with Docker

#### Table of Contents
* [About](#about)
* [Data pipeline](#pipeline)
* [How to replicate the project](#run)
* [Demo video](#video)
* [Acknowledgement](#acknowledgement)
* [Connect](#connect)


<a name="about"></a>
# About
This project is the first assignment from Big Data for Engineering class. It utilizes Docker to deploy an end-to-end data pipeline on your local computer using containerized Kafka for data streaming, Cassandra for NoSQL database with Jupyter Lab and Dash framework for data analysis Visualization. There are 3 pipelines using data from Twitter and OpenWeatherMap APIs, Faker API and PokeAPI.


<a name="pipeline"></a>
# Data pipeline

<p>Kafka Producers and Consumers help stream data from provided APIs:</p>
<p align="center"><img src="./img/kafka.png" alt="Kafka" width="90%"></p>

<p>Data is then stored in Cassandra Database:</p>
<p align="center"><img src="./img/cassandra.png" alt="Cassandra" width="90%"></p>

<p>Using Jupyter Lab (or Dash) to query database and visualize data:</p>
<p align="center"><img src="./img/jupyter.png" alt="Jupyter" width="90%"></p>

<p>All Docker containers used in the pipeline:</p>
<p align="center"><img src="./img/docker.png" alt="Docker" width="90%"></p>


<a name="run"></a>
# How to replicate the project

Containers for all things mentioned in this project can be found in the `src` folder. All images have been pre-built, however if you want to replicate the pipeline, you can rebuild the images and compose them up again using the following guide:

#### Create docker networks
<code>docker network create kafka-network
docker network create cassandra-network</code>

#### Start up Cassandra
<code>docker-compose -f cassandra/docker-compose.yml up -d --build</code>

#### Start up Kafka
<code>docker-compose -f kafka/docker-compose.yml up -d</code>

#### Start up the producers
- **OpenWeatherMap**: <code>docker-compose -f owm-producer/docker-compose.yml up -d --build</code>
- **Twitter Producer**: <code>docker-compose -f twitter-producer/docker-compose.yml up --build</code>
- **FakerAPI**: <code>docker-compose -f faker-producer/docker-compose.yml up -d --build</code>
- **Pokemon Producer** <code>docker-compose -f pokemon-producer/docker-compose.yml up -d --build</code>

#### Start all 4 consumers
<code>docker-compose -f consumers/docker-compose.yml up --build</code>

#### Check data in Cassandra DB
- Log in to Cassandra CLI: <code>docker exec -it cassandra bash</code>
- Query the data from 4 tables:
<code>$ cqlsh --cqlversion=3.4.4 127.0.0.1 #make sure you use the correct cqlversion
cqlsh> use kafkapipeline; #keyspace name
cqlsh:kafkapipeline> select * from twitterdata;
cqlsh:kafkapipeline> select * from weatherreport;
cqlsh:kafkapipeline> select * from fakerdata;</code>

#### Data visualization
- With Jupyter Notebook: <code>docker-compose -f data-vis/docker-compose.yml up -d --build</code>
- With Dash: <code>docker-compose -f dashboard/docker-compose.yml up -d</code>


<a name="video"></a>
# Demo video
[![Watch on Youtube!](https://img.youtube.com/vi/7Qf5LH3mwek/hqdefault.jpg)](https://youtu.be/7Qf5LH3mwek)


<a name="acknowledgement"></a>
# Acknowledgement
Based on: https://github.com/salcaino/sfucmpt733/tree/main/foobar-kafka and https://github.com/vnyennhi/docker-kafka-cassandra


<a name="connect"></a>
# Connect with me
* My [Website](https://hoangdesu.com/)
* My [LinkedIn](https://www.linkedin.com/in/hoangdesu/)
* My [Facebook](https://www.facebook.com/Hoangdayo/)
* My [Instagram](https://www.instagram.com/hoang.desu/)
* You can shoot me an [email](mailto:hoangdesu@gmail.com) too!

If you find this project useful, you can let me know. I would love to hear about it! 🔥



FROM cassandra:3.11.1

WORKDIR /opt/scripts

# Copy schema files into /opt/scripts
COPY [ "schema.cql", "schema-faker.cql", "faker_populate.cql", "schema-pokemon.cql", "pokemon_populate.cql", "keyspace.cql" , "bootstrap.sh", "wait-for-it.sh" , "./" ]
RUN chmod +x /opt/scripts/*
# Set the entrypoint to the bootstrap script
ENTRYPOINT [ "/opt/scripts/bootstrap.sh" ]

# Run DSE in search mode in the foreground by default
CMD [ "dse", "cassandra", "-s", "-g", "-f" ]

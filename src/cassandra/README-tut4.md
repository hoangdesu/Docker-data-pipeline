## Create a new keyspace

```
CREATE KEYSPACE IF NOT EXISTS cycling 
WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
```

## Use the keyspace
Do this if you want, adding keyspace name to cql queries will work the same way

```
USE cycling;
```

## Dealing with map

Create table
```
CREATE TABLE cycling.cyclist_teams ( id UUID PRIMARY KEY, lastname text, firstname text, teams map<int,text> );
```

Insert sample data
```
INSERT INTO cycling.cyclist_teams (id, lastname, firstname, teams) 
VALUES (
  5b6962dd-3f90-4c93-8f61-eabfa4a803e2,
  'VOS', 
  'Marianne', 
  {2015 : 'Rabobank-Liv Woman Cycling Team', 2014 : 'Rabobank-Liv Woman Cycling Team', 2013 : 'Rabobank-Liv Giant', 
    2012 : 'Rabobank Women Team', 2011 : 'Nederland bloeit' }); 
```

Check the data
```
SELECT * FROM cycling.cyclist_teams;
```

Get the data out as json format
```
SELECT JSON * from cycling.cyclist_teams;
```

Add 1 item to the map (json)
```
UPDATE cycling.cyclist_teams SET teams = teams + {2009 : 'DSB Bank - Nederland bloeit'} WHERE id = 5b6962dd-3f90-4c93-8f61-eabfa4a803e2;
```

Update item by map key
```
UPDATE cycling.cyclist_teams SET teams[2009] = 'Team DSB - Ballast Nedam' WHERE id = 5b6962dd-3f90-4c93-8f61-eabfa4a803e2;
```

Delete 1 item from the map
```
DELETE teams[2009] FROM cycling.cyclist_teams WHERE id=5b6962dd-3f90-4c93-8f61-eabfa4a803e2;
```

Delete multiple items from the map
```
UPDATE cycling.cyclist_teams SET teams = teams - {2013,2014} WHERE id=5b6962dd-3f90-4c93-8f61-eabfa4a803e2;
```

## More on other data types: set, list, tuples or user defined type
https://docs.datastax.com/en/cql-oss/3.3/cql/cql_using/useAdvancedDataTypesTOC.html


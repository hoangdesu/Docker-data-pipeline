USE kafkapipeline;
CREATE TABLE IF NOT EXISTS kafkapipeline.pokedata (
  id INT,
  name TEXT,
  type TEXT,
  weight INT,
  height INT,
  PRIMARY KEY (id)
);

USE kafkapipeline;
CREATE TABLE IF NOT EXISTS kafkapipeline.fakerdata (
  firstname TEXT,
  lastname TEXT,
  age INT,
  ssn TEXT,
  email TEXT,
  phonenumber TEXT,
  address TEXT,
  job TEXT,
  company TEXT,
  year INT,
  PRIMARY KEY (firstname, ssn)
);

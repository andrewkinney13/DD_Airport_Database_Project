-- Create the airport database
DROP DATABASE IF EXISTS airportDB;
CREATE DATABASE airportDB;
USE airportDB; 

-- Create the flight table 
CREATE TABLE IF NOT EXISTS flights_table (
    source VARCHAR(3),
    dest VARCHAR (3), 
    flight_date DATE,
    passengers INT, 
    PRIMARY KEY (source, dest, flight_date)
    );

-- Select everything from the table to make sure we got the data
SELECT * FROM flights_table;

-- A particular flight between two dates
SELECT * FROM flights_table 
WHERE source = "LAX" AND dest = "BOS" 
AND flight_date >= "2100-01-03" 
AND flight_date <= "2100-01-06";

-- Top three source, dest by passenger #
SELECT * FROM flights_table
ORDER BY passengers DESC
LIMIT 3;

-- Find the next available flight between two airports
SELECT * FROM flights_table WHERE
source = "JFK" AND dest = "LAX"
AND passengers < 300 
ORDER BY flight_date
LIMIT 1;

-- Average occupancy for flights between two cities
SELECT AVG(passengers) AS average_occupancy
FROM flights_table 
WHERE source = "PHL" AND dest = "DEN";
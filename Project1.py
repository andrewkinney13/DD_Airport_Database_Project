# Andrew Kinney
# Database Design Project 1
# Airport XML -> SQL Table -> SQL Queries
# 10.16.2023
# Constraints: 
# Check validity: booking time before flight time
# Creating flights: there are less than 300 passengers in a given flight

import mysql.connector
from collections import defaultdict
from lxml import etree

# Function to insert data into tables
def insert_into_table(table_name, columns, data):

    # Create SQL statement
    statement = ""
    statement += "INSERT INTO " + table_name + " ("
    for column in columns:
        statement += column
        if column != columns[-1]:
            statement += ", "
    statement += ") VALUES ("
    for item in data:
        statement += "'" + str(item) + "'"
        if item != data[-1]:
            statement += ", "
    statement += ")"
    
    # Execute it
    cursor.execute(statement)
    db.commit()


# Init variables
root = etree.parse("PNR.xml")

# Connect to SQL server
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "12345",
    database = "airportDB"
)

# Add cursor
cursor = db.cursor()

# flights is a dict of dicts of lists of Flight objects
# flights[airport][bookingTime][Flight object index]
bookings = []

# Obtain the flight data
attribCount = -10 # -10 to skip first row of column names
for flight in root.iter():
     
    # Entering a new booing
    if flight.tag == "{urn:schemas-microsoft-com:office:spreadsheet}Row" and attribCount >= 0:
        # Reset attrib counter
        attribCount = 0

    # We're looking at a given flight's data
    if flight.tag == "{urn:schemas-microsoft-com:office:spreadsheet}Data":
        
        # Create a new flight obj if needed
        if attribCount == 0:
            currentBooking = {}
        
        # Insert data
        if attribCount == 0:
            currentBooking["firstName"]= flight.text
        if attribCount == 1:
            currentBooking['lastName'] = flight.text
        if attribCount == 2:
            currentBooking["address"] = flight.text
        if attribCount == 3:
            currentBooking["age"] = flight.text
        if attribCount == 4:
            currentBooking["source"] = flight.text
        if attribCount == 5:
            currentBooking["dest"] = flight.text
        if attribCount == 6:
            currentBooking["travelDate"] = flight.text
        if attribCount == 7:
            currentBooking["class"] = flight.text
        if attribCount == 8:
            currentBooking["bookingTime"] = flight.text
        if attribCount == 9:
            currentBooking["npass"] = flight.text

        # Increment attrib count
        attribCount += 1

        # Append the current booking (ONLY FULL ONES!)
        if attribCount == 10:
            bookings.append(currentBooking)

# Obtain a list of airports
inputFile = open("iata.txt", "r")
airports = inputFile.read().splitlines()
inputFile.close()

# Create data structure for the flights based on airport and travel date\
# airportFlights = {source airport: flights = {travelDate: bookings[]}}

# Create tuple list of source --> destination airports
flightPaths = []
for sourceAirport in airports:
    for destinationAirport in airports:
        if sourceAirport != destinationAirport:
            flightPaths.append((sourceAirport, destinationAirport))

# Initalize dict to store bookings at (source, destination) key
airportFlights = {}
for path in flightPaths:
    airportFlights[path] = defaultdict(list)

# Insert bookings into the dict
for booking in bookings:
    airportFlights[(booking["source"], booking["dest"])][booking["travelDate"]].append(booking)

# Insert grouped bookings into sql table
for path in airportFlights:
    for travelTime in airportFlights[path]:
        
        # Determine total passengers for a flight
        currentPassengers = 0
        for booking in airportFlights[path][travelTime]:
            currentPassengers += int(booking["npass"])
            #insert_into_table("flights", 
            #("firstname", "lastname", "address", "age", "source", "dest", 
            #"travelDate", "class", "bookingTime", "npass"), 
            #booking)

        # Insert the data
        insert_into_table("flights_table", ("source", "dest", "flight_date", "passengers"), 
                         (path[0], path[1], travelTime, currentPassengers))


cursor.close()

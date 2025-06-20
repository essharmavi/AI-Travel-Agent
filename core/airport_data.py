import airportsdata
import json
airports = airportsdata.load('IATA')
city_to_airport = []
for key, value in airports.items():
    name = key + "(" + value['city'] + ", " + value['country'] + ")"
    city_to_airport.append(name)

city_to_airport = city_to_airport.sort()
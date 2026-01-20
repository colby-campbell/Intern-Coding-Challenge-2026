"""
Colby Campbell
(306) 750-1225
colby.campbell@ucalgary.ca (preferred)

Since this coding challenge is for an internship position, I wanted to explain my
approach to solving the problem before presenting the code itself.

Problem:
    - There are two sensors, both with 100m accuracy
    - We will have to read two different file formats: CSV and JSON
    - Since both sensors have 100m accuracy, if the readings are within 200m of each other,
        we will consider them to be a genuine detection.
    - We need to output the genuine detections.
    
Approach:
    - Read the CSV and JSON files using standard Python libraries, parsing the data into a common format (list of dictionaries)
    - For each reading in the CSV file, compare it to each reading in the JSON file
    - Use the Haversine formula to calculate the distance between the two readings. Since I don't want to use
        external libraries for the ease of the reviewer, I implemented the Haversine formula with Python math functions.
        I am using the formula from https://www.vcalc.com/wiki/vcalc/haversine-distance.
    - If the distance is less than or equal to 200m, consider it a genuine detection and store it
    - Output to a new CSV file and the terminal (the README wasn't clear on the format).
"""

import csv
import json
import math

# Constants
MEAN_EARTH_RADIUS_M = 6371009
SENSOR_FILE_CSV = "SensorData1.csv"
SENSOR_FILE_JSON = "SensorData2.json"


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the Haversine distance between two points"""

    # Convert latitude and longitude from degrees to radians to use in the trigonometric functions
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta1_rad = math.radians(lat2 - lat1) / 2
    delta2_rad = math.radians(lon2 - lon1) / 2

    # Haversine formula
    a = (math.sin(delta1_rad) ** 2 + math.sin(delta2_rad) ** 2 * math.cos(lat1_rad) * math.cos(lat2_rad))
    distance = 2 * math.asin(math.sqrt(a)) * MEAN_EARTH_RADIUS_M
    return distance


def read_csv_sensor_data(file_path):
    """Read sensor data from a CSV file and return as a list of dictionaries"""
    sensor_data = []
    with open(file_path, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            sensor_data.append({
                'id': row['id'],
                'latitude': float(row['latitude']),
                'longitude': float(row['longitude'])
            })
    return sensor_data


def read_json_sensor_data(file_path):
    """Read sensor data from a JSON file and return as a list of dictionaries"""
    with open(file_path, mode='r') as json_file:
        sensor_data = json.load(json_file)
    return sensor_data

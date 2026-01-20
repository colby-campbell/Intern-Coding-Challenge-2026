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
SENSOR_FILE_1 = "SensorData1.csv"
SENSOR_FILE_2 = "SensorData2.json"
OUTPUT_FILE_CSV = "GenuineDetections.csv"
SENSOR_ACCURACY_M = 100


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


def find_genuine_detections(sensor_data_csv, sensor_data_json):
    """Find genuine detections between two sensor datasets, return as a list of dictionaries"""
    genuine_detections = []
    # The distance threshold for genuine detection is twice the sensor accuracy distance
    threshold_distance = SENSOR_ACCURACY_M * 2

    # Compare each reading from CSV with each reading from JSON, calculate the distance, and check if within threshold
    for data_csv in sensor_data_csv:
        for data_json in sensor_data_json:
            distance = haversine_distance(
                data_csv['latitude'], data_csv['longitude'],
                data_json['latitude'], data_json['longitude']
            )
            if distance <= threshold_distance:
                genuine_detections.append({
                    'sensor1_id': data_csv['id'],
                    'sensor2_id': data_json['id']
                })
    return genuine_detections


def write_genuine_detections_to_csv(genuine_detections, output_file):
    """Write the genuine detections to a CSV file"""
    with open(output_file, mode='w', newline='') as csv_file:
        # Define the CSV field names and write the header
        field_names = ['sensor1_id', 'sensor2_id']
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        # Write each genuine detection as a row in the CSV file
        for detection in genuine_detections:
            writer.writerow(detection)


def main():
    # Read sensor data from files
    sensor_data_1 = read_csv_sensor_data(SENSOR_FILE_1)
    sensor_data_2 = read_json_sensor_data(SENSOR_FILE_2)

    # Find genuine detections
    genuine_detections = find_genuine_detections(sensor_data_1, sensor_data_2)

    # Output genuine detections to terminal
    print(f"Found {len(genuine_detections)} genuine detection(s):")
    for detection in genuine_detections:
        print(f"Sensor 1 ID: {detection['sensor1_id']}, Sensor 2 ID: {detection['sensor2_id']}")

    # Write to the output CSV file
    write_genuine_detections_to_csv(genuine_detections, OUTPUT_FILE_CSV)
    print(f"Genuine detections written to {OUTPUT_FILE_CSV}")


if __name__ == "__main__":
    main()

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


# DBScan
Coordinate clustering

1. Introduction
Guidelines
Please complete the assignment inside this notebook. Make sure the code can be executed easily.

Write production-ready code using OOP when relevant.
For question 1, create simple unit tests for your code where applicable.
For question 1, add comments and documentation strings for all methods.
For question 2 and 3, discuss your design choices.
For question 2 and 3, discuss the complexity (Big O notation) of your solutions, both memory wise and performance wise.
For question3, provide map visualization when relevant
Try to stick to the most popular scientific Python libraries.
Input data
You should have received three csv files. Each csv-file represents the locations where a person was stationary for a certain amount of time. The csv-files contain the following fields:

Latitude: The latitude of the detected GPS coordinates Longitude: The longitude of the detected GPS coordinates
Timestamp: The start time of the stationary in the following format:
YYYY = year
MM = month of year
dd = day of month
HH=hourofday
mm = minute of hour
Z = timezone offset
Duration: The length of time the person was stationary (in milliseconds)
All questions in this assignment are related to this data.

In [2]:
# import statements go here.
2. Programming skills
Question 1: Data parsing
Create the code needed to read and parse the data.
Print out some summary statistics of the data
e.g. Average number of places visited per day
e.g. Median distance traveled between two subsequent stationary locations
...
Question 2: Data lookup
Create a method that generates a lookup table allowing us to effiently check whether or not a user has ever visited a location even if the new location is not exactly the same as the visited location (some noise is added to the longitude/latitude pairs).

In [ ]:

Question 3: Home and work detection
The goal of this question, is to design an algorithm that allows us to distinguish the likely home locations of a user from his likely work locations.

Note that a person might have multiple home and work locations, or might not have a work location at all. Also note that the data might be noise, incorrect and/or incomplete.

Discuss your choice of algorithms, rules, methods, distance measures, etc.

In [ ]:

import csv
from pynn import NearestNeighborIndex

"""
Demonstration of usage of the pynn library nearest_neighbor_index in a geospatial defense context.

Script reads data from a csv file (example provided at root/data/base_locations.csv) then builds the k-d tree. This 
would already be in our dataset. It is here for example. Data scientist would receive the shortly mentioned points of 
interest and will be able to query his tree to see if anything else of interest is near it.

User can pass in points of interest (hospitals, civilian locations, etc) to the search and it will return
the closest base (or enemy ground force, SAM sites, any intel) to that. 

input: csv file with x, y points
output: nearest base location (will be one of the bases in the provided csv)
"""

def load_from_csv(csv_path):

    # leveraging csv reader here to easily read a csv file. each row should have two columns: x and y.
    # returns a list of points.
    points = []
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            # map can be used here to easily convert the individual values of the tuple into floats
            # then returns an iterable object which we can use to easily assign our x and y.
            x, y = map(float, row)
            points.append((x, y))
    return points

if __name__ == '__main__':

    # load the known locations of hostile forces
    base_locations_csv = "data/base_locations.csv"
    base_locations = load_from_csv(base_locations_csv)

    # build our k-d tree for quick querying
    built_index = NearestNeighborIndex(base_locations)

    # define some points (these would be troop locations, targets, friendlies, etc..)
    data_scientist_queries = [
        (132.3, -1.8),
        (5, -5),
        (119.31, 55.26),
    ]

    # find and print nearest base to each queried point so user can view them.
    print("Nearest base locations for each query point:")
    for query in data_scientist_queries:
        nearest_base = built_index.find_nearest(query)
        print(f"Data scientist query: {query}'s nearest base is at {nearest_base}")

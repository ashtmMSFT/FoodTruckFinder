from geopy import distance
import logging
import os
import pandas
import requests
import sys

## 'Constants'
FOOD_TRUCK_DATA_CSV = "Mobile_Food_Facility_Permit.csv"
FOOD_TRUCK_DATA_URL = "https://data.sfgov.org/api/views/rqzj-sfat/rows.csv?accessType=DOWNLOAD"

## Function definitions
def parse_user_input():
    """ Parse and validate the script arguments to learn the user's current location. """
    if len(sys.argv) != 3:
        logging.error("Incorrect number of arguments provided")
        display_expected_usage_and_quit()

    try:
        user_lat = float(sys.argv[1])
        user_long = float(sys.argv[2])
    except ValueError:
        logging.error("Incorrect type of arguments provided")
        display_expected_usage_and_quit()

    return (user_lat, user_long)

def display_expected_usage_and_quit():
    """ Print a message displaying the expected script usage, then exit. """
    print("Expected usage: py ftf.py [your_latitude] [your_longitude]")
    print("          e.g., py ftf.py 37.7775 -122.416389")
    raise SystemExit

def download_latest_data():
    """ Download the latest food truck permit dataset from SFGov
        and save it to disk. """
    try:
        response = requests.get(FOOD_TRUCK_DATA_URL)
        response.raise_for_status()

        with open(FOOD_TRUCK_DATA_CSV, 'w') as file:
            file.write(response.text)

    except requests.RequestException:
        logging.error("There was a problem retrieving the most recent food truck data.")
        logging.warning("Falling back to local data (if available).")

def read_local_data():
    """ Read the food truck dataset from disk. """
    try:
        data = pandas.read_csv(FOOD_TRUCK_DATA_CSV)
        return data
    except:
        logging.error("Food truck data file could not be loaded! Cannot proceed -- aborting program")
        raise

def clean_data(data):
    """ Remove data rows (i.e., food trucks) with incomplete location data
        or without an approved permit. """
    # Filter out food trucks missing lat/long data
    trucks_without_lat_long = data[(data["Latitude"] == 0) | (data["Longitude"] == 0)].index
    data.drop(trucks_without_lat_long, inplace = True)

    # Filter out food trucks with pending/expired/suspended permits
    trucks_without_valid_permit = data[data["Status"] != "APPROVED"].index
    data.drop(trucks_without_valid_permit, inplace = True)

def calculate_distances(data, user_location):
    """ Add a column to our dataset indicating how far away the food truck is from the user. """
    data["DistanceFromUser"] = data.apply(calculate_distance_to_truck, axis = 1, user_location = user_location)

def calculate_distance_to_truck(row, user_location):
    """ Use GeoPy's distance function to calculate how far away the user is 
        from a particular food truck (in miles). """
    food_truck_location = (row["Latitude"], row["Longitude"])
    return distance.distance(food_truck_location, user_location).miles

def sort_by_distance(data):
    """ Sort our data in place by DistanceFromUser, ascending. """
    data.sort_values(by=['DistanceFromUser'], inplace = True)

def display_results(data):
    """ Show the user a list of the closest food trucks. """
    results = data.head(10)

    print()
    print("=" * 60)
    print("= We found some food trucks near you. Let's eat!")
    print("=" * 60, end="\n\n")

    for row in results.itertuples():
        print(f"{row.Applicant}")
        print(f"{row.DistanceFromUser:.2f} miles away -- {row.Address} ({row.Latitude:.4f}, {row.Longitude:.4f})")
        print(f"{row.FoodItems}", end="\n\n")

def main():
    user_location = parse_user_input()

    # Fetch the food truck data and save it to disk (if not already present)
    if not os.path.isfile(FOOD_TRUCK_DATA_CSV):
        download_latest_data()

    data = read_local_data()
    clean_data(data)

    calculate_distances(data, user_location)
    sort_by_distance(data)
    display_results(data)

## Run the script
main()
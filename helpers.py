""" This is a stash of functions which are not used by the
    mainline code but have proven useful while debugging. """

def print_trimmed_data(data):
    columns_to_keep = ['Applicant', 'FacilityType', 'Address', 'FoodItems', 'Latitude', 'Longitude', 'DistanceFromUser']
    columns_to_drop = data.columns.difference(columns_to_keep)
    trimmed_data = data.drop(columns = columns_to_drop)
    print(trimmed_data)
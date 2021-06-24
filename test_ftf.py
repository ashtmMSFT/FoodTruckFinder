import ftf
import pandas
import unittest

class TestFoodTruckFinder(unittest.TestCase):

    def test_full_golden_path(self):
        results = ftf.main(user_input = ["37.7775", "-122.416389"])
        
        # Confirm info for 10 trucks was returned
        self.assertEqual(len(results), 10)

        # Confirm a column was added to the truck data containing the distance away from the user
        self.assertTrue("DistanceFromUser" in results)

        # Confirm the results were sorted by distance, ascending
        truck_distance_from_user = results["DistanceFromUser"]
        for i in range(0, len(results) - 1):
            self.assertLessEqual(truck_distance_from_user.iloc[i], truck_distance_from_user.iloc[i + 1])

    def test_parse_user_input_not_enough_args(self):
        with self.assertRaises(SystemExit):
            user_location = ftf.parse_user_input([])

    def test_parse_user_input_too_many_args(self):
        with self.assertRaises(SystemExit):
            user_location = ftf.parse_user_input(["37.0", "-122.0", "53.0"])

    def test_parse_user_input_incorrect_types(self):
        with self.assertRaises(SystemExit):
            user_location = ftf.parse_user_input(["aaa", "bbb"])

    def test_clean_data(self):
        data = pandas.DataFrame({
            "Applicant": ["Truck A", "Truck B", "Truck C", "Truck D"],
            "Latitude": [0.0, 1.0, 1.0, 1.0],
            "Longitude": [1.0, 0.0, 1.0, 1.0],
            "Status": ["APPROVED", "APPROVED", "EXPIRED", "APPROVED"],
        })

        # Confirm we're starting with four test trucks
        self.assertEqual(len(data), 4)

        ftf.clean_data(data)

        # Confirm Truck D is the only remaining truck, as it was the only
        # one with non-zero lat/longs and an APPROVED status
        self.assertEqual(len(data), 1)
        self.assertEqual(data.iloc[0].Applicant, "Truck D")

    def test_calculate_distances(self):
        user_location = ["37.7775", "-122.416389"]

        data = pandas.DataFrame({
            "Applicant": ["Truck A"],
            "Latitude": [37.7850],
            "Longitude": [-122.4057],
        })

        # Calculated using https://latlongdata.com/distance-calculator/
        actual_distance_between_user_and_truck = 0.781

        self.assertFalse("DistanceFromUser" in data)
        ftf.calculate_distances(data, user_location)
        self.assertTrue("DistanceFromUser" in data)
        self.assertAlmostEqual(data.iloc[0].DistanceFromUser, actual_distance_between_user_and_truck, 3)

    def test_calculate_distance_to_truck(self):
        user_location = ["37.7775", "-122.416389"]

        data = pandas.DataFrame({
            "Applicant": ["Truck A"],
            "Latitude": [37.7850],
            "Longitude": [-122.4057],
        })

        # Calculated using https://latlongdata.com/distance-calculator/
        actual_distance_between_user_and_truck = 0.781

        distance = ftf.calculate_distance_to_truck(data.iloc[0], user_location)
        self.assertAlmostEqual(distance, actual_distance_between_user_and_truck, 3)

    def test_sort_by_distance(self):
        data = pandas.DataFrame({
            "Applicant": ["Truck A", "Truck B", "Truck C", "Truck D"],
            "DistanceFromUser": [30, 10, 50, 20]
        })

        ftf.sort_by_distance(data)

        sorted_distances = data["DistanceFromUser"]
        for i in range(0, len(data) - 1):
            self.assertLessEqual(sorted_distances.iloc[i], sorted_distances.iloc[i + 1])


if __name__ == '__main__':
    unittest.main()
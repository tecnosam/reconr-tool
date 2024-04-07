import datetime
import unittest


from reconr import (
    read_csv,
    find_missing_records,
    find_discrapancies
)


class TestReconrFunctions(unittest.TestCase):

    def setUp(self):

        test_source = "./source.csv"
        test_target = "./target.csv"

        source = read_csv(test_source, False)
        target = read_csv(test_target, False)

    def test_read_csv(self):

        test_fn = "./source.csv"

        correct = {
            '001': {'Name': 'john doe', 'Date': datetime.date(2023, 1, 1), 'Amount': 100.0},
            '002': {'Name': 'jane smith', 'Date': datetime.date(2023, 1, 2), 'Amount': 200.5},
            '003': {'Name': 'robert brown', 'Date': datetime.date(2023, 1, 3), 'Amount': 300.75}
        }

        self.assertEqual(read_csv(test_fn, False), correct)

    def test_find_missing_records(self):

        test_source = "./source.csv"
        test_target = "./target.csv"

        source = read_csv(test_source, False)
        target = read_csv(test_target, False)

        missing_in_source, missing_in_target = find_missing_records(source, target)

        self.assertEqual(missing_in_source, {'004'})
        self.assertEqual(missing_in_target, {'003'})

    def test_find_discrapancies(self):

        test_source = "./source.csv"
        test_target = "./target.csv"

        source = read_csv(test_source, False)
        target = read_csv(test_target, False)


        disc = find_discrapancies(source, target)

        self.assertEqual(len(disc), 1)


if __name__ == '__main__':

    unittest.main()

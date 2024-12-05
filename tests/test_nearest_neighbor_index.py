"""nn_search_test"""

import random
import time
import unittest

from pynn import NearestNeighborIndex


class NearestNeighborIndexTest(unittest.TestCase):
    def test_empty(self):

        # input an empty dataset to ensure the algorithm returns none
        uut = NearestNeighborIndex([])
        self.assertIsNone(uut.find_nearest((0, 0)))

    def test_singe_point(self):

        # input a single point and ensure the algorithm returns that point
        uut = NearestNeighborIndex([(1, 1)])
        self.assertEqual((1, 1), uut.find_nearest((1, 1)))
        self.assertEqual((1, 1), uut.find_nearest((6, 6)))
        self.assertEqual((1, 1), uut.find_nearest((12, 12)))

    def test_identical(self):

        # test to make sure identical points function correctly
        uut = NearestNeighborIndex([(3, 3), (3, 3), (3, 3)])
        self.assertEqual((3, 3), uut.find_nearest((1, 1)))

    def test_large(self):

        # test performance and integrity with large dataset

        def rand_point():
            return (random.uniform(-1e7, 1e7), random.uniform(-1e7, 1e7))

        index_points = [rand_point() for _ in range (100000)]
        query_points = [rand_point() for _ in range (1000)]

        uut = NearestNeighborIndex(index_points)

        for query_point in query_points:
            nearest = uut.find_nearest(query_point)
            self.assertIsNotNone(nearest)



    def test_basic(self):
        """
        test_basic tests a handful of nearest neighbor queries to make sure they return the right
        result.
        """

        test_points = [
            (1, 2),
            (1, 0),
            (10, 5),
            (-1000, 20),
            (3.14159, 42),
            (42, 3.14159),
        ]

        uut = NearestNeighborIndex(test_points)

        self.assertEqual((1, 0), uut.find_nearest((0, 0)))
        self.assertEqual((-1000, 20), uut.find_nearest((-2000, 0)))
        self.assertEqual((42, 3.14159), uut.find_nearest((40, 3)))


    def test_dynamic_updates(self):

        # test to ensure the algorithm works even with insertions and deletions
        points = [(0, 0), (12, 12), (23, 23)]
        uut = NearestNeighborIndex(points)

        # do a query before an update
        self.assertEqual((12, 12), uut.find_nearest((13, 14)))

        # update by rebuilding the tree
        updates = points + [(13, 13)]
        uut = NearestNeighborIndex(updates)
        self.assertEqual((13, 13), uut.find_nearest((13, 14)))

        # update by removing two points
        updated_list = [(12, 12), (23, 23)]
        uut = NearestNeighborIndex(updated_list)
        self.assertEqual((23, 23), uut.find_nearest((19, 19)))


    def test_boundary(self):

        # test with extremely (relatively) small/large numbers
        points = [(1e10, 1e10), (-1e10, -1e10), (0,0)]
        uut = NearestNeighborIndex(points)

        self.assertEqual((1e10, 1e10), uut.find_nearest((1e10 - 1, 1e10 - 1)))
        self.assertEqual((-1e10, -1e10), uut.find_nearest((-1e10 + 1, -1e10 + 1)))
        self.assertEqual((0, 0), uut.find_nearest((3, 3)))


    def test_benchmark(self):
        """
        test_benchmark tests a bunch of values using the slow and fast version of the index
        to determine the effective speedup.
        """

        def rand_point():
            return (random.uniform(-1000, 1000), random.uniform(-1000, 1000))

        index_points = [rand_point() for _ in range(10000)]
        query_points = [rand_point() for _ in range(1000)]

        expected = []
        actual = []

        # Run the baseline slow tests to get the expected values.
        start = time.time()
        for query_point in query_points:
            expected.append(NearestNeighborIndex.find_nearest_slow(query_point, index_points))
        slow_time = time.time() - start

        # don't include the indexing time when benchmarking
        uut = NearestNeighborIndex(index_points)

        # Run the indexed tests
        start = time.time()
        for query_point in query_points:
            actual.append(uut.find_nearest(query_point))
        new_time = time.time() - start

        print(f"slow time: {slow_time:0.2f}sec")
        print(f"new time: {new_time:0.2f}sec")
        print(f"speedup: {(slow_time / new_time):0.2f}x")

import math

class NearestNeighborIndex:

    class KDNode:
        def __init__(self, point, left=None, right=None):
            self.point = point
            self.left = left
            self.right = right

    def __init__(self, points):
        self.points = points
        self.root = self.build_kd_tree(points, depth=0)

    def build_kd_tree(self, points, depth=0):
        if not points:
            return None

        axis = depth % 2
        points.sort(key=lambda x: x[axis])
        median = len(points) // 2

        return self.KDNode(
            point=points[median],
            left=self.build_kd_tree(points[:median], depth + 1),
            right=self.build_kd_tree(points[median + 1:], depth + 1)
        )

    def _nearest(self, node, query_point, depth, best):
        if node is None:
            return best

        dist = self._distance(query_point, node.point)
        if dist < best[1]:
            best = (node.point, dist)

        axis = depth % 2
        diff = query_point[axis] - node.point[axis]
        near_side = node.left if diff < 0 else node.right
        far_side = node.right if diff < 0 else node.left

        best = self._nearest(near_side, query_point, depth + 1, best)

        if abs(diff) < best[1]:
            best = self._nearest(far_side, query_point, depth + 1, best)

        return best

    @staticmethod
    def _distance(point1, point2):
        deltax = point1[0] - point2[0]
        deltay = point1[1] - point2[1]
        return math.sqrt(deltax * deltax + deltay * deltay)


    def find_nearest_fast(self, query_point):
        if not self.root:
            return None
        return self._nearest(self.root, query_point, depth=0, best=(None, float('inf')))[0]

    @staticmethod
    def find_nearest_slow(query_point, haystack):
        """
        find_nearest_slow returns the point that is closest to query_point. If there are no indexed
        points, None is returned.
        """

        min_dist = None
        min_point = None

        for point in haystack:
            deltax = point[0] - query_point[0]
            deltay = point[1] - query_point[1]
            dist = math.sqrt(deltax * deltax + deltay * deltay)
            if min_dist is None or dist < min_dist:
                min_dist = dist
                min_point = point

        return min_point

    def find_nearest(self, query_point):
        """
        TODO comment me.
        """

        # TODO implement me so this class runs much faster.
        return self.find_nearest_fast(query_point)


#
# class NearestNeighborIndex:
#     """
#     TODO give me a decent comment
#
#     NearestNeighborIndex is intended to index a set of provided points to provide fast nearest
#     neighbor lookup. For now, it is simply a stub that performs an inefficient traversal of all
#     points every time.
#     """
#
#     def __init__(self, points):
#         """
#         takes an array of 2d tuples as input points to be indexed.
#         """
#         self.points = points
#
#     @staticmethod
#     def find_nearest_slow(query_point, haystack):
#         """
#         find_nearest_slow returns the point that is closest to query_point. If there are no indexed
#         points, None is returned.
#         """
#
#         min_dist = None
#         min_point = None
#
#         for point in haystack:
#             deltax = point[0] - query_point[0]
#             deltay = point[1] - query_point[1]
#             dist = math.sqrt(deltax * deltax + deltay * deltay)
#             if min_dist is None or dist < min_dist:
#                 min_dist = dist
#                 min_point = point
#
#         return min_point
#
#     def find_nearest_fast(self, query_point):
#         """
#         TODO: Re-implement me with your faster solution.
#
#         find_nearest_fast returns the point that is closest to query_point. If there are no indexed
#         points, None is returned.
#         """
#
#         min_dist = None
#         min_point = None
#
#         for point in self.points:
#             deltax = point[0] - query_point[0]
#             deltay = point[1] - query_point[1]
#             dist = math.sqrt(deltax * deltax + deltay * deltay)
#             if min_dist is None or dist < min_dist:
#                 min_dist = dist
#                 min_point = point
#
#         return min_point
#
#     def find_nearest(self, query_point):
#         """
#         TODO comment me.
#         """
#
#         # TODO implement me so this class runs much faster.
#         return self.find_nearest_fast(query_point)

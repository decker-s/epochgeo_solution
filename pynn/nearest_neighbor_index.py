import math

"""
references used:
    https://johnlekberg.com/blog/2020-04-17-kd-tree.html: for actual implementation
    wikipedia: https://en.wikipedia.org/wiki/Nearest_neighbor_search (specifically the section on space partitioning
    
    I chose this algorithm because it seemed to be a quick way to query data that did not need to be rebuilt too often
    quickly. This was based off of the wikipedia page. Considering the application could vary a lot, this may result in 
    slowdown depending on application. Geospatial data with millions of people moving that needs to be updated on the 
    hour? Probably going to perform badly. Vehicles, tanks, ships, etc moving but everything else staying the same? Will 
    perform very well. 
    
    https://en.wikipedia.org/wiki/K-d_tree has an interesting video that may help understand 
        https://en.wikipedia.org/wiki/File:Kdtreeogg.ogv
    
    As does https://upload.wikimedia.org/wikipedia/commons/9/9c/KDTree-animation.gif 
        (found from https://stackoverflow.com/questions/1627305/nearest-neighbor-k-d-tree-wikipedia-proof)
        
"""


"""
Example usage for this class:
    points = [(1, 2), (3, 4), (5, 6)]
    index = NearestNeighborIndex(points)
    query_point = (4, 5)
    nearest = index.find_nearest(query_point)
    print(f"nearest point to {query_point} is {nearest}")
"""

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
        """
        A k-d tree uses recursion to build a tree from a list of points.
        It alternates splitting space along each dimension (in this case x and y).
        The points themselves are divided into two subsets at each level based on median values of the splitting
        dimension.


        Arguments are:
            - points: list of tuples (2D points to put into the k-d tree)
            - depth: int (current depth of recursion to determine the splitting dimension.

        Returns the root of the tree
        """

        # edge case if there are no points, just return none.
        # If you've reached the end of a branch you will end up here.
        if not points:
            return None

        # determines axis to split along depending on depth of recursion (alternates splitting x and y)
        axis = depth % 2

        # sorts points based off of the current axis, depth 0 is x, depth 1 is y
        points.sort(key=lambda x: x[axis])

        # find median point after sorting which splits data into two (roughly) equal (sub)sets
        median = len(points) // 2

        # creation of a new node. the median now becomes the root at this level of the tree.
        # the left child is made from points to left of median, right child from points to right of median
        return self.KDNode(
            point=points[median],
            left=self.build_kd_tree(points[:median], depth + 1),
            right=self.build_kd_tree(points[median + 1:], depth + 1)
        )

    def _nearest(self, node, query_point, depth, best):
        """
        recursively search the tree for the nearest point.

        Arguments are:
            - node: KDNode (the current node)
            - query_point: tuple (the point we are comparing other points to, we want to find what is closest to this)
            - depth: int (current level of recursion)
            - best: tuple (current best candidate (point, distance))

        Returns the best candidate after searching current node and corresponding subtrees.

        """

        # node empty? just return the previous best
        if node is None:
            return best

        # compute distance using a helper function
        dist = self._distance(query_point, node.point)

        # if distance beats our previous best, set that as our new best
        if dist < best[1]:
            best = (node.point, dist)

        # determine axis for our current depth
        axis = depth % 2

        # calculate difference to check which subtree to explore first
        diff = query_point[axis] - node.point[axis]
        near_side = node.left if diff < 0 else node.right
        far_side = node.right if diff < 0 else node.left

        # begin recursive search on the near side first
        best = self._nearest(near_side, query_point, depth + 1, best)

        # possible the far side could contain a closer point so we check it.
        # this case can occur if distance to splitting plane is < current best
        if abs(diff) < best[1]:
            best = self._nearest(far_side, query_point, depth + 1, best)

        return best

    @staticmethod
    def _distance(point1, point2):
        # normal euclidean distance function.
        deltax = point1[0] - point2[0]
        deltay = point1[1] - point2[1]
        return math.sqrt(deltax * deltax + deltay * deltay)


    def find_nearest(self, query_point):
        if not self.root:
            return None

        # we set best to a tuple of None (because initially no point is found) and inf because any valid distance will
        # be smaller. [0] contains the point itself, [1] being the distance
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


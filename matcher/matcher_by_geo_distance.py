from haversine import haversine
from geopy.point import Point
from geopy import distance

from matcher.matcher_type import MatcherType


EARTH_DIAMETER = 12715.43

class GeoDistanceCalculatorAbstraction(object):

    def calculate_distance(self):
        pass


class GeoDistanceImplementorAPI(object):

    def calculate_distance_between_points(self, point_a, point_b):
        pass


#######################################################################################################################
#       Concrete Implementors for Geo Distance                                                                        #
#######################################################################################################################

class GeoDistanceByHaversine(GeoDistanceImplementorAPI):
    """
    Calculate the distance between two geographical points with Haversine formula
    (http://en.wikipedia.org/wiki/Haversine_formula) using Haversine library (https://pypi.python.org/pypi/haversine)
    point_a and point_b must be tuples

    return distance in km
    """

    def calculate_distance_between_points(self, point_a, point_b):

        if isinstance(point_a, tuple) and isinstance(point_b, tuple):
            try:
                return haversine(point_a, point_b)
            except Exception as e:
                raise e
        else:
            raise TypeError


class GeoDistanceByGreatCircle(GeoDistanceImplementorAPI):
    """
    Calculate the distance by Great-circle distance (http://en.wikipedia.org/wiki/Great-circle_distance)
    between two geographical points using geopy library (https://code.google.com/p/geopy/wiki/GettingStarted)

    point_a and point_b must be tuples

    return distance in km or false in case of error
    """

    def calculate_distance_between_points(self, point_a, point_b):

        if isinstance(point_a, tuple):
            point_a = Point(str(point_a[0]) + ";" + str(point_a[1]))

        if isinstance(point_b, tuple):
            point_b = Point(str(point_b[0]) + ";" + str(point_b[1]))

        if isinstance(point_a, Point) and isinstance(point_b, Point):

            distance.distance = distance.GreatCircleDistance
            return distance.distance(point_a, point_b).km

        else:
            raise TypeError


class GeoDistanceByVincenty(GeoDistanceImplementorAPI):
    """
    Calculate the distance by Vincenty distance (http://en.wikipedia.org/wiki/Vincenty's_formulae)
    between two geographical points using geopy library (https://code.google.com/p/geopy/wiki/GettingStarted)

    point_a and point_b must be tuples

    return distance in km or false in case of error
    """

    def calculate_distance_between_points(self, point_a, point_b):

        if isinstance(point_a, tuple):
            point_a = Point(str(point_a[0]) + ";" + str(point_a[1]))

        if isinstance(point_b, tuple):
            point_b = Point(str(point_b[0]) + ";" + str(point_b[1]))

        if isinstance(point_a, Point) and isinstance(point_b, Point):

            return distance.distance(point_a, point_b).km

        else:
            raise TypeError


#######################################################################################################################
#       End Concretes Implementors for Geo Distance                                                                   #
#######################################################################################################################

#######################################################################################################################
#       Refined Abstraction for Geo Distance                                                                          #
#######################################################################################################################

class RefinedGeoDistanceCalculator(GeoDistanceCalculatorAbstraction):

    __point_a = None
    __point_b = None
    __concrete_implementor = None

    def __init__(self, point_a, point_b, concrete_implementor):
        if isinstance(point_a, tuple) and isinstance(point_b, tuple):
            self.__point_a = point_a
            self.__point_b = point_b
            self.__concrete_implementor = concrete_implementor
        else:
            raise TypeError

    def calculate_distance(self):
        return self.__concrete_implementor.calculate_distance_between_points(self.__point_a, self.__point_b)


#######################################################################################################################
#       End Bridge Desing Pattern                                                                                     #
#######################################################################################################################

class Radius(object):
    """
    class to define a weighted radius for GeoDistance Matcher.
    distance must be a float and distance must be in km
    weight must be a float between [0,1]

    from_distance is the initial distance of the radius
    to_distance is the final distance of the radius
    balanced_by_distance means that ratio result depending of distance of point in Radius.
    In case of balanced_by_distance min_ratio suggests the minimum of the ratio
    and max_ratio suggests the maximum of the possible ratio depending of the distance
    """
    __min = 0
    __max = 1
    __from_distance = 0
    __to_distance = 0
    __min_ratio = 0
    __max_ratio = 0
    __balanced_by_distance = False

    def __init__(self, from_distance, to_distance, max_ratio, min_ratio, balanced_by_distance=False):
        try:
            self.__from_distance = float(from_distance)
            self.__to_distance = float(to_distance)
            self.__balanced_by_distance = balanced_by_distance

            if (self.__min <= min_ratio <= self.__max) and (self.__min <= max_ratio <= self.__max):
                self.__min_ratio = float(min_ratio)
                self.__max_ratio = float(max_ratio)
            else:
                raise ValueError

        except Exception as e:
            raise e

    @property
    def get_from_distance(self):
        return self.__from_distance

    @property
    def get_to_distance(self):
        return self.__to_distance

    @property
    def get_balanced_by_distance(self):
        return self.__balanced_by_distance

    @property
    def get_min_ratio(self):
        return self.__min_ratio

    @property
    def get_max_ratio(self):
        return self.__max_ratio

    def balance_ratio_in_radius(self, distance):
        """
        if radius has configured balanced_by_distance the ratio is calculated depending of the distance in radius.
        0      d1         0.2 (Radius distances)
        |------|---------|
        1      ratio_1    0.8 (ratios)

        Ratio ratio_1 is calculated through the formula of the line which connects the two known points
        x1=(0,1) & x2=(0.2,0.8)

        In this way the formula is:     y - y1 = (y2 - y1 / x2 - x1) * (x -x1)

        It translated inside our variables is:

        y - get_max_ratio = ((get_min_ratio - get_max_ratio) / (get_to_distance - get_from_distance)) *
                            * (x - get_from_distance)

        If clear something up:

        y = [((get_min_ratio - get_max_ratio) / (get_to_distance - get_from_distance)) *
                            * (x - get_from_distance)] + get_max_ratio

        where x -> is the distance passed by parameter
        and y-> is the ratio tu return
        """
        if distance == self.get_from_distance:
            return self.get_max_ratio
        elif distance == self.get_to_distance:
            return self.get_min_ratio
        else:
            return ((((self.get_min_ratio - self.get_max_ratio) / (self.get_to_distance - self.get_from_distance)) *
                    (distance - self.get_from_distance)) + self.get_max_ratio)


class MatcherByGeoDistance(MatcherType):
    """
    Class to calculate Geo-Distance ratio matching of point B with respect to point A
    weighted_radiuses define concentric circles from point A. Each radius has a weight to balance the outcome.

    Each radius must be a Raduis instance
    point_a and point_b must be tuples
    """

    __concrete_implementor = None
    __weighted_radiuses = []
    __ratio_farther = 0

    def __init__(self, weighted_radiuses, concrete_implementor=GeoDistanceByVincenty(), ratio_farther=0):
        if self.__check_raduis(weighted_radiuses) and isinstance(concrete_implementor, GeoDistanceImplementorAPI):
            self.__weighted_radiuses = weighted_radiuses
            self.__concrete_implementor = concrete_implementor
            self.__ratio_farther = ratio_farther
        else:
            raise TypeError

    @property
    def get_concrete_implementor(self):
        return self.__concrete_implementor

    @property
    def get_weighted_radiuses(self):
        return self.__weighted_radiuses

    @property
    def get_ratio_farther(self):
        return self.__ratio_farther

    def __check_raduis(self, weighted_radiuses):
        """
        check if all elements of weighted_radiuses belongs to the same class Radius
        """
        for elem in weighted_radiuses:
            if not isinstance(elem, Radius):
                return False

        return True

    def __calculate_ratio(self, distance):
        """
        For a given distance, return the weight of the radius to which this belongs
        """
        for radius in self.__weighted_radiuses:
            if radius.get_from_distance <= distance <= radius.get_to_distance:
                if not radius.get_balanced_by_distance:
                    return radius.get_max_ratio
                else:
                    #Calculate ratio according distance between point_a and point_b
                    return radius.balance_ratio_in_radius(distance)

        #If not. Far Far away. There, where the wild things are. I'm sorry.
        # ratio = self.__ratio_farther means point_b is far away of greater Radius configured
        return self.get_ratio_farther

    def get_ratio_match(self, point_a, point_b):
        """
        Return the weight of the radius according to distance from point_a to point_b
        The weight of the radiuses is defined through __weighted_radiuses and Raduis Class

        ratio = self.__ratio_farther means point_b is far away of greater Radius configured
        """
        if ((not point_a is None) and (not point_b is None) and
                (isinstance(point_a, tuple) and isinstance(point_b, tuple)) and
                (len(point_a) > 0 and len(point_b) > 0)):

            return self.__calculate_ratio(RefinedGeoDistanceCalculator(
                point_a, point_b, self.__concrete_implementor).calculate_distance())
        else:
            return self.get_ratio_farther


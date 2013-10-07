from django.db.models.query import QuerySet
from matcher.matcher_type import MatcherType
from matcher.matcher_exceptions import MatcherException
from matcher.queryset_iterator import QuerySetIterator


class MatcherFieldConfiguration(object):
    """
    Class to define a Matcher Configuration

    matcher_type must be a MatcherType object
    field must be a str of a field identification
    weight must be a float between 0 and 1
    """
    __matcher_type = None
    __field = None
    __weight = None
    __min_weight = 0
    __max_weight = 1

    def __init__(self, matcher_type, field, weight, min=0, max=1):
        if isinstance(matcher_type, MatcherType) and isinstance(field, str) and isinstance(weight, float):
            self.__matcher_type = matcher_type
            self.__field = field
            if self.__min_weight <= weight <= self.__max_weight:
                self.__weight = weight
                self.__min_weight = 0
                self.__max_weight = 1
            else:
                raise ValueError
        else:
            raise TypeError

    @property
    def get_matcher_type(self):
        return self.__matcher_type

    @property
    def get_field(self):
        return self.__field

    @property
    def get_weight(self):
        return self.__weight

    @property
    def get_min_weight(self):
        return self.__min_weight

    @property
    def get_max_weight(self):
        return self.__max_weight


class Match(object):
    """
    Class to define a match result for Matcher

    Match ratio = 0 Worse match case
    Match ratio = 1 Better match case
    """
    __id = None
    __match_element = None
    __total_ratio = 0
    __match_log = []

    def __init__(self, match_element, total_ratio, match_log=[]):
        try:
            self.__match_element = match_element
            self.__match_log = match_log
            self.__total_ratio = total_ratio
        except Exception as e:
            raise e

    @property
    def get_id(self):
        return self.__id

    @property
    def get_match_element(self):
        return self.__match_element

    @property
    def get_match_log(self):
        return self.__match_log

    @property
    def get_total_ratio(self):
        return self.__total_ratio


class Matcher(object):
    """
    Class to define a Matcher.

    With a correct matcher configuration, a needle and hayloft,  the class try to find best matches of
    needle in hayloft.

    The Matcher Configuration defines the needle field, the MatcherType for use in search and his weight.
    """
    __needle = None
    __matches = []
    __matcher_configuration = []
    __threshold = 0

    def __init__(self, needle, matcher_configuration, threshold):
        if self.__check_configuration(matcher_configuration):
            self.__needle = needle
            self.__matcher_configuration = matcher_configuration
            self.__threshold = threshold
        else: raise TypeError

    @property
    def get_needle(self):
        return self.__needle

    @property
    def get_matches(self):
        return self.__matches

    @property
    def get_matcher_configuration(self):
        return self.__matcher_configuration

    @property
    def get_threshold(self):
        return self.__threshold

    def __check_configuration(self, matcher_configuration):
        """
        check if all elements of matcher_configuration belongs to the same class MatcherFieldConfiguration
        """
        for elem in matcher_configuration:
            if not isinstance(elem, MatcherFieldConfiguration):
                return False

        return True

    def __get_field_value(self, obj, field_str):
        if isinstance(obj, dict):
            try:
                return obj[field_str]
            except KeyError:
                raise MatcherException(1000, msg_to_append='%s key not exist.' % field_str)

        else:
            try:
                return getattr(obj, field_str)
            except AttributeError:
                raise MatcherException(1000, msg_to_append='%s Attribute not exist.' % field_str)

    def __balance_ratio(self, field_weight, ratio_result, max = 1):
        """
        balance the match ratio result for one field into general field weight
        if for 'name' field his weight is 30% and the ratio match results is 80%
        balance ratio is (80% * 30%) / 1 = 24%
        """
        if not isinstance(field_weight, float): field_weight = float(field_weight)

        return (field_weight * ratio_result) / max

    def __add_to_results(self, element, total_ratio, match_log = False):
        """
        add one match element to match results self.__matches with his matching pattern
        """
        if match_log:
            self.__matches.append(Match(element, total_ratio, match_log))
        else:
            self.__matches.append(Match(element, total_ratio))

    def __get_iterator(self, hayloft):
        return QuerySetIterator(hayloft).queryset_iterator()

    def search_matches(self, hayloft, logging = False, clean_matches=False):
        """
        Method to find the matches of self.__needle in hayloft
        To find the matches we use __matcher_configuration a list of MatcherFieldConfiguration which tell us the field
        of needle and hayloft element, the matcher type to execute to obtain the match ratio and the field weight in
        matching.

        If result of ratio matching for all fields in one __matcher_configuration element is greater or equal than
        self.____threshold, the hayloft element is added to self.__matches with his matching result.

        needle object class and hayloft element object class must be the same

        needle and hayloft can be objects or dicts
        """
        if clean_matches: self.__matches = []
        
        if self.__matcher_configuration and hayloft:

            if isinstance(hayloft, QuerySet):
                hayloft = self.__get_iterator(hayloft)

            #For each hayloft element
            for element in hayloft:
                #check object classes
                if self.__needle.__class__.__name__ == element.__class__.__name__:
                    ratio_balanced = 0
                    result_description = []
                    #For each Matcher Configuration in ____matcher_configuration
                    for config in self.__matcher_configuration:
                        needle_field = self.__get_field_value(self.__needle, config.get_field)
                        element_field = self.__get_field_value(element, config.get_field)

                        ratio = config.get_matcher_type.get_ratio_match(needle_field, element_field)

                        """try:
                            ratio = config.get_matcher_type.get_ratio_match(needle_field, element_field)
                        except (TypeError, ValueError) as e:
                            raise MatcherException(1002, msg_to_append=e)"""

                        ratio_balanced += self.__balance_ratio(config.get_weight, ratio, config.get_max_weight)

                        if logging:
                            result_description.append("%s - %s" % (str(ratio), element_field))

                    if ratio_balanced >= self.__threshold:
                        #append Match!!!
                        self.__add_to_results(element, ratio_balanced, result_description)

                else:
                    #the needle and hayloft element do not have the same class
                    raise TypeError

    def order_matches(self):
        """
        Order a matches list based on total_ratio attribute of Radius
        """
        self.get_matches.sort(key=lambda x: x.get_total_ratio, reverse=True)

    def get_distance_position_from_the_best(self, list_position):
        """
        Return the distance between a element in the list and the first element in the list
        It is needed that the list is ordered to perform this operation correctly.

        The distance is the elements ratios difference.
        """
        if list_position <= (len(self.get_matches) - 1):
            return self.get_matches[0].get_total_ratio - self.get_matches[list_position].get_total_ratio
        else:
            return -1

    def get_distance_position_with_next(self, list_position):
        """
        Return the distance between a element in the list and the next element in the list
        It is needed that the list is ordered to perform this operation correctly.

        The distance is the elements ratios difference.
        """
        if (list_position + 1) <= (len(self.get_matches) - 1):
            return self.get_matches[list_position].get_total_ratio - self.get_matches[list_position + 1].get_total_ratio
        else:
            return -1
import jellyfish

from fuzzywuzzy import fuzz

from matcher.matcher_type import MatcherType
from matcher.stringslipper import score


class MatchAlgorithm(object):
    """
    Interface for any Match Algorithm
    """

    def compare_two_texts(self, string_a, string_b, normalize_value=True):
        pass


class MatchBySimpleRatio(MatchAlgorithm):
    """
    Class to compare strings by Simple Ratio algorithm of fuzzywuzzy
    Return a value normalized between 0 and 1
    1 means a perfect similarity
    0 means means the worst similarity
    """

    def __normalized_value(self, value):
        return float(value) / 100

    def compare_two_texts(self, string_a, string_b, normalize_value=True):
        """
        Compare two string and return the value of Simple Ratio algorithm
        the value is normalized between 0 and 1 values.
        """
        if ((isinstance(string_a, unicode) and isinstance(string_b, unicode)) or
                (isinstance(string_a, str) and isinstance(string_b, str))):
            if normalize_value:
                return self.__normalized_value(fuzz.ratio(string_a, string_b))
            else:
                return fuzz.ratio(string_a, string_b)
        else:
            raise TypeError


class MatchByPartialRatio(MatchAlgorithm):
    """
    Class to compare strings by Partial Ratio algorithm of fuzzywuzzy
    Return a value normalized between 0 and 1
    1 means a perfect similarity
    0 means means the worst similarity
    """

    def __normalized_value(self, value):
        return float(value) / 100

    def compare_two_texts(self, string_a, string_b, normalize_value=True):
        """
        Compare two string and return the value of Partial Ratio algorithm
        the value is normalized between 0 and 1 values.
        """
        if ((isinstance(string_a, unicode) and isinstance(string_b, unicode)) or
                (isinstance(string_a, str) and isinstance(string_b, str))):
            if normalize_value:
                return self.__normalized_value(fuzz.partial_ratio(string_a, string_b))
            else:
                fuzz.partial_ratio(string_a, string_b)
        else:
            raise TypeError


class MatchByTokenSortRatio(MatchAlgorithm):
    """
    Class to compare strings by Token Sort Ratio algorithm of fuzzywuzzy
    Return a value normalized between 0 and 1
    1 means a perfect similarity
    0 means means the worst similarity
    """

    def __normalized_value(self, value):
        return float(value) / 100

    def compare_two_texts(self, string_a, string_b, normalize_value=True):
        """
        Compare two string and return the value of Token Sort Ratio algorithm
        the value is normalized between 0 and 1 values.
        """
        if ((isinstance(string_a, unicode) and isinstance(string_b, unicode)) or
                (isinstance(string_a, str) and isinstance(string_b, str))):
            if normalize_value:
                return self.__normalized_value(fuzz.token_sort_ratio(string_a, string_b))
            else:
                return fuzz.token_sort_ratio(string_a, string_b)
        else:
            raise TypeError


class MatchByTokenSetRatio(MatchAlgorithm):
    """
    Class to compare strings by Token Set Ratio algorithm of fuzzywuzzy
    Return a value normalized between 0 and 1
    1 means a perfect similarity
    0 means means the worst similarity
    """

    def __normalized_value(self, value):
        return float(value) / 100

    def compare_two_texts(self, string_a, string_b, normalize_value=True):
        """
        Compare two string and return the value of Token Set Ratio algorithm
        the value is normalized between 0 and 1 values.
        """
        if ((isinstance(string_a, unicode) and isinstance(string_b, unicode)) or
                (isinstance(string_a, str) and isinstance(string_b, str))):
            if normalize_value:
                return self.__normalized_value(fuzz.token_set_ratio(string_a, string_b))
            else:
                return fuzz.token_set_ratio(string_a, string_b)
        else:
            raise TypeError


class MatchByStringScore(MatchAlgorithm):
    """
    Class to compare strings by String Score algorithm of https://github.com/joshaven/string_score
    Return a value normalized between 0 and 1
    1 means a perfect similarity
    0 means means the worst similarity
    """

    def compare_two_texts(self, string_a, string_b):
        """
        Compare two string and return the value of String Score algorithm
        the value is normalized between 0 and 1 values.
        """
        if ((isinstance(string_a, unicode) and isinstance(string_b, unicode)) or
                (isinstance(string_a, str) and isinstance(string_b, str))):
            if string_a >= string_b:
                return score(string_a, string_b)
            else:
                return score(string_b, string_a)
        else:
            raise TypeError


class MatchByJaroDistance(MatchAlgorithm):
    """
    Class to compare strings by Jaro Distance algorithm http://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance
    Use a Jellyfish library https://github.com/sunlightlabs/jellyfish
    Return a value normalized between 0 and 1
    1 means a perfect similarity
    0 means means the worst similarity
    """

    def compare_two_texts(self, string_a, string_b):
        """
        Compare two string and return the value of Jaro algorithm
        the value is normalized between 0 and 1 values.
        """
        if ((isinstance(string_a, unicode) and isinstance(string_b, unicode)) or
                (isinstance(string_a, str) and isinstance(string_b, str))):
            return jellyfish.jaro_distance(string_a, string_b)
        else:
            raise TypeError


class MatchByLevenshteinDistance(MatchAlgorithm):
    """
    Class to compare strings by Levenshtein Distance algorithm http://en.wikipedia.org/wiki/Levenshtein_distance
    Use a Jellyfish library https://github.com/sunlightlabs/jellyfish
    Return a value normalized between 0 and 1
    1 means a perfect similarity
    0 means means the worst similarity
    """

    def __normalized_value(self, value):
        if value == 0: return 1
        elif value > 0 and value < 10: return 1 - (float(value) / 10)
        elif value >= 10 and value <= 99: return (1 - (float(value) / (10*10))) / 10
        else: return 0

    def compare_two_texts(self, string_a, string_b, normalize_value=True):
        """
        Compare two string and return the value of Levenshtein algorithm
        the value is normalized between 0 and 1 values.
        """
        if ((isinstance(string_a, unicode) and isinstance(string_b, unicode)) or
                (isinstance(string_a, str) and isinstance(string_b, str))):
            if normalize_value:
                return self.__normalized_value(jellyfish.levenshtein_distance(string_a, string_b))
            else:
                return jellyfish.levenshtein_distance(string_a, string_b)
        else:
            raise TypeError


class MatchByHammingDistance(MatchAlgorithm):
    """
    Class to compare strings by Hamming Distance algorithm http://en.wikipedia.org/wiki/Hamming_distance
    Use a Jellyfish library https://github.com/sunlightlabs/jellyfish
    Return a value normalized between 0 and 1
    1 means a perfect similarity
    0 means means the worst similarity
    """

    def __normalized_value(self, value):
        if value == 0: return 1
        elif value > 0 and value < 10: return 1 - (float(value) / 10)
        elif value >= 10 and value <= 99: return (1 - (float(value) / (10*10))) / 10
        else: return 0

    def compare_two_texts(self, string_a, string_b, normalize_value=True):
        """
        Compare two string and return the value of Hamming algorithm
        the value is normalized between 0 and 1 values.
        """
        if ((isinstance(string_a, unicode) and isinstance(string_b, unicode)) or
                (isinstance(string_a, str) and isinstance(string_b, str))):
            if normalize_value:
                return self.__normalized_value(jellyfish.hamming_distance(string_a, string_b))
            else:
                return jellyfish.hamming_distance(string_a, string_b)
        else:
            raise TypeError


#####################################################################################################################
#####################################################################################################################


class MatcherByText(MatcherType):
    """
    Class to calculate ratio matching for two strings using values of several algorithms.

    __mode indicates which case we want to take

    __mode = 2  # 0 = worse case ; 1 = average ; 2 = better case. Of all algorithms executed for get_matches catch
    the value indicated by the mode attribute.

    __default_algorithms = [MatchBySimpleRatio(), MatchByPartialRatio(), MatchByTokenSortRatio(),
                            MatchByTokenSetRatio(), MatchByStringScore(), MatchByJaroDistance(),
                            MatchByLevenshteinDistance(), MatchByHammingDistance(),
                            ]
    each algorithm must be a MatchAlgorithm instance
    """

    def __init__(self, mode=2, algorithms=[]):
        self.__mode = mode

        if algorithms and self.__check_algorithms(algorithms):
            self.__algorithms = algorithms
        else:
            self.__algorithms = [MatchBySimpleRatio(), MatchByPartialRatio(), MatchByTokenSortRatio(),
                                 MatchByTokenSetRatio(), MatchByStringScore(), MatchByJaroDistance(),
                                 MatchByLevenshteinDistance(), MatchByHammingDistance(),
            ]

    @property
    def get_mode(self):
        return self.__mode

    @property
    def get_algorithms(self):
        return self.__algorithms

    def __calculate_average(self, list):
        """
        Calculates the average of the elements of a list
        """
        return reduce(lambda x, y: x + y, list) / len(list)

    def __calculate_worse_case(self, list):
        """
        Return the min of the elements of a list
        """
        return min(list)

    def __calculate_better_case(self, list):
        """
        Return the max of the elements of a list
        """
        return max(list)

    def __check_algorithms(self, algorithms):
        """
        check if all elements of algorithms belongs to the same class MatchAlgorithm
        """
        for elem in algorithms:
            if not isinstance(elem, MatchAlgorithm):
                return False

        return True

    def get_ratio_match(self, string_a, string_b):
        """
        string_a and string_b are two str objects
        algorithms must be a list of class objects Match [MatchBySimpleRatio(), MatchByPartialRatio(), etc...]
        If algorithms is a empty list we instantiate all default objects algorithms in self.__default_algorithms
        """
        if not isinstance(string_a, str):
            try:
                string_a = u'' + string_a.encode('ascii', 'ignore')
            except Exception as e:
                raise TypeError(e)

        if not isinstance(string_b, str):
            try:
                string_b = u'' + string_b.encode('ascii', 'ignore')
            except Exception as e:
                raise TypeError(e)

        if len(string_a) > 0 and len(string_b) > 0:

            results = []
            for algorithm in self.__algorithms:
                results.append(algorithm.compare_two_texts(string_a, string_b))

            if self.__mode == 0: return self.__calculate_worse_case(results)
            elif self.__mode ==1: return self.__calculate_average(results)
            else: return self.__calculate_better_case(results)

        else:
            raise ValueError('Error in values of string Paramaters for matcher by text')










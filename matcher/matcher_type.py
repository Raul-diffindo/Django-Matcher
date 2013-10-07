

class MatcherType(object):
    """
    Interface for each Matcher functions. All matchers types must be implement get_ratio_match method between two
    objects and return a ratio value.
    """

    def get_ratio_match(self, object_a, object_b):
        pass

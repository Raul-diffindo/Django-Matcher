
class MatcherException(Exception):
    """
    This class handles all Matcher exceptions directly
    """

    _error_codes = {
        1000 : 'KeyError Exception in get_field of Needle or Element hayloft Dict. ',
        1001 : 'AttributeError Exception in get_field of Needle or Element hayloft Dict. ',
        1002 : 'Error in Needle or Element hayloft Values passed. ',
        1003 : 'Wrong Matcher Configuration',
    }

    def __init__(self, code, msg = None, msg_to_append = None):
        self.code = code
        if msg:
            self.message = msg
        elif msg_to_append:
            self.message = self._error_codes.get(code) + str(msg_to_append)
        else:
            self.message = self._error_codes.get(code)

    def __str__(self):
        return "Error %i: %s" % (self.code, self.message)


class MatcherByGeoDistanceException(Exception):
    """
    This class handles all Matcher By Geo Distance exceptions directly
    """

    _error_codes = {
        1000 : 'Radius Distances configuration Error. Integer division or modulo by zero',
    }

    def __init__(self, code, msg = None, msg_to_append = None):
        self.code = code
        if msg:
            self.message = msg
        elif msg_to_append:
            self.message = self._error_codes.get(code) + str(msg_to_append)
        else:
            self.message = self._error_codes.get(code)

    def __str__(self):
        return "Error %i: %s" % (self.code, self.message)
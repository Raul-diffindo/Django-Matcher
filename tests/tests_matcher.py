from apps.matcher.matcher_by_text import MatcherByText
from apps.matcher.matcher_by_geo_distance import MatcherByGeoDistance, Radius
from apps.matcher.matcher import Matcher, MatcherFieldConfiguration


class MatcherTest(object):

    place_a = {'Place': 'Camp Nou', 'Geopoint': (41.380853, 2.122907)}
    place_b = {'Place': 'santiago_bernabeu', 'Geopoint': (40.451585, -3.690375)}

    hayloft = [
        {'Place': 'Camp Nou', 'Geopoint': (41.380853, 2.122907)},
        {'Place': 'Santiago Bernabeu', 'Geopoint': (40.451585, -3.690375)},
        {'Place': 'Hotel NH Rallye', 'Geopoint': (41.381401, 2.126934)},
        {'Place': 'Jardins de Bacardi', 'Geopoint': (41.380077, 2.125314)},
        {'Place': 'Plaza Catalunya - BCN', 'Geopoint': ((41.386997, 2.168546))},
        {'Place': 'Estadio Santiago Bernabeu', 'Geopoint': (40.452135, -3.688716)},
        {'Place': 'Hotel NH Eurobuilding - Madrid', 'Geopoint': (40.458948, -3.685961)},
        {'Place': 'Plaza Mayor - Madrid', 'Geopoint': (40.415832, -3.707285)},
    ]

    test_radiuses = [Radius(0, 0.2, 1, 0.8, balanced_by_distance=True),
                     Radius(0.2, 1, 0.8, 0.5, balanced_by_distance=True),
                     Radius(1, 5, 0.5, 0, balanced_by_distance=True),
                     Radius(5, 10, 0.1, 0, balanced_by_distance=False)
                    ]

    matcher_config = [
        MatcherFieldConfiguration(MatcherByText(), 'Place', weight=0.3),
        MatcherFieldConfiguration(MatcherByGeoDistance(test_radiuses, ratio_farther=0), 'Geopoint', weight=0.7),
    ]

    def test_search_matches(self):
        my_matcher = Matcher(self.place_a, self.matcher_config, threshold=0)

        try:
            my_matcher.search_matches(self.hayloft, logging=True)
            if my_matcher.get_matches:
                print "Needle searched is: %s\n\n" % str(my_matcher.get_needle)
                for match in my_matcher.get_matches:
                    print "%s - %s - %s\n" % (match.get_match_element, str(match.get_total_ratio), match.get_match_log)
        except Exception as e:
            print "Exception: %s" % e
            pass


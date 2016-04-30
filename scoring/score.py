
from collections import Counter

class InvalidScoresheetException(Exception):
    pass

class Scorer:
    # Note: if the arena colours (from arena.yaml) change,
    # both this and the printed score-sheets will need to change
    ZONE_COLOURS = [
        'G',    # zone 0 = green
        'O',    # zone 1 = orange
        'P',    # zone 2 = purple
        'Y',    # zone 3 = yellow
    ]

    VALID_TOKENS = ZONE_COLOURS + ['W']

    def __init__(self, teams_data, arena_data):
        self._teams_data = teams_data
        self._arena_data = arena_data

        self._all_tokens = ''.join(d['tokens'] for d in arena_data.values()) \
                             .replace(' ', '')

    def calculate_scores(self):
        total_points = Counter(self._all_tokens)

        scores = {}
        for tla, info in self._teams_data.items():
            zone = info['zone']
            colour = self.ZONE_COLOURS[zone]
            corner_points = Counter(self._arena_data[zone]['tokens'])

            scores[tla] = corner_points[colour] + total_points[colour]

        return scores

    def validate(self, extra):

        num_tokens = len(self._all_tokens)
        if not num_tokens == 9:
            msg = "Should have exactly 9 tokens (got {0})".format(num_tokens)
            raise InvalidScoresheetException(msg)


        valid_tokens = set(self.VALID_TOKENS)
        actual_tokens = set(self._all_tokens)
        extras = actual_tokens - valid_tokens
        if extras:
            extras_str = ', '.join(extras)
            valid_str =  ', '.join(valid_tokens)
            msg = "Found invalid tokens {0} (valid: {1})".format(extras_str, valid_str)
            raise InvalidScoresheetException(msg)


if __name__ == '__main__':
    import libproton
    libproton.main(Scorer)

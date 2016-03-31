
from score import Scorer

# Path hackery
import os.path
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT)

from score import Scorer, InvalidScoresheetException

def test_scores_match_start():
    teams_data = {
        'ABC': {'zone': 0},
        'DEF': {'zone': 1},
        'GHI': {'zone': 2}
    }
    arena_data = {
        0: { 'tokens': '' },
        1: { 'tokens': '' },
        2: { 'tokens': '' },
        3: { 'tokens': '' },
        'other': { 'tokens': 'PWO WWW GWY' },
    }
    expected = {
        'ABC': 1,
        'DEF': 1,
        'GHI': 1,
    }

    scorer = Scorer(teams_data, arena_data)
    scores = scorer.calculate_scores()

    assert expected == scores, "Wrong scores!"

def test_scores_one_zone():
    teams_data = {
        'ABC': {'zone': 0},
        'DEF': {'zone': 1},
        'GHI': {'zone': 2}
    }
    arena_data = {
        0: { 'tokens': '' },
        1: { 'tokens': '' },
        2: { 'tokens': 'P' },
        3: { 'tokens': '' },
        'other': { 'tokens': 'O W W W W W W W' },
    }
    expected = {
        'ABC': 0,
        'DEF': 1,
        'GHI': 2
    }

    scorer = Scorer(teams_data, arena_data)
    scores = scorer.calculate_scores()

    assert expected == scores, "Wrong scores!"

def test_scores_others_zone():
    teams_data = {
        'ABC': {'zone': 0},
        'DEF': {'zone': 1},
        'GHI': {'zone': 2}
    }
   # zone 1 is orange, but purple still gets the upright point
    arena_data = {
        0: { 'tokens': '' },
        1: { 'tokens': 'P' },
        2: { 'tokens': '' },
        3: { 'tokens': '' },
        'other': { 'tokens': 'W W W W W W W W' },
    }
    expected = {
        'ABC': 0,
        'DEF': 0,
        'GHI': 1
    }

    scorer = Scorer(teams_data, arena_data)
    scores = scorer.calculate_scores()

    assert expected == scores, "Wrong scores!"

def test_validate_error_invalid_notation():
    teams_data = {
        'ABC': {'zone': 0},
        'DEF': {'zone': 1},
        'GHI': {'zone': 2}
    }
    arena_data = {
        0: { 'tokens': '' },
        1: { 'tokens': 'A' },
        2: { 'tokens': '' },
        3: { 'tokens': '' },
        'other': { 'tokens': 'W' * 8 },
    }

    try:
        scorer = Scorer(teams_data, arena_data)
        scores = scorer.validate(None)
    except InvalidScoresheetException:
        pass
    else:
        assert False, "Should error when there are invalid tokens"


def test_validate_error_too_few_tokens():
    teams_data = {
        'ABC': {'zone': 0},
        'DEF': {'zone': 1},
        'GHI': {'zone': 2}
    }
    arena_data = {
        0: { 'tokens': '' },
        1: { 'tokens': 'P' },
        2: { 'tokens': '' },
        3: { 'tokens': '' },
        'other': { 'tokens': 'W W' },
    }

    try:
        scorer = Scorer(teams_data, arena_data)
        scores = scorer.validate(None)
    except InvalidScoresheetException:
        pass
    else:
        assert False, "Should error when there are too few tokens"

def test_validate_error_too_many_tokens():
    teams_data = {
        'ABC': {'zone': 0},
        'DEF': {'zone': 1},
        'GHI': {'zone': 2}
    }
    arena_data = {
        0: { 'tokens': '' },
        1: { 'tokens': 'P P P P P P' },
        2: { 'tokens': '' },
        3: { 'tokens': '' },
        'other': { 'tokens': 'W W W W W W W W' },
    }

    try:
        scorer = Scorer(teams_data, arena_data)
        scores = scorer.validate(None)
    except InvalidScoresheetException:
        pass
    else:
        assert False, "Should error when there are too many tokens"

import pytest
from tennis_scoring import game_score, set_winner, match_status


# ---------- game_score ----------
def test_game_start():
    assert game_score(0, 0) == "0-0"

def test_game_normal_points():
    assert game_score(1, 2) == "15-30"

def test_game_points_below_deuce_zone():
    assert game_score(3, 0) == "40-0"

def test_game_negative_a_raises():
    with pytest.raises(ValueError):
        game_score(-1, 0)

def test_game_negative_b_raises():
    with pytest.raises(ValueError):
        game_score(0, -1)

def test_game_deuce():
    assert game_score(3, 3) == "deuce"

def test_game_deep_deuce():
    assert game_score(5, 5) == "deuce"

def test_game_advantage_a():
    assert game_score(4, 3) == "advantage A"

def test_game_advantage_b():
    assert game_score(3, 4) == "advantage B"

def test_game_won_by_a_after_deuce():
    assert game_score(5, 3) == "game A"

def test_game_won_by_b_after_deuce():
    assert game_score(3, 5) == "game B"

def test_game_a_reaches_four_points():
    assert game_score(4, 0) == "game A"

def test_game_b_reaches_four_points():
    assert game_score(0, 4) == "game B"


# ---------- set_winner ----------
def test_set_undecided():
    assert set_winner(3, 2) is None

def test_set_a_wins_6_0():
    assert set_winner(6, 0) == "A"

def test_set_b_wins_0_6():
    assert set_winner(0, 6) == "B"

def test_set_a_wins_7_5():
    assert set_winner(7, 5) == "A"

def test_set_b_wins_5_7():
    assert set_winner(5, 7) == "B"

def test_set_tiebreak_a_wins():
    assert set_winner(7, 6) == "A"

def test_set_tiebreak_b_wins():
    assert set_winner(6, 7) == "B"

def test_set_six_all_undecided():
    assert set_winner(6, 6) is None

def test_set_six_five_undecided():
    assert set_winner(6, 5) is None


# ---------- match_status ----------
def test_match_in_progress_start():
    assert match_status(0, 0, 3) == "in progress"

def test_match_a_wins_best_of_3():
    assert match_status(2, 0, 3) == "A wins"

def test_match_b_wins_best_of_3():
    assert match_status(0, 2, 3) == "B wins"

def test_match_decider_best_of_3():
    assert match_status(1, 1, 3) == "decider"

def test_match_in_progress_best_of_5():
    assert match_status(2, 1, 5) == "in progress"

def test_match_a_wins_best_of_5():
    assert match_status(3, 1, 5) == "A wins"

def test_match_b_wins_best_of_5():
    assert match_status(1, 3, 5) == "B wins"

def test_match_decider_best_of_5():
    assert match_status(2, 2, 5) == "decider"

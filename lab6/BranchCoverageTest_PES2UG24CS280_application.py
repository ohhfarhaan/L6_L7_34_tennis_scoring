import pytest
from tennis_scoring import game_score, set_winner, match_status


# ---------- game_score ----------
# Decision 1: if a < 0 or b < 0
def test_game_branch_negative_a_true():
    with pytest.raises(ValueError):
        game_score(-1, 2)

def test_game_branch_negative_b_true():
    with pytest.raises(ValueError):
        game_score(2, -1)

def test_game_branch_both_non_negative_false():
    assert game_score(1, 1) == "15-15"

# Decision 2: if a >= 3 and b >= 3 (True)
def test_game_branch_deuce_zone_true():
    assert game_score(3, 3) == "deuce"

# Decision 2 (False): a >= 3 true but b < 3
def test_game_branch_a_high_b_low_false():
    assert game_score(3, 2) == "40-30"

# Decision 2 (False): a < 3 short-circuits
def test_game_branch_a_low_false():
    assert game_score(2, 3) == "30-40"

# Decision 3: if a == b (True inside deuce zone)
def test_game_branch_equal_true():
    assert game_score(4, 4) == "deuce"

# Decision 3 (False): a != b inside deuce zone
def test_game_branch_equal_false():
    assert game_score(4, 3) == "advantage A"

# Decision 4: if a - b >= 2 (True)
def test_game_branch_a_two_ahead_true():
    assert game_score(5, 3) == "game A"

# Decision 5: if b - a >= 2 (True)
def test_game_branch_b_two_ahead_true():
    assert game_score(3, 5) == "game B"

# Decision 6: if a > b (True) -> advantage A
def test_game_branch_a_greater_true():
    assert game_score(4, 3) == "advantage A"

# Decision 6 (False): falls through to advantage B
def test_game_branch_a_greater_false():
    assert game_score(3, 4) == "advantage B"

# Decision 7: if a >= 4 (True, outside deuce zone)
def test_game_branch_a_at_four_true():
    assert game_score(4, 0) == "game A"

# Decision 7 (False) and Decision 8 (True): b >= 4
def test_game_branch_b_at_four_true():
    assert game_score(0, 4) == "game B"

# Decision 8 (False): neither player at 4 -> normal points
def test_game_branch_normal_points_false():
    assert game_score(2, 1) == "30-15"


# ---------- set_winner ----------
# Decision 1: if a >= 6 and a - b >= 2 (True)
def test_set_branch_a_wins_true():
    assert set_winner(6, 4) == "A"

# Decision 1 (False): a >= 6 but lead is only 1
def test_set_branch_a_lead_one_false():
    assert set_winner(6, 5) is None

# Decision 1 (False): a below 6
def test_set_branch_a_below_six_false():
    assert set_winner(5, 3) is None

# Decision 2: if b >= 6 and b - a >= 2 (True)
def test_set_branch_b_wins_true():
    assert set_winner(4, 6) == "B"

# Decision 2 (False): b >= 6 but lead is only 1
def test_set_branch_b_lead_one_false():
    assert set_winner(5, 6) is None

# Decision 2 (False): b below 6
def test_set_branch_b_below_six_false():
    assert set_winner(3, 5) is None

# Decision 3: if a == 7 and b == 6 (True)
def test_set_branch_tiebreak_a_true():
    assert set_winner(7, 6) == "A"

# Decision 3 (False): a == 7 but b != 6
def test_set_branch_a_seven_b_not_six_false():
    assert set_winner(7, 5) == "A"

# Decision 3 (False): a != 7, b == 6 (reaches decision 4 check)
def test_set_branch_tiebreak_a_false_then_b_check():
    assert set_winner(6, 6) is None

# Decision 4: if b == 7 and a == 6 (True)
def test_set_branch_tiebreak_b_true():
    assert set_winner(6, 7) == "B"

# Decision 4 (False): all checks fail -> None
def test_set_branch_all_false_returns_none():
    assert set_winner(7, 7) is None


# ---------- match_status ----------
# Decision 1: if sets_a == needed (True)
def test_match_branch_a_wins_true_bo3():
    assert match_status(2, 0, 3) == "A wins"

# Decision 1 (False) and Decision 2 (True): sets_b == needed
def test_match_branch_b_wins_true_bo3():
    assert match_status(1, 2, 3) == "B wins"

# Decision 2 (False) and Decision 3 (True): both at needed - 1
def test_match_branch_decider_true_bo3():
    assert match_status(1, 1, 3) == "decider"

# Decision 3 (False): needed - 1 only for one player
def test_match_branch_decider_false_bo3():
    assert match_status(1, 0, 3) == "in progress"

# Best-of-5 boundaries
def test_match_branch_a_wins_true_bo5():
    assert match_status(3, 2, 5) == "A wins"

def test_match_branch_b_wins_true_bo5():
    assert match_status(2, 3, 5) == "B wins"

def test_match_branch_decider_true_bo5():
    assert match_status(2, 2, 5) == "decider"

def test_match_branch_in_progress_bo5():
    assert match_status(2, 1, 5) == "in progress"

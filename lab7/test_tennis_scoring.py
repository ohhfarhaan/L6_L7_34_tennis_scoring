from hypothesis import given, strategies as st
from tennis_scoring import parse_score, game_lead, set_spread

POINT_LABELS = ["0", "15", "30", "40"]


# ---------- Fuzz tests: arbitrary / malformed input must never crash ----------

@given(st.text() | st.none())
def test_parse_score_no_crash(s):
    try:
        parse_score(s)
    except Exception as e:
        assert False, f"parse_score crashed with: {e!r}"


@given(st.text() | st.none())
def test_game_lead_no_crash(s):
    try:
        game_lead(s)
    except Exception as e:
        assert False, f"game_lead crashed with: {e!r}"


@given(st.text() | st.none())
def test_set_spread_no_crash(s):
    try:
        set_spread(s)
    except Exception as e:
        assert False, f"set_spread crashed with: {e!r}"


# Targeted fuzzing: inputs built from the characters the parsers care about,
# so Hypothesis explores near-valid strings (empty parts, extra separators,
# signs, spaces) far more often than plain st.text() would.

@given(st.text(alphabet="0123456789-, +"))
def test_parse_score_near_valid_no_crash(s):
    try:
        parse_score(s)
    except Exception as e:
        assert False, f"parse_score crashed on {s!r} with: {e!r}"


@given(st.text(alphabet="01345-AD "))
def test_game_lead_near_valid_no_crash(s):
    try:
        game_lead(s)
    except Exception as e:
        assert False, f"game_lead crashed on {s!r} with: {e!r}"


@given(st.text(alphabet="0123456789,- "))
def test_set_spread_near_valid_no_crash(s):
    try:
        set_spread(s)
    except Exception as e:
        assert False, f"set_spread crashed on {s!r} with: {e!r}"


# ---------- Property tests: valid input must still give the right answer ----------

@given(st.integers(min_value=0, max_value=999_999), st.integers(min_value=0, max_value=999_999))
def test_parse_score_valid_round_trip(a, b):
    assert parse_score(f"{a}-{b}") == (a, b)


@given(st.sampled_from(POINT_LABELS), st.sampled_from(POINT_LABELS))
def test_game_lead_valid(first, second):
    expected = POINT_LABELS.index(first) - POINT_LABELS.index(second)
    assert game_lead(f"{first}-{second}") == expected


@given(st.lists(st.integers(min_value=0, max_value=7), min_size=1, max_size=5))
def test_set_spread_valid(games):
    csv = ",".join(str(g) for g in games)
    assert set_spread(csv) == max(games) - min(games)

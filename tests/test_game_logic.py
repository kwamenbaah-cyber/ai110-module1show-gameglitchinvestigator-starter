import pytest
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score


# ── get_range_for_difficulty ──────────────────────────────────────────────────

def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_hard_range():
    assert get_range_for_difficulty("Hard") == (1, 50)

def test_unknown_difficulty_falls_back_to_normal():
    assert get_range_for_difficulty("Unknown") == (1, 100)


# ── parse_guess ───────────────────────────────────────────────────────────────

def test_parse_valid_integer():
    ok, val, err = parse_guess("42")
    assert ok is True
    assert val == 42
    assert err is None

def test_parse_empty_string():
    ok, val, err = parse_guess("")
    assert ok is False
    assert val is None

def test_parse_none():
    ok, val, err = parse_guess(None)
    assert ok is False

def test_parse_non_numeric():
    ok, val, err = parse_guess("abc")
    assert ok is False
    assert "not a number" in err.lower()

def test_parse_decimal_truncates_to_int():
    ok, val, err = parse_guess("7.9")
    assert ok is True
    assert val == 7

def test_parse_negative_number():
    ok, val, err = parse_guess("-5")
    assert ok is True
    assert val == -5


# ── check_guess ───────────────────────────────────────────────────────────────

def test_correct_guess_returns_win():
    outcome, msg = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in msg

def test_guess_above_secret_is_too_high():
    outcome, msg = check_guess(60, 50)
    assert outcome == "Too High"

def test_too_high_hint_says_lower():
    # Regression: original bug returned "Go HIGHER!" when guess exceeded secret
    _, msg = check_guess(60, 50)
    assert "LOWER" in msg

def test_guess_below_secret_is_too_low():
    outcome, msg = check_guess(40, 50)
    assert outcome == "Too Low"

def test_too_low_hint_says_higher():
    # Regression: original bug returned "Go LOWER!" when guess was below secret
    _, msg = check_guess(40, 50)
    assert "HIGHER" in msg

def test_guess_far_above_secret():
    outcome, msg = check_guess(99, 1)
    assert outcome == "Too High"
    assert "LOWER" in msg

def test_guess_far_below_secret():
    outcome, msg = check_guess(1, 99)
    assert outcome == "Too Low"
    assert "HIGHER" in msg


# ── update_score ──────────────────────────────────────────────────────────────

def test_win_on_first_attempt_gives_good_score():
    score = update_score(0, "Win", 1)
    assert score > 0

def test_too_high_decreases_score():
    # Regression: original added 5 points on even attempts for wrong guesses
    score = update_score(50, "Too High", 2)
    assert score < 50

def test_too_low_decreases_score():
    score = update_score(50, "Too Low", 1)
    assert score < 50

def test_score_floor_on_late_win():
    # Winning very late should still award at least 10 points
    score = update_score(0, "Win", 100)
    assert score >= 10

def test_unknown_outcome_does_not_change_score():
    score = update_score(75, "Unknown", 3)
    assert score == 75
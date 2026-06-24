def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.
    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."
    if raw == "":
        return False, None, "Enter a guess."
    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."
    return True, value, None


def check_guess(guess: int, secret: int):
    """
    Compare guess to secret and return (outcome, message).
    outcome examples: "Win", "Too High", "Too Low"

    FIX: Original code had hints inverted — "Go HIGHER!" when guess was too
    high, and "Go LOWER!" when guess was too low. Fixed by swapping messages.
    Also removed the string-comparison branch that caused wrong results on
    even-numbered attempts.
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        # FIX: was returning "📈 Go HIGHER!" — incorrect when guess exceeds secret
        return "Too High", "📉 Go LOWER!"
    # FIX: was returning "📉 Go LOWER!" — incorrect when guess is below secret
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.

    FIX: Original added 5 points on even attempts for "Too High" guesses,
    rewarding wrong answers. All wrong guesses now consistently subtract 5.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points
    # FIX: removed the even/odd branch that gave points for wrong guesses
    if outcome in ("Too High", "Too Low"):
        return current_score - 5
    return current_score
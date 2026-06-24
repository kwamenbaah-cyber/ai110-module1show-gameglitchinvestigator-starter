# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the fixed app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.**
   - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game purpose:** A number guessing game where the player tries to identify a hidden number within a limited number of attempts. The difficulty setting controls both the number range (Easy: 1–20, Normal: 1–100, Hard: 1–50) and the number of allowed attempts. Each wrong guess deducts 5 points from your score; winning early earns more points than winning on the last attempt.

**Bugs found:**
1. Hints were inverted — "Go HIGHER!" displayed when the guess exceeded the secret, and "Go LOWER!" when it was below.
2. On every even-numbered attempt, the app cast the secret number to a string and passed it into `check_guess`, causing string comparison instead of numeric comparison and producing wrong or missed wins.
3. `update_score` added 5 points for "Too High" guesses on even attempts instead of subtracting — wrong guesses rewarded the player.
4. The "New Game" button always generated a random number between 1 and 100 regardless of difficulty, so Hard difficulty effectively had the same range as Normal.
5. The hint text was hardcoded to "Guess a number between 1 and 100" even when playing Easy or Hard.
6. `st.session_state.attempts` was initialized to 1 instead of 0, causing the displayed "Attempts left" to be off by one from the start.

**Fixes applied:**
- Swapped return messages in `check_guess` so "Too High" → "Go LOWER!" and "Too Low" → "Go HIGHER!".
- Removed the even/odd string-cast in `app.py`; `check_guess` now always receives two integers.
- Removed the points-for-wrong-guess branch in `update_score`; all non-win outcomes subtract 5.
- Fixed "New Game" to use `random.randint(low, high)` derived from the current difficulty.
- Replaced hardcoded range text with `{low}` and `{high}` variables.
- Changed `attempts` initialization from 1 to 0.
- Moved all four game logic functions into `logic_utils.py` and updated `app.py` to import them.

## 📸 Demo Walkthrough

1. User opens the app and selects **Normal** difficulty (range 1–100, 8 attempts).
2. The sidebar confirms "Range: 1 to 100" and "Attempts allowed: 8". The secret number (visible in Developer Debug Info) is, for example, **63**.
3. User types **40** and clicks **Submit Guess**. The app shows "📉 Go LOWER! ... wait, no — 📈 Go HIGHER!" — hint correctly says **Go HIGHER** because 40 < 63. Score drops to −5.
4. User types **80**. Hint correctly says **Go LOWER** because 80 > 63. Score drops to −10.
5. User types **63**. App shows 🎉 Correct!, balloons appear, and the final score is displayed. Game status is set to "won" and further guesses are blocked until a new game starts.
6. User clicks **New Game**. Score resets to 0, a new secret is drawn from the correct difficulty range, attempt counter resets to 0, and the game is ready to play again.

## 🧪 Test Results

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0
rootdir: /home/claude/project
collected 22 items

tests/test_game_logic.py::test_easy_range PASSED                         [  4%]
tests/test_game_logic.py::test_normal_range PASSED                       [  9%]
tests/test_game_logic.py::test_hard_range PASSED                         [ 13%]
tests/test_game_logic.py::test_unknown_difficulty_falls_back_to_normal PASSED [ 18%]
tests/test_game_logic.py::test_parse_valid_integer PASSED                [ 22%]
tests/test_game_logic.py::test_parse_empty_string PASSED                 [ 27%]
tests/test_game_logic.py::test_parse_none PASSED                         [ 31%]
tests/test_game_logic.py::test_parse_non_numeric PASSED                  [ 36%]
tests/test_game_logic.py::test_parse_decimal_truncates_to_int PASSED     [ 40%]
tests/test_game_logic.py::test_parse_negative_number PASSED              [ 45%]
tests/test_game_logic.py::test_correct_guess_returns_win PASSED          [ 50%]
tests/test_game_logic.py::test_guess_above_secret_is_too_high PASSED     [ 54%]
tests/test_game_logic.py::test_too_high_hint_says_lower PASSED           [ 59%]
tests/test_game_logic.py::test_guess_below_secret_is_too_low PASSED      [ 63%]
tests/test_game_logic.py::test_too_low_hint_says_higher PASSED           [ 68%]
tests/test_game_logic.py::test_guess_far_above_secret PASSED             [ 72%]
tests/test_game_logic.py::test_guess_far_below_secret PASSED             [ 77%]
tests/test_game_logic.py::test_win_on_first_attempt_gives_good_score PASSED [ 81%]
tests/test_game_logic.py::test_too_high_decreases_score PASSED           [ 86%]
tests/test_game_logic.py::test_too_low_decreases_score PASSED            [ 90%]
tests/test_game_logic.py::test_score_floor_on_late_win PASSED            [ 95%]
tests/test_game_logic.py::test_unknown_outcome_does_not_change_score PASSED [100%]

============================== 22 passed in 0.04s
==============================
```

## 🚀 Stretch Features

*(No stretch features attempted for this submission.)*
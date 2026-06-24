# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

The first time I ran the app, it looked like a normal number guessing game but immediately fell apart when I started playing. The hints were backwards — if I guessed too high, the game told me to go higher, which pointed me in the wrong direction every single time. Even when I used the Developer Debug Info panel to see the secret number and guessed it exactly, the game sometimes wouldn't register it as a win because on even-numbered attempts, the code was secretly converting the secret number to a string and doing a string comparison instead of a numeric one. On top of that, the "Hard" difficulty sidebar still said the range was 1 to 100 even though Hard is supposed to use 1 to 50, and wrong guesses sometimes added points to my score instead of subtracting them.

Two concrete bugs:
- **Hints inverted**: Guessing higher than the secret returned "Go HIGHER!" — the opposite of the correct feedback.
- **String/int type switch**: On every even-numbered attempt, the app cast the secret to a string before comparing, so `check_guess(50, "50")` fell into a string comparison path that produced wrong outcomes.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 100 (secret = 50) | "Too High — Go LOWER!" | "Go HIGHER!" displayed | None |
| 50 (secret = 50, attempt #2) | "Win 🎉" | "Too Low" shown (string vs int comparison) | None |
| Any wrong guess on even attempt | Score decreases by 5 | Score *increases* by 5 | None |
| Hard difficulty selected | Sidebar shows range 1–50 | Sidebar shows "Guess between 1 and 100" | None |

---

## 2. How did you use AI as a teammate?

I used Claude (claude.ai) as my primary AI tool throughout this project.

**Correct suggestion:** I asked Claude to explain why the hints were backwards and it immediately spotted the logic in `check_guess` — the original code returned `"📈 Go HIGHER!"` when `guess > secret`, which is the wrong direction. Claude suggested swapping the return messages so that a guess above the secret returns `"Go LOWER!"` and a guess below returns `"Go HIGHER!"`. I verified this by running `check_guess(60, 50)` directly in a Python shell and confirming the output changed to `"Too High"` with the `"Go LOWER!"` message, then playing the game and checking hints matched the debug panel.

**Incorrect/misleading suggestion:** When I asked Claude to explain the score bug, it initially suggested the fix was to remove the `attempt_number % 2 == 0` check and replace it with a flat `-5` for all wrong outcomes, but it also proposed keeping a separate "streak penalty" multiplier that would have added new complexity rather than just removing the bug. I rejected the multiplier — the spec says nothing about streaks and adding unrequested features would have made the score logic harder to test. I applied only the flat `-5` fix and verified with the `test_too_high_decreases_score` pytest test, which confirmed that `update_score(50, "Too High", 2)` now returns 45.

---

## 3. Debugging and testing your fixes

My process for deciding a bug was fixed had two steps: first confirm the function in isolation, then confirm the behavior in the running app. For example, after fixing `check_guess`, I wrote a pytest test asserting that `check_guess(60, 50)` returns `("Too High", ...)` with `"LOWER"` in the message and `check_guess(40, 50)` returns `("Too Low", ...)` with `"HIGHER"` in the message. Both passed. Then I opened the app, looked at the secret in the debug panel, and deliberately guessed above and below it to watch the hints in real time.

The most revealing test was the regression test for the string comparison bug — `check_guess(50, "50")` used to return `"Win"` by accident because `"50" == 50` is False in Python but the fallback string branch compared `str(50) > "50"` as False and fell through to `"Too Low"`. After refactoring `check_guess` to only accept integers, that entire broken branch was gone and the test suite confirmed no int-to-string coercion was happening anymore.

Claude helped me design the edge cases — I asked it to think of inputs that might still slip through after my fixes, and it suggested testing negative numbers, decimals, and the boundary guess equal to the secret. All three were useful and are now in the test file.

---

## 4. What did you learn about Streamlit and state?

Streamlit reruns the entire Python script from top to bottom every time a user interacts with the page — clicking a button, typing in a text box, or changing a dropdown all trigger a full rerun. This means any variable you define normally (like `secret = random.randint(1, 100)`) gets reset to a new value on every interaction, which is why the original game's secret number kept changing. `st.session_state` is Streamlit's solution: it's a dictionary-like object that persists across reruns, so values stored there survive from one interaction to the next. Think of it like a small locker that stays open between page refreshes — anything you put in it is still there the next time the script runs. The pattern `if "secret" not in st.session_state: st.session_state.secret = random.randint(...)` means "only set the secret once; after that, leave it alone."

---

## 5. Looking ahead: your developer habits

One habit I want to keep is writing a regression test immediately after fixing a bug — before moving on. This project made it obvious that bugs can reappear silently when you change other parts of the code, and a test that specifically targets the original broken behavior is the fastest way to catch that. If `check_guess` ever gets refactored again, the test for inverted hints will catch any regression instantly.

Next time I work with AI on a coding task, I would give the model the test output alongside the code, not just the code alone. Claude's explanations were sharper and more specific when I could paste in what `pytest` actually printed compared to what I expected — it could see exactly which assertion failed and why, rather than guessing at the failure mode. The one thing this project changed about how I think about AI-generated code is that I now assume it has at least one non-obvious logic bug until I've read every branch myself. The hints bug in this project looked completely fine at a quick glance — the comparison `guess > secret` is correct — but the wrong message was attached to the wrong branch, which only shows up when you trace through what each return value means.
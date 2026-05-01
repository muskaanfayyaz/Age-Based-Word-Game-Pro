# Age Based Word Game Pro — Edition ✦

A professional-grade, cross-platform terminal word puzzle game built with Python. Featuring age-adaptive difficulty, real-time HUD rendering, and persistent leaderboards.

---

## 🚀 Features

- **Age-Adaptive Engine:** Word banks and difficulty scaling automatically adjust based on the player's age (Kids, Teens, Adults).
- **Real-Time HUD:** A flicker-free, 4-line terminal interface that updates live with a countdown timer, score tracking, and instant feedback.
- **Dynamic Difficulty:** Word lengths and the number of hidden letters (blanks) scale as you progress through 10 challenging levels.
- **Hint System:** Trade points for letters when you're stuck.
- **Persistent Leaderboard:** Saves high scores locally to `leaderboard.json`.
- **Cross-Platform Input:** Optimized for both Windows (`msvcrt`) and Unix-based systems (`termios`/`select`).
- **Audio Feedback:** Non-blocking beeps for correct/wrong guesses and level completions (Windows native, terminal bell fallback).

---

## 🛠️ Installation & Usage

### Prerequisites
- Python 3.8 or higher.

### Running the Game
1. Clone or download the repository to your local machine.
2. Navigate to the project directory:
   ```bash
   cd "word game"
   ```
3. Launch the game:
   ```bash
   python main.py
   ```

*Optional: Run with `DEBUG=1 python main.py` for full stack traces on errors.*

---

## 🎮 How to Play

1. **Setup:** Enter your name and age. The game will select a word set appropriate for your age group.
2. **Guessing:** Type a single letter and press **Enter**.
3. **Hints:** Type `?` and press **Enter** to reveal a random letter. This costs **5 points**.
4. **Quitting:** Type `quit` and press **Enter** during a level to return to the main menu.
5. **Goal:** Solve all words in the level before the timer hits zero to advance.

---

## 🏗️ Technical Architecture

The project is modularized into several core components:

- **`main.py`**: The entry point. Handles the global exception wrapper and initializes the `GameEngine`.
- **`engine.py`**: The heart of the game.
  - `GameEngine`: Manages the high-level flow (intro, player setup, level loop, report).
  - `Level`: Manages the logic for a single level, including word loops and guess handling.
  - `WordGenerator`: Handles age-group filtering and level-based word selection.
  - `HUD`: Manages the complex ANSI-based terminal rendering for the real-time interface.
- **`config.py`**: Centralized configuration for age groups, word banks (thousands of words), level settings, and point systems.
- **`input_handler.py`**: A low-level utility to capture keyboard input without blocking the main execution thread, allowing the timer to update live.
- **`utils.py`**: Contains ANSI color styles, audio helpers, and leaderboard I/O logic.

---

## 📊 Scoring System

- **Correct Guess:** Instant visual feedback and sound.
- **Wrong Guess:** Penalty of **2 points** (cannot go below zero).
- **Hint:** Costs **5 points**.
- **Level Completion:** Points awarded per word solved, scaling with level difficulty.
- **Grand Champion:** Complete all 10 levels to earn the title!

---

## 📝 License
This project is provided for educational and entertainment purposes. Feel free to modify and extend it!

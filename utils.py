# utils.py — Cross-platform helpers for Word Game Pro

import json
import os
import sys
import threading
import config

# ── ANSI STYLES ─────────────────────────────────────────────────
class Style:
    BLUE         = '\033[94m'
    CYAN         = '\033[96m'
    GREEN        = '\033[92m'
    YELLOW       = '\033[93m'
    RED          = '\033[91m'
    MAGENTA      = '\033[95m'
    BRIGHT_WHITE = '\033[97m'
    DIM          = '\033[2m'
    BOLD         = '\033[1m'
    UNDERLINE    = '\033[4m'
    RESET        = '\033[0m'
    CLEAR        = '\033[H\033[J'

    # Convenience combos
    SUCCESS  = '\033[1m\033[92m'   # bold green
    DANGER   = '\033[1m\033[91m'   # bold red
    INFO     = '\033[1m\033[96m'   # bold cyan
    WARNING  = '\033[1m\033[93m'   # bold yellow

# ── SOUND ────────────────────────────────────────────────────────
def _beep(freq: int, duration_ms: int) -> None:
    """Non-blocking beep — Windows native, silent fallback elsewhere."""
    if sys.platform == "win32":
        try:
            import winsound
            threading.Thread(
                target=winsound.Beep,
                args=(freq, duration_ms),
                daemon=True,
            ).start()
        except Exception:
            pass
    else:
        # ANSI terminal bell — audible if terminal supports it
        sys.stdout.write('\a')
        sys.stdout.flush()

def play_correct():  _beep(1000, 180)
def play_wrong():    _beep(350,  350)
def play_level_up(): _beep(1500, 450)
def play_win():
    for freq in (800, 1000, 1200, 1500):
        _beep(freq, 120)

# ── TERMINAL HELPERS ─────────────────────────────────────────────
def hide_cursor() -> None:
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor() -> None:
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def clear_line() -> None:
    sys.stdout.write("\r\033[K")
    sys.stdout.flush()

def move_up(n: int) -> None:
    sys.stdout.write(f"\033[{n}A")
    sys.stdout.flush()

def print_banner(text: str, color: str = Style.CYAN, width: int = 54) -> None:
    border = "═" * width
    print(f"\n{color}╔{border}╗")
    print(f"║{text.center(width)}║")
    print(f"╚{border}╝{Style.RESET}\n")

def print_line(char: str = "─", width: int = 54, color: str = Style.DIM) -> None:
    print(f"{color}{char * width}{Style.RESET}")

# ── INPUT HELPERS ────────────────────────────────────────────────
def get_input(prompt: str, required: bool = True) -> str:
    while True:
        sys.stdout.write(f"{Style.YELLOW}{prompt}{Style.RESET}")
        sys.stdout.flush()
        val = input().strip()
        if not val and required:
            print(f"{Style.RED}  ✖  Input cannot be empty.{Style.RESET}")
            continue
        return val

def get_int_input(prompt: str, min_val: int = 0, max_val: int = 120) -> int:
    while True:
        sys.stdout.write(f"{Style.YELLOW}{prompt}{Style.RESET}")
        sys.stdout.flush()
        try:
            val = int(input().strip())
            if min_val <= val <= max_val:
                return val
            print(f"{Style.RED}  ✖  Enter a number between {min_val} and {max_val}.{Style.RESET}")
        except ValueError:
            print(f"{Style.RED}  ✖  Please enter a valid number.{Style.RESET}")

# ── LEADERBOARD ──────────────────────────────────────────────────
def load_leaderboard() -> list:
    if not os.path.exists(config.LEADERBOARD_FILE):
        return []
    try:
        if os.path.getsize(config.LEADERBOARD_FILE) == 0:
            return []
        with open(config.LEADERBOARD_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError, ValueError):
        return []

def save_score(name: str, score: int) -> None:
    data = load_leaderboard()

    # Keep only the player's personal best
    existing = next((e for e in data if e["name"].lower() == name.lower()), None)
    if existing:
        if score > existing["score"]:
            existing["score"] = score
    else:
        data.append({"name": name, "score": score})

    data = sorted(data, key=lambda x: x["score"], reverse=True)[:config.MAX_LEADERBOARD]

    try:
        with open(config.LEADERBOARD_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except OSError as e:
        print(f"{Style.RED}  ✖  Could not save leaderboard: {e}{Style.RESET}")

def show_leaderboard() -> None:
    data = load_leaderboard()
    if not data:
        print(f"{Style.DIM}  No scores yet — be the first!{Style.RESET}\n")
        return

    width = 54
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}

    print(f"\n{Style.WARNING}{'🏆  TOP LEGENDS  🏆'.center(width)}{Style.RESET}")
    print_line("═", width, Style.YELLOW)
    print(f"{Style.DIM}{'#':<4} {'NAME':<18} {'SCORE':>8}{Style.RESET}")
    print_line("─", width, Style.DIM)

    for i, entry in enumerate(data, 1):
        medal = medals.get(i, f"{i:>2}.")
        if i == 1:
            row_color = Style.WARNING
        elif i <= 3:
            row_color = Style.CYAN
        else:
            row_color = Style.RESET
        name  = entry["name"][:16]
        score = entry["score"]
        print(f"{row_color}{medal:<4} {name:<18} {score:>6} pts{Style.RESET}")

    print_line("═", width, Style.YELLOW)
    print()
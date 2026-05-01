# engine.py — Word Game Pro  |  Core game engine

import random
import time
import sys

import config
import utils
from utils import Style
from input_handler import get_input_with_timer


# ── HELPERS ──────────────────────────────────────────────────────
def fmt_time(seconds: int) -> str:
    m, s = divmod(max(0, seconds), 60)
    return f"{m:02}:{s:02}"


def _timer_color(remaining: int, total: int) -> str:
    ratio = remaining / max(total, 1)
    if ratio > 0.5:
        return Style.GREEN
    if ratio > 0.25:
        return Style.YELLOW
    return Style.DANGER


# ── DATA CLASSES ─────────────────────────────────────────────────
class Player:
    __slots__ = ("name", "age", "total_score", "words_solved",
                 "hints_used", "wrong_guesses", "levels_completed")

    def __init__(self, name: str, age: int) -> None:
        self.name             = name
        self.age              = age
        self.total_score      = 0
        self.words_solved     = 0
        self.hints_used       = 0
        self.wrong_guesses    = 0
        self.levels_completed = 0


# ── WORD GENERATOR ───────────────────────────────────────────────
class WordGenerator:
    """
    Picks words for each level with three guarantees:
      1. No word repeats across the entire game session.
      2. Word length scales with age group AND level band.
      3. Blanks scale from easy (few) to hard (many) across levels.
    """

    def __init__(self, age: int) -> None:
        self.age        = age
        self._used: set = set()   # words already seen this session
        self._group     = self._age_group()
        # Pre-shuffle the full bank once; slices are taken from it per level
        self._bank      = list(dict.fromkeys(config.WORD_BANKS[self._group]))
        random.shuffle(self._bank)

    def _age_group(self) -> str:
        for group, (lo, hi) in config.AGE_GROUPS.items():
            if lo <= self.age <= hi:
                return group
        return "adults"

    def _length_range(self, level: int) -> tuple:
        band = config.level_band(level)
        return config.WORD_LENGTH[self._group][band]

    def _candidates(self, level: int) -> list:
        """Words that fit the length range and haven't been used yet."""
        lo, hi = self._length_range(level)
        return [w for w in self._bank if lo <= len(w) <= hi and w not in self._used]

    def get_level_words(self, level: int, count: int) -> list:
        candidates = self._candidates(level)

        # If the length-filtered pool is too small, relax length constraint
        if len(candidates) < count:
            candidates = [w for w in self._bank if w not in self._used]

        # Still not enough? Reset used set for this level only (last resort)
        if len(candidates) < count:
            self._used.clear()
            candidates = self._candidates(level)
            if len(candidates) < count:
                candidates = self._bank[:]

        random.shuffle(candidates)
        chosen = candidates[:count]
        self._used.update(chosen)
        return chosen

    def make_puzzle(self, word: str, level: int) -> list:
        """
        Replace a portion of letters with '_'.
        Blank ratio: 30 % at level 1 → 75 % at level 10.
        Always at least 1 blank; always at least 1 letter visible.
        """
        blank_ratio  = 0.30 + (min(level, 10) - 1) * 0.05   # 0.30 … 0.75
        blanks_count = max(1, min(len(word) - 1, round(len(word) * blank_ratio)))
        chars        = list(word)
        for i in random.sample(range(len(word)), blanks_count):
            chars[i] = "_"
        return chars


# ── HUD ──────────────────────────────────────────────────────────
class HUD:
    """
    4-line in-place HUD.  ALL output during a guess round goes through
    here — no stray print() calls — so the cursor never drifts.

    Lines:
        1  stats bar   (level / word index / score / timer)
        2  puzzle      (revealed letters + blanks)
        3  input line  (prompt + typed chars + cursor)
        4  feedback    (result of last guess — cleared on next render)
    """

    LINES = 4

    def __init__(
        self,
        player:      Player,
        level_num:   int,
        words_total: int,
        time_limit:  int,
        word:        str,
    ) -> None:
        self.player      = player
        self.level_num   = level_num
        self.words_total = words_total
        self.time_limit  = time_limit
        self.word        = word
        self.word_idx    = 1
        self._first      = True
        self._feedback   = ""          # shown on line 4; replaced each render

    def set_feedback(self, msg: str) -> None:
        """Store a feedback message to display on the next render cycle."""
        self._feedback = msg

    def render(self, remaining: int, puzzle: list[str], input_str: str, prompt: str) -> None:
        p = self.player

        # Line 1 — stats bar
        tc        = _timer_color(remaining, self.time_limit)
        score_col = Style.SUCCESS if p.total_score > 0 else Style.RESET
        stats = (
            f"{Style.INFO}LVL {self.level_num}{Style.RESET}  "
            f"{Style.DIM}│{Style.RESET}  "
            f"WORD {self.word_idx}/{self.words_total}  "
            f"{Style.DIM}│{Style.RESET}  "
            f"{score_col}⭐ {p.total_score} pts{Style.RESET}  "
            f"{Style.DIM}│{Style.RESET}  "
            f"{tc}⏱  {fmt_time(remaining)}{Style.RESET}"
        )

        # Line 2 — puzzle
        cells = []
        for ch in puzzle:
            if ch == "_":
                cells.append(f"{Style.DIM}_{Style.RESET}")
            else:
                cells.append(f"{Style.SUCCESS}{ch.upper()}{Style.RESET}")
        puzzle_line = f"{Style.BOLD}PUZZLE:{Style.RESET}  {' '.join(cells)}"

        # Line 3 — input
        cursor   = f"{Style.YELLOW}▌{Style.RESET}"
        hint_tip = f"  {Style.DIM}[? = hint]{Style.RESET}"
        inp_line = (
            f"{Style.CYAN}{prompt}{Style.RESET}"
            f"{Style.BRIGHT_WHITE}{input_str}{Style.RESET}"
            f"{cursor}{hint_tip}"
        )

        # Line 4 — feedback (blank when nothing to show)
        fb_line = self._feedback if self._feedback else ""

        # Move cursor back up over the previous 4-line block
        if not self._first:
            sys.stdout.write(f"\033[{self.LINES}A")
        self._first = False

        for line in (stats, puzzle_line, inp_line, fb_line):
            sys.stdout.write("\r\033[K" + line + "\n")
        sys.stdout.flush()

    def clear(self) -> None:
        """Erase all HUD lines so normal output can follow cleanly."""
        sys.stdout.write(f"\033[{self.LINES}A")
        for _ in range(self.LINES):
            sys.stdout.write("\r\033[K\n")
        sys.stdout.write(f"\033[{self.LINES}A")
        sys.stdout.flush()


# ── LEVEL ────────────────────────────────────────────────────────
class Level:
    def __init__(self, number: int) -> None:
        self.number   = number
        self.settings = config.LEVEL_SETTINGS.get(number, config.LEVEL_SETTINGS[5])

    # ── hint helper ──
    @staticmethod
    def _apply_hint(player: Player, word: str, puzzle: list[str]) -> tuple[list[str], bool]:
        if player.total_score < config.HINT_COST:
            return puzzle, False
        blanks = [i for i, ch in enumerate(puzzle) if ch == "_"]
        if not blanks:
            return puzzle, False
        player.total_score -= config.HINT_COST
        player.hints_used  += 1
        idx          = random.choice(blanks)
        new_puzzle   = puzzle[:]
        new_puzzle[idx] = word[idx]
        return new_puzzle, True

    def _handle_guess(self, player: Player, word: str, puzzle: list[str], choice: str, hud: HUD) -> list[str]:
        # ── validate: single letter (normalise FIRST) ──
        choice = choice.strip().lower()
        
        if choice == "quit":
            return None # Special signal for quitting

        if len(choice) != 1 or not choice.isalpha():
            hud.set_feedback(f"  {Style.RED}✖  Type ONE letter then press Enter.{Style.RESET}")
            return puzzle

        # ── already fully revealed ──
        letter_positions = [i for i, ch in enumerate(word) if ch == choice]
        if letter_positions and not any(puzzle[i] == "_" for i in letter_positions):
            hud.set_feedback(
                f"  {Style.DIM}'{choice.upper()}' already revealed — try another letter.{Style.RESET}"
            )
            return puzzle

        # ── apply guess ──
        new_puzzle = puzzle[:]
        matched    = False
        for i, ch in enumerate(word):
            if ch == choice and puzzle[i] == "_":
                new_puzzle[i] = choice
                matched = True
        
        if matched:
            count = sum(1 for c in new_puzzle if c == choice)
            hud.set_feedback(
                f"  {Style.SUCCESS}✔  '{choice.upper()}' correct! "
                f"{count} match{'es' if count > 1 else ''}{Style.RESET}"
            )
            utils.play_correct()
        else:
            penalty = min(config.WRONG_GUESS_PENALTY, player.total_score)
            player.total_score   = max(0, player.total_score - config.WRONG_GUESS_PENALTY)
            player.wrong_guesses += 1
            hud.set_feedback(
                f"  {Style.DANGER}✖  '{choice.upper()}' not in word  (-{penalty} pts){Style.RESET}"
            )
            utils.play_wrong()
            
        return new_puzzle

    # ── main play loop ──
    def play(self, player: Player, generator: WordGenerator) -> bool:
        utils.print_banner(f"🚀  LEVEL {self.number}", Style.BLUE)
        s = self.settings
        print(
            f"  {Style.CYAN}Words:{Style.RESET} {s['words']}   "
            f"{Style.CYAN}Time:{Style.RESET} {fmt_time(s['time'])}   "
            f"{Style.CYAN}Bonus:{Style.RESET} +{s['points']} pts/word\n"
        )
        print(
            f"  {Style.DIM}● Type a letter & press Enter to guess\n"
            f"  ● Press {Style.RESET}{Style.WARNING}?{Style.RESET}"
            f"{Style.DIM} then Enter to use a hint  "
            f"(costs {config.HINT_COST} pts){Style.RESET}\n"
        )
        time.sleep(1.2)

        words      = generator.get_level_words(self.number, s["words"])
        start_time = time.time()

        for word_idx, word in enumerate(words, 1):
            puzzle = generator.make_puzzle(word, self.number)

            # ── word header ──
            utils.print_line("-", 54, Style.DIM)
            print(
                f"  {Style.INFO}Word {word_idx}/{len(words)}{Style.RESET}  "
                f"{Style.DIM}|  {len(word)} letters"
                f"  |  {Style.RESET}{Style.WARNING}? + Enter{Style.RESET}"
                f"{Style.DIM} = hint (-{config.HINT_COST} pts){Style.RESET}"
            )
            print()

            hud = HUD(
                player      = player,
                level_num   = self.number,
                words_total = len(words),
                time_limit  = s["time"],
                word        = word,
            )
            hud.word_idx = word_idx

            # ── inner guess loop ──
            while "_" in puzzle:

                def _render(rem: int, inp: str, pmt: str) -> None:  # noqa: E731
                    hud.render(rem, puzzle, inp, pmt)

                choice, timed_out = get_input_with_timer(
                    prompt       = "Guess › ",
                    start_time   = start_time,
                    time_limit   = s["time"],
                    hud_renderer = _render,
                )

                # ── timed out ──
                if timed_out:
                    hud.clear()
                    utils.print_banner("⏰  TIME'S UP!", Style.DANGER)
                    time.sleep(1.5)
                    return False

                # ── hint request ──
                if choice == "?":
                    puzzle, granted = self._apply_hint(player, word, puzzle)
                    if granted:
                        blanks_left = puzzle.count("_")
                        hud.set_feedback(
                            f"  {Style.WARNING}💡 Hint revealed a letter! "
                            f"{blanks_left} blank(s) left  (-{config.HINT_COST} pts){Style.RESET}"
                        )
                    else:
                        hud.set_feedback(
                            f"  {Style.DANGER}✖  Need {config.HINT_COST} pts for a hint "
                            f"(you have {player.total_score} pts){Style.RESET}"
                        )
                    continue

                # ── handle guess ──
                result = self._handle_guess(player, word, puzzle, choice, hud)
                if result is None: # Quit signal
                    hud.clear()
                    return False
                puzzle = result

            # ── word solved — clear HUD then print the reveal ──
            hud.clear()
            player.total_score += s["points"]
            player.words_solved += 1
            reveal = " ".join(ch.upper() for ch in word)
            print(f"  {Style.SUCCESS}★  {reveal}{Style.RESET}  "
                  f"{Style.DIM}+{s['points']} pts{Style.RESET}\n")

        # ── level complete ──
        utils.play_level_up()
        player.levels_completed += 1
        utils.print_banner(f"🌟  LEVEL {self.number} COMPLETE! 🌟", Style.GREEN)
        return True


# ── GAME ENGINE ──────────────────────────────────────────────────
class GameEngine:
    _LOGO = f"""\
{Style.BOLD}{Style.CYAN}
 ██╗    ██╗ ██████╗ ██████╗ ██████╗      ██████╗  █████╗ ███╗   ███╗███████╗
 ██║    ██║██╔═══██╗██╔══██╗██╔══██╗    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝
 ██║ █╗ ██║██║   ██║██████╔╝██║  ██║    ██║  ███╗███████║██╔████╔██║█████╗
 ██║███╗██║██║   ██║██╔══██╗██║  ██║    ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝
 ╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝    ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗
  ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝      ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝
                          ✦  P R O  E D I T I O N  ✦
{Style.RESET}"""

    def start(self) -> None:
        print(Style.CLEAR, end="")
        print(self._LOGO)
        utils.show_leaderboard()

        # ── player setup ──
        name = utils.get_input("  👤  Your name   : ")
        age  = utils.get_int_input("  🎂  Your age    : ", 5, 100)
        print()

        player    = Player(name, age)
        generator = WordGenerator(age)

        group_desc = {
            "kids":   "Perfect for young learners",
            "teens":  "Challenge your vocabulary",
            "adults": "The ultimate mental workout",
        }
        desc = group_desc.get(generator._group, "Custom set")
        
        print(f"  {Style.CYAN}Welcome, {Style.BOLD}{name}!{Style.RESET}  ")
        print(f"  {Style.DIM}{desc} ({generator._group.capitalize()} Mode){Style.RESET}\n")
        time.sleep(1.0)

        # ── level loop ──
        for lvl_num in range(1, 11):
            success = Level(lvl_num).play(player, generator)

            if not success:
                print(f"\n  {Style.DIM}You made it to level {lvl_num} "
                      f"with {player.total_score} pts.{Style.RESET}\n")
                break

            if lvl_num == 10:
                utils.play_win()
                utils.print_banner("👑  GRAND CHAMPION  👑", Style.YELLOW)
                time.sleep(1.5)
                break

            choice = utils.get_input(
                f"  ▶  Continue to Level {lvl_num + 1}? (y/n) : "
            ).lower()
            if choice != "y":
                break

        # ── final report ──
        self._show_report(player)
        utils.save_score(player.name, player.total_score)
        utils.show_leaderboard()
        print(f"  {Style.CYAN}Thanks for playing Word Game Pro, {player.name}!{Style.RESET}\n")
        input("  Press Enter to exit…")

    # ── report ──
    @staticmethod
    def _show_report(player: Player) -> None:
        width = 54
        utils.print_line("═", width, Style.YELLOW)
        print(f"{Style.WARNING}{'🏆  PERFORMANCE REPORT  🏆'.center(width)}{Style.RESET}")
        utils.print_line("═", width, Style.YELLOW)

        rows = [
            ("Player",           player.name),
            ("Levels completed", str(player.levels_completed)),
            ("Words solved",     str(player.words_solved)),
            ("Wrong guesses",    str(player.wrong_guesses)),
            ("Hints used",       str(player.hints_used)),
            ("Final score",      f"{player.total_score} pts"),
        ]
        for label, value in rows:
            print(f"  {Style.DIM}{label:<20}{Style.RESET}{Style.BOLD}{value}{Style.RESET}")

        utils.print_line("═", width, Style.YELLOW)
        print()
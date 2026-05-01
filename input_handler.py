# input_handler.py — Cross-platform real-time character input

import sys
import time

# ── PLATFORM-SPECIFIC GETCH ─────────────────────────────────────
if sys.platform == "win32":
    import msvcrt

    def _kbhit() -> bool:
        return msvcrt.kbhit()

    def _getch() -> bytes:
        return msvcrt.getch()

else:
    import tty
    import termios
    import select

    def _kbhit() -> bool:
        return bool(select.select([sys.stdin], [], [], 0)[0])

    def _getch() -> bytes:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            return ch.encode("utf-8", errors="replace")
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


# ── SPECIAL KEY CONSTANTS ────────────────────────────────────────
KEY_ENTER     = b'\r'
KEY_ENTER_LF  = b'\n'
KEY_BACKSPACE = b'\x08'
KEY_BACKSPACE2= b'\x7f'   # Unix backspace
KEY_HINT      = b'?'
KEY_CTRL_C    = b'\x03'


# ── TIMED INPUT ──────────────────────────────────────────────────
def get_input_with_timer(
    prompt:            str,
    start_time:        float,
    time_limit:        int,
    hud_renderer,              # callable(remaining) → None
    refresh_hz:        float = 20,
) -> tuple[str, bool]:
    """
    Read a line of input while rendering an updating HUD.

    Returns
    -------
    (input_str, timed_out)
        timed_out is True when the clock hits zero.
    """
    input_str = ""
    interval  = 1.0 / refresh_hz

    sys.stdout.write("\033[?25l")   # hide cursor
    sys.stdout.flush()

    try:
        while True:
            elapsed   = time.time() - start_time
            remaining = max(0, int(time_limit - elapsed))

            if remaining <= 0:
                return input_str, True

            # Render HUD + current input
            hud_renderer(remaining, input_str, prompt)

            # Poll for key within one refresh interval
            deadline = time.time() + interval
            while time.time() < deadline:
                if _kbhit():
                    ch = _getch()

                    if ch in (KEY_CTRL_C,):
                        raise KeyboardInterrupt

                    elif ch in (KEY_ENTER, KEY_ENTER_LF):
                        return input_str, False

                    elif ch in (KEY_BACKSPACE, KEY_BACKSPACE2):
                        input_str = input_str[:-1]

                    elif ch == KEY_HINT:
                        return "?", False

                    else:
                        try:
                            char = ch.decode("utf-8")
                            if char.isalpha():          # letters only
                                input_str += char.lower()
                        except UnicodeDecodeError:
                            pass
                    break   # re-render after any keypress
                time.sleep(0.01)

    finally:
        sys.stdout.write("\033[?25h")   # restore cursor
        sys.stdout.flush()

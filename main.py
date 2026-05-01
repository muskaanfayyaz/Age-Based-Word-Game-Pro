# main.py — Word Game Pro  |  Entry point

import os
import sys
import traceback

from engine import GameEngine

DEBUG = os.getenv("DEBUG", "0") == "1"

if __name__ == "__main__":
    try:
        GameEngine().start()
    except KeyboardInterrupt:
        print("\n\n  👋  Game exited. See you next time!\n")
        sys.exit(0)
    except Exception as exc:
        if DEBUG:
            traceback.print_exc()
        else:
            print(f"\n  ⚠️   Unexpected error: {exc}")
            print("  Run with  DEBUG=1 python main.py  for a full traceback.\n")
        sys.exit(1)
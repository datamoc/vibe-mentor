#!/usr/bin/env python3
"""Size guardrail (Mentor mode): run before adding code to a file.

Usage: python check_file.py src/app.ts [other.py ...] [--adding 80] [--root .]
Exit code: 0 = OK, 1 = warning (>= warn_lines), 2 = blocked (> max_lines).
"""
import argparse
import sys
from pathlib import Path

from common import active_lines, language_of, load_config, read_lines


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--adding", type=int, default=0,
                    help="lines of code about to be added")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    cfg = load_config(Path(args.root).resolve())
    worst = 0
    for name in args.files:
        path = Path(name)
        lang = language_of(path)
        if not path.exists():
            print(f"NEW      {name} (0 lines)")
            current = 0
        elif lang is None:
            print(f"IGNORED  {name} (not a code file)")
            continue
        else:
            current = len(active_lines(read_lines(path), lang))
        projected = current + args.adding
        if projected > cfg["max_lines"]:
            status, code = "BLOCKED", 2
        elif projected >= cfg["warn_lines"]:
            status, code = "WARNING", 1
        else:
            status, code = "OK", 0
        worst = max(worst, code)
        print(f"{status:8} {name}: {current} active lines"
              + (f" -> {projected} after adding" if args.adding else ""))
    return worst


if __name__ == "__main__":
    sys.exit(main())

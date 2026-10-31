#!/usr/bin/env python3
"""Check whether the installed vibe-mentor skill triggers on the right requests.

Usage:
    python tools/trigger_eval.py                      # tests/trigger-evals.json, 2 runs per query
    python tools/trigger_eval.py --runs 3 --workers 4

For each query it starts a headless `claude -p` and stops as soon as Claude has chosen
its first tool: the query counts as "triggered" if that tool is the Skill tool called
with 'vibe-mentor'. It tests the skill INSTALLED in ~/.claude/skills, so install the
version you want to test first. Works on Windows (no select on pipes), standard library only.
Each run is a real model call: keep --runs low.
"""
import argparse
import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EVALS = ROOT / "tests" / "trigger-evals.json"
SKILL_NAME = "vibe-mentor"


def triggered_once(query: str, timeout: int) -> bool:
    exe = shutil.which("claude")
    if not exe:
        sys.exit("The 'claude' command was not found in PATH.")
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}  # allow nesting
    cmd = [exe, "-p", query, "--output-format", "stream-json", "--verbose", "--max-turns", "1"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env, cwd=ROOT)
    lines: "queue.Queue[bytes | None]" = queue.Queue()

    def reader():
        for raw in proc.stdout:
            lines.put(raw)
        lines.put(None)

    threading.Thread(target=reader, daemon=True).start()
    deadline = time.time() + timeout
    try:
        while time.time() < deadline:
            try:
                raw = lines.get(timeout=1)
            except queue.Empty:
                continue
            if raw is None:
                return False
            try:
                event = json.loads(raw.decode("utf-8", errors="replace"))
            except json.JSONDecodeError:
                continue
            if event.get("type") == "assistant":
                for item in event.get("message", {}).get("content", []):
                    if item.get("type") == "tool_use":  # first tool decides
                        return item.get("name") == "Skill" and SKILL_NAME in str(item.get("input", {}).get("skill", ""))
            elif event.get("type") == "result":
                return False
        return False
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--evals", type=Path, default=DEFAULT_EVALS)
    parser.add_argument("--runs", type=int, default=2, help="runs per query")
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=90, help="seconds per run")
    args = parser.parse_args()

    cases = json.loads(args.evals.read_text(encoding="utf-8"))
    jobs = [(i, c["query"]) for i, c in enumerate(cases) for _ in range(args.runs)]
    with ThreadPoolExecutor(args.workers) as pool:
        outcomes = list(pool.map(lambda j: (j[0], triggered_once(j[1], args.timeout)), jobs))

    failed = 0
    for i, case in enumerate(cases):
        hits = sum(1 for idx, ok in outcomes if idx == i and ok)
        rate = hits / args.runs
        passed = rate >= 0.5 if case["should_trigger"] else rate < 0.5
        failed += not passed
        print(f"{'PASS' if passed else 'FAIL'} {hits}/{args.runs} expected={case['should_trigger']} | {case['query'][:70]}")
    print(f"\n{len(cases) - failed}/{len(cases)} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()

#!/usr/bin/env python3
"""Deterministic repository audit (Audit mode): /100 score, top-5 priorities.

Usage: python audit.py [repo-path] [--json] [--out AUDIT.md]
Thresholds and stack: optional .vibe-mentor.json file at the repository root.
"""
import argparse
import json
import sys
from pathlib import Path

from common import load_config
from metrics import collect


def score_and_priorities(m: dict, cfg: dict):
    """Return (score, [(weight, text)]): the weight drives both the score and the ranking."""
    items = []
    g, s, d, st = m["git"], m["size"], m["dup"], m["stack"]
    if not g["is_repo"]:
        items.append((20, "No Git repository: `git init`, first commit, then connect to the official forge."))
    else:
        if not g["official_remote"]:
            items.append((10, "No remote on the official forge (GitHub/GitLab): the code is neither backed up nor shared."))
        if g["giant_commits"]:
            items.append((min(10, 2 * len(g["giant_commits"])),
                          f"{len(g['giant_commits'])} giant commit(s), e.g. {g['giant_commits'][0]}: commit in small steps."))
        if g["mass_edit_commits"]:
            items.append((min(10, 3 * len(g["mass_edit_commits"])),
                          f"Mass data edit without a script, e.g. {g['mass_edit_commits'][0]}: write a replayable Python script."))
    if s["over"]:
        name, n = s["over"][0]
        items.append((min(25, 5 * len(s["over"])),
                      f"{len(s['over'])} file(s) above {cfg['max_lines']} lines, the worst being `{name}` ({n}): split into modules."))
    if s["warn"]:
        items.append((min(5, len(s["warn"])), f"{len(s['warn'])} file(s) between {cfg['warn_lines']} and {cfg['max_lines']} lines: plan the split."))
    if d["rate"] >= 0.03:
        pair = d["top_pairs"][0] if d["top_pairs"] else None
        hint = f", e.g. `{pair[0]}` and `{pair[1]}`" if pair else ""
        items.append((min(20, round(d["rate"] * 100)), f"{d['rate']:.0%} duplicated code{hint}: factor it out."))
    if m["struct"]["blocks"]:
        name, copies, lines = m["struct"]["blocks"][0]
        items.append((min(15, copies), f"`{name}` contains about {copies} copies of the same block where only the names change ({lines} lines involved): one generic version would do."))
    if st["out_of_stack"]:
        langs = ", ".join(f"{k} ({len(v)})" for k, v in st["out_of_stack"].items())
        items.append((min(15, 3 * sum(len(v) for v in st["out_of_stack"].values())), f"Languages outside the stack: {langs}."))
    if st["long_shell"]:
        name, n = st["long_shell"][0]
        items.append((min(10, 3 * len(st["long_shell"])), f"Complex shell script `{name}` ({n} lines): rewrite in Python."))
    score = max(0, 100 - sum(w for w, _ in items))
    return score, sorted(items, key=lambda x: -x[0])


def render_markdown(root: Path, m: dict, score: int, items: list) -> str:
    g, s, d, st = m["git"], m["size"], m["dup"], m["stack"]
    out = [f"# Code health audit: `{root.name}`", "", f"**Overall score: {score}/100**", ""]
    out.append("## Top 5 refactoring priorities")
    out += [f"{i}. {text}" for i, (_, text) in enumerate(items[:5], 1)] or ["Nothing to report."]
    out += ["", "## Indicator detail", ""]
    if g["is_repo"]:
        out.append(f"- **Git**: branch `{g['branch']}`, {g['commits']} commits, official remote: {'yes' if g['official_remote'] else 'NO'}")
    else:
        out.append("- **Git**: no repository")
    out.append(f"- **Size**: {len(s['over'])} file(s) over the limit, {len(s['warn'])} in the warning zone")
    out += [f"  - `{n}`: {c} lines" for n, c in s["over"][:10]]
    out.append(f"- **Duplication**: {d['rate']:.1%} of active lines")
    out += [f"  - `{a}` ↔ `{b}` ({n} shared blocks)" for a, b, n in d["top_pairs"]]
    out.append("- **Structural copies** (same shape, different names)")
    out += [f"  - `{n}`: ~{c} copies, {l} lines involved" for n, c, l in m["struct"]["blocks"]] or ["  - none"]
    out.append(f"- **Languages**: {st['by_lang'] or 'no code detected'}")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--json", action="store_true", help="raw JSON output")
    ap.add_argument("--out", help="write the Markdown report to this file")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    root = Path(args.root).resolve()
    cfg = load_config(root)
    metrics = collect(root, cfg)
    score, items = score_and_priorities(metrics, cfg)
    if args.json:
        print(json.dumps({"score": score, "priorities": [t for _, t in items], "metrics": metrics},
                         indent=2, ensure_ascii=False))
        return 0
    report = render_markdown(root, metrics, score, items)
    if args.out:
        Path(args.out).write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())

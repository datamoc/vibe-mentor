"""Audit metric collection: Git, size, duplicates, stack."""
import hashlib
import re
from collections import defaultdict
from pathlib import Path

from common import (CODE_EXT, DATA_EXT, active_lines, language_of, list_files,
                    read_lines, run_git)


def git_metrics(root: Path, cfg: dict) -> dict:
    inside = run_git(root, "rev-parse", "--is-inside-work-tree")
    if inside is None:
        return {"is_repo": False}
    remotes = run_git(root, "remote", "-v") or ""
    urls = sorted({line.split()[1] for line in remotes.splitlines() if line.strip()})
    official = [u for u in urls if any(h in u for h in cfg["forge_hosts"])]
    branch = (run_git(root, "rev-parse", "--abbrev-ref", "HEAD") or "").strip()

    giant, mass_edits, commits = [], [], 0
    stat = run_git(root, "log", "--shortstat", "--pretty=format:@@%h %s") or ""
    for block in stat.split("@@")[1:]:
        commits += 1
        head, *rest = block.strip().splitlines()
        nums = [int(n) for n in re.findall(r"(\d+) (?:insertion|deletion)", " ".join(rest))]
        if sum(nums) > cfg["giant_commit_lines"]:
            giant.append(f"{head} ({sum(nums)} lines)")

    names = run_git(root, "log", "--name-only", "--pretty=format:@@%h %s") or ""
    for block in names.split("@@")[1:]:
        head, *files = [x for x in block.strip().splitlines() if x.strip()]
        data = [f for f in files if Path(f).suffix.lower() in DATA_EXT]
        has_code = any(Path(f).suffix.lower() in CODE_EXT for f in files)
        if len(data) > cfg["mass_edit_files"] and not has_code:
            mass_edits.append(f"{head} ({len(data)} data files)")
    return {"is_repo": True, "remotes": urls, "official_remote": bool(official),
            "branch": branch, "commits": commits, "giant_commits": giant,
            "mass_edit_commits": mass_edits}


def size_metrics(files: list[Path], root: Path, cfg: dict) -> dict:
    over, warn = [], []
    for path in files:
        lang = language_of(path)
        if lang is None:
            continue
        n = len(active_lines(read_lines(path), lang))
        rel = path.relative_to(root).as_posix()
        if n > cfg["max_lines"]:
            over.append((rel, n))
        elif n >= cfg["warn_lines"]:
            warn.append((rel, n))
    return {"over": sorted(over, key=lambda x: -x[1]), "warn": sorted(warn, key=lambda x: -x[1])}


def duplication_metrics(files: list[Path], root: Path, cfg: dict) -> dict:
    """Duplicates = runs of dup_window identical active lines in several places."""
    window = cfg["dup_window"]
    seen = defaultdict(list)          # window hash -> [(file, start index)]
    per_file = {}
    for path in files:
        lang = language_of(path)
        if lang is None:
            continue
        lines = [" ".join(x.split()) for x in active_lines(read_lines(path), lang)]
        lines = [x for x in lines if len(x) > 3]          # skip "}", "end", etc.
        rel = path.relative_to(root).as_posix()
        per_file[rel] = len(lines)
        for i in range(len(lines) - window + 1):
            digest = hashlib.md5("\n".join(lines[i:i + window]).encode()).hexdigest()
            seen[digest].append((rel, i))

    covered = defaultdict(set)
    pairs = defaultdict(int)
    for places in seen.values():
        if len(places) < 2:
            continue
        for rel, i in places:
            covered[rel].update(range(i, i + window))
        distinct = sorted({p[0] for p in places})
        for a in distinct:
            for b in distinct:
                if a < b:
                    pairs[(a, b)] += 1
    total = sum(per_file.values()) or 1
    dup = sum(len(v) for v in covered.values())
    top = sorted(pairs.items(), key=lambda kv: -kv[1])[:5]
    return {"rate": dup / total, "top_pairs": [(a, b, n) for (a, b), n in top]}


KEYWORDS = {"function", "const", "let", "var", "return", "if", "else", "for", "while", "new",
            "throw", "def", "class", "fn", "pub", "use", "in", "of", "await", "async", "try", "catch"}
_STRING = re.compile(r"\"[^\"]*\"|'[^']*'|`[^`]*`")
_WORD = re.compile(r"[A-Za-z_]\w*")


def _shape(line: str) -> str:
    """Reduce a line to its shape: strings, numbers and names become wildcards."""
    line = re.sub(r"\d+", "N", _STRING.sub("S", line))
    return _WORD.sub(lambda m: m.group(0) if m.group(0) in KEYWORDS else "I", line)


def structural_metrics(files: list[Path], root: Path, cfg: dict) -> dict:
    """Copy-pasted blocks where only the names change (invisible to exact duplicates)."""
    window, min_copies = cfg["struct_window"], cfg["struct_min_copies"]
    seen = defaultdict(list)
    shapes = {}
    for path in files:
        lang = language_of(path)
        if lang is None:
            continue
        lines = [_shape(" ".join(x.split())) for x in active_lines(read_lines(path), lang)]
        lines = [x for x in lines if len(x) > 3]
        rel = path.relative_to(root).as_posix()
        shapes[rel] = len(lines)
        for i in range(len(lines) - window + 1):
            digest = hashlib.md5("\n".join(lines[i:i + window]).encode()).hexdigest()
            seen[digest].append((rel, i))

    copies, covered = defaultdict(int), defaultdict(set)
    for places in seen.values():
        if len(places) < min_copies:
            continue
        for rel, i in places:
            copies[rel] = max(copies[rel], len(places))
            covered[rel].update(range(i, i + window))
    found = [(rel, copies[rel], len(covered[rel])) for rel in covered if len(covered[rel]) >= 3 * window]
    return {"blocks": sorted(found, key=lambda x: -x[2])[:5]}


def stack_metrics(files: list[Path], root: Path, cfg: dict) -> dict:
    allowed = {lang for langs in cfg["stack"].values() for lang in langs}
    by_lang = defaultdict(int)
    out_of_stack, long_shell = defaultdict(list), []
    for path in files:
        lang = language_of(path)
        if lang is None:
            continue
        by_lang[lang] += 1
        rel = path.relative_to(root).as_posix()
        if lang == "shell":
            n = len(active_lines(read_lines(path), lang))
            if n > cfg["max_shell_lines"]:
                long_shell.append((rel, n))
        elif lang not in allowed:
            out_of_stack[lang].append(rel)
    return {"by_lang": dict(by_lang), "out_of_stack": dict(out_of_stack), "long_shell": long_shell}


def collect(root: Path, cfg: dict) -> dict:
    files = list_files(root)
    return {"git": git_metrics(root, cfg), "size": size_metrics(files, root, cfg),
            "dup": duplication_metrics(files, root, cfg),
            "struct": structural_metrics(files, root, cfg),
            "stack": stack_metrics(files, root, cfg)}

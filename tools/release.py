#!/usr/bin/env python3
"""Build the vibe-mentor zip and publish it as a GitHub release.

Usage:
    python tools/release.py 0.1.6              # rehearsal: checks + builds a temp zip, publishes nothing
    python tools/release.py 0.1.6 --publish    # real run: tag, release, upload the zip

Safety checks before anything is published:
  - the version looks like X.Y.Z and its tag does not exist yet;
  - no tracked file has uncommitted changes, and we are on 'main';
  - 'main' is fully pushed to GitHub (the tag is created from the remote branch).
Standard library only. Requires git and the GitHub CLI (gh), already logged in.
"""
import argparse
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "vibe-mentor"
OUT_DIR = ROOT / "releases"
BRANCH = "main"
SKIP_PARTS = {"__pycache__", ".sandbox"}
SKIP_SUFFIXES = {".pyc"}
FIXED_TIME = (2020, 1, 1, 0, 0, 0)  # same input -> same zip, whatever the build date

NOTES = """Download `vibe-mentor-{version}.zip` below.

- **Claude Desktop**: Settings, then upload the zip as a skill.
- **Claude Code**: unzip it into `.claude/skills/vibe-mentor/`.

Modes: Initiation (practice exercises), Audit (repository score and priorities), Mentor (real-time guardrails).
"""


def run(*cmd):
    """Run a command (no shell), return stdout; stop with a clear message on failure."""
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"Command failed: {' '.join(cmd)}\n{result.stderr.strip()}")
    return result.stdout.strip()


def skill_files():
    files = [
        p for p in SKILL_DIR.rglob("*")
        if p.is_file() and not (SKIP_PARTS & set(p.parts)) and p.suffix not in SKIP_SUFFIXES
    ]
    return sorted(files)


def build_zip(target: Path):
    files = skill_files()
    if not (SKILL_DIR / "SKILL.md").is_file():
        sys.exit("vibe-mentor/SKILL.md not found: wrong folder?")
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            info = zipfile.ZipInfo(path.relative_to(ROOT).as_posix(), FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, path.read_bytes())
    return len(files)


def check_ready(version: str):
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        sys.exit(f"Invalid version '{version}': expected X.Y.Z (for example 0.1.6).")
    tag = f"v{version}"
    if run("git", "tag", "--list", tag):
        sys.exit(f"Tag {tag} already exists locally.")
    if run("gh", "release", "list", "--json", "tagName", "--jq", f'.[]|select(.tagName=="{tag}")'):
        sys.exit(f"Release {tag} already exists on GitHub.")
    if run("git", "branch", "--show-current") != BRANCH:
        sys.exit(f"Switch to the '{BRANCH}' branch first.")
    if run("git", "status", "--porcelain", "--untracked-files=no"):
        sys.exit("Uncommitted changes in tracked files: commit them first (the release is built from what is saved).")
    run("git", "fetch", "origin", BRANCH)
    if run("git", "rev-parse", "HEAD") != run("git", "rev-parse", f"origin/{BRANCH}"):
        sys.exit(f"'{BRANCH}' is not in sync with GitHub: push (or pull) first.")
    return tag


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("version", help="new version, X.Y.Z (no leading v)")
    parser.add_argument("--publish", action="store_true", help="really create the release (default: rehearsal)")
    args = parser.parse_args()

    tag = check_ready(args.version)
    name = f"vibe-mentor-{args.version}.zip"

    if not args.publish:
        with tempfile.TemporaryDirectory() as tmp:
            count = build_zip(Path(tmp) / name)
            size = (Path(tmp) / name).stat().st_size
        print(f"Rehearsal OK: {name} would contain {count} files ({size} bytes).")
        print(f"Tag {tag} would be created from {BRANCH} and published as the latest release.")
        print("Nothing was published. Re-run with --publish to do it.")
        return

    OUT_DIR.mkdir(exist_ok=True)
    zip_path = OUT_DIR / name
    count = build_zip(zip_path)
    print(f"Built {zip_path.relative_to(ROOT)} ({count} files).")
    url = run(
        "gh", "release", "create", tag, str(zip_path), "--target", BRANCH, "--latest",
        "--title", f"vibe-mentor {args.version}", "--notes", NOTES.format(version=args.version),
        "--generate-notes",
    )
    print(f"Release published: {url}")


if __name__ == "__main__":
    main()

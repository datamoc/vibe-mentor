"""Shared building blocks for the vibe-mentor scripts (config, files, active lines)."""
import json
import re
import subprocess
from pathlib import Path

DEFAULT_CONFIG = {
    "warn_lines": 400,         # warning: plan a split
    "max_lines": 500,          # block: refactor before adding code
    "dup_window": 6,           # consecutive identical lines = duplicate
    "struct_window": 8,        # structural duplicate: same shape, different names
    "struct_min_copies": 3,    # minimum number of copies to report it
    "max_shell_lines": 30,     # above this, a shell script should become Python
    "mass_edit_files": 5,      # above this, data processing must go through a script
    "giant_commit_lines": 500, # "giant" commit (lines added + removed)
    "forge_hosts": ["github.com", "gitlab.com", "bitbucket.org"],
    # Allowed languages per kind of need (configurable stack)
    "stack": {
        "scripts": ["python"],
        "web": ["typescript", "javascript"],
        "heavy": ["rust"],
    },
}

CODE_EXT = {
    ".py": "python", ".ts": "typescript", ".tsx": "typescript",
    ".js": "javascript", ".jsx": "javascript", ".mjs": "javascript",
    ".rs": "rust", ".sh": "shell", ".bash": "shell", ".ps1": "shell",
    ".bat": "shell", ".cmd": "shell", ".go": "go", ".java": "java",
    ".rb": "ruby", ".php": "php", ".c": "c", ".cpp": "cpp", ".cs": "csharp",
}
DATA_EXT = {".json", ".yaml", ".yml", ".csv", ".toml", ".xml"}
SKIP_DIRS = {".git", "node_modules", "target", "dist", "build", ".venv", "venv",
             "__pycache__", ".sandbox", ".next", ".remember"}
COMMENT_PREFIXES = {
    "python": ("#",), "shell": ("#", "REM ", "::"),
    "typescript": ("//", "/*", "*"), "javascript": ("//", "/*", "*"),
    "rust": ("//",),
}
IMPORT_RE = re.compile(r"^(import |from \S+ import |use |const .*= require\(|#include )")


def load_config(root: Path) -> dict:
    """Load .vibe-mentor.json (if present) on top of the defaults."""
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    path = root / ".vibe-mentor.json"
    if path.exists():
        user = json.loads(path.read_text(encoding="utf-8"))
        stack = {**cfg["stack"], **user.pop("stack", {})}
        cfg.update(user)
        cfg["stack"] = stack
    return cfg


def run_git(root: Path, *args: str):
    """Return git's output, or None if git is missing or the command fails."""
    try:
        res = subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                             text=True, encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return None
    return res.stdout if res.returncode == 0 else None


def list_files(root: Path) -> list[Path]:
    """Project files. Honours .gitignore when inside a Git repository."""
    out = run_git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    if out is not None:
        paths = [root / n for n in out.split("\0") if n]
    else:
        paths = list(root.rglob("*"))
    return [p for p in paths
            if p.is_file() and not set(p.relative_to(root).parts) & SKIP_DIRS]


def language_of(path: Path):
    return CODE_EXT.get(path.suffix.lower())


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def active_lines(lines: list[str], lang: str) -> list[str]:
    """Active code lines: no blanks, comments or imports."""
    prefixes = COMMENT_PREFIXES.get(lang, ())
    kept = []
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith(prefixes) or IMPORT_RE.match(line):
            continue
        kept.append(line)
    return kept

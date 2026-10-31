# Manual checks and fallbacks (no scripts, no Python, no Node, or plain chat)

The scripts in `scripts/` are accelerators, never requirements. Every check has a manual equivalent below. Use the lightest one that the environment allows, and say plainly which checks were run and which were done by reading.

## 1. Capability levels

| Level | Typical environment | What to do |
|---|---|---|
| **A. Shell + files + Python** | A coding agent in a terminal, or a desktop app with a code or workspace mode | Use the scripts. |
| **B. Shell + files, no Python** | Same, on a machine without Python | Use the shell commands in section 2. Suggest installing Python only if the user wants the scripts. |
| **C. Chat with a code sandbox, no access to the user's disk** | A chat assistant with code execution and file uploads | Ask for a zip of the repository (or the key files); run the scripts on the upload; give the user the commands to run locally. |
| **D. Chat with no tools at all** | Plain chat | Manual mode: section 3. |

Detect the level by what you can actually do (try a harmless command, or notice no file or shell tool is available). Do not assume.

## 2. Shell equivalents (levels A and B)

Run from the repository root.

| Check | macOS / Linux / Git Bash | PowerShell |
|---|---|---|
| Inside a Git repo? | `git rev-parse --is-inside-work-tree` | same |
| Official remote? | `git remote -v` | same |
| Biggest files (lines) | `git ls-files \| xargs wc -l \| sort -rn \| head -15` | `git ls-files \| ForEach-Object { "{0} {1}" -f (Get-Content $_ \| Measure-Object -Line).Lines, $_ } \| Sort-Object { [int]($_ -split ' ')[0] } -Descending \| Select-Object -First 15` |
| Languages in use | `git ls-files \| sed 's/.*\.//' \| sort \| uniq -c \| sort -rn` | `git ls-files \| Group-Object { [IO.Path]::GetExtension($_) } \| Sort-Object Count -Descending` |
| Giant commits | `git log --shortstat --oneline \| head -40` | `git log --shortstat --oneline \| Select-Object -First 40` |
| Does a function exist already? | `git grep -n -i "<keyword>"` | `git grep -n -i "<keyword>"` |
| Repeated blocks | `git grep -c "<distinctive line>"` per file; or read the file and look for sections that differ only by a name | same |

`wc -l` counts blanks and comments, so it over-counts active code by roughly 10-20%. Treat a file as "in the warning zone" from about 450 raw lines and "over the limit" above about 580, then confirm by reading.

## 3. Plain chat, no tools (level D)

You cannot run or read anything, so work from what the user shows you.

- **Audit**: ask the user to paste the output of the commands in section 2 (they can run them and paste the result), or to paste or upload the key file. Review what you are given and say clearly what you did *not* see.
- **Size guardrail**: estimate by eye from the pasted file; when delivering new code, keep each file small by design (one responsibility, under ~200 lines) and say so.
- **Delivering code (rule 1 in chat)**: there is no repository here, so do not refuse. Deliver the code as **separate files**, one block per file with its relative path as a heading, small modules rather than one big file. Open with what the code does and how to try it, in plain words. Only then, in a closing section, explain in one sentence what a version history (Git) is for and give the commands to put the files in a repository: create the folder, `git init`, copy the files, `git switch -c feature/<name>`, `git add`, `git commit`, and connect the remote. Keep the chat for the design and explanation, not as the place the code lives.
- **Mass edit (rule 5)**: write the script (Python by default) with a `--dry-run` mode and follow the review gate in `SKILL.md`: explain the script in plain language, ask them to run the rehearsal and paste the output, show three before/after examples from it, and get a concrete confirmation before giving the command for the real run. Do not rewrite the files in the chat.
- **Initiation katas and downloadable exercises**: offer them at the start. Workshop 1 (JSON files): give a small generator script (Python) the person can run, or ten sample files as separate blocks (ten is enough to feel the problem). Workshop 2 (long file): give the structure and ask them to paste a file of their own, or deliver a short messy file as a block. Workshop 3 (duplicates): three short files as separate blocks. With a code sandbox (level C), run `make_sandbox.py <n> --zip` and hand over the zip. Guide step by step; one idea per message.
- Everything else (rules 3 to 8, language, tone) applies unchanged.

## 4. A runtime is missing (Python, Node, Rust, Git)

The rules do not depend on a runtime being installed. If one is missing:

1. Say so in one sentence and what it blocks ("Node is not installed, so I cannot run the server; I wrote it and checked it by reading").
2. Offer the one-line install, never run an installer without being asked: Python: `winget install Python.Python.3.12` (Windows), `brew install python` (macOS), `sudo apt install python3` (Debian/Ubuntu). Node.js LTS: `winget install OpenJS.NodeJS.LTS`, `brew install node`, or nodejs.org. Git: `winget install Git.Git`, `brew install git`, `sudo apt install git`.
3. Keep following the stack rule: write the code in the right language even if it cannot be run here. Mark it **untested** and give the exact command that will test it on the user's machine.
4. Prefer checks that need no runtime: reading the code, `git` commands, and shell tools already present.
5. Never claim something was run or verified when it was not.

## 5. Reading the answer to "which language can I run?"

Ask the user to type the command and tell you exactly what appears.

| What they see | Meaning | What to do |
|---|---|---|
| `Python 3.x.y` (3.8 or newer) | Python is ready | Use Python. |
| `Python was not found; run without arguments to install from the Microsoft Store` (Windows) | Windows only has a placeholder, Python is **not** installed | Offer to install it (python.org installer, tick "Add python.exe to PATH", or `winget install Python.Python.3.12`) or use PowerShell. Do not tell them to open the Store without explaining. |
| `'python' is not recognized…` / `command not found: python` | Not installed, or only installed under another name | On Windows try `py --version`; on Mac/Linux try `python3 --version`. If those fail too, treat as not installed. |
| macOS dialog "The `python3` command requires the command line developer tools" | Python is not ready; accepting installs Apple's developer tools (large download) | Explain the download is large; offer the python.org installer or the native shell instead. Let them choose. |
| `Python 2.7.x` | Too old | Treat as not installed for our purposes. |

## 6. Native shell fallbacks for small file jobs

Use these only when Python is not available and the user prefers not to install it, for small, one-off jobs. Write them like any other script: rehearsal mode, before/after examples, backup first, review gate.

- **Windows, PowerShell** (always present). Start the script with `[CmdletBinding(SupportsShouldProcess)]` and wrap each change in `if ($PSCmdlet.ShouldProcess($file, 'update')) { ... }`: running it with `-WhatIf` then shows what would change without changing anything. Print before/after lines yourself so the rehearsal shows examples. If PowerShell refuses to run a saved script ("running scripts is disabled"), explain that this is a safety setting, and after the user has read the script, run it for this one time with `powershell -ExecutionPolicy Bypass -File .\script.ps1 -WhatIf`. Do not ask them to turn the protection off for good.
- **macOS / Linux, shell (zsh or bash)**. Add a `DRY_RUN=1` environment variable or a `--dry-run` argument that only prints the planned changes; use `sed`/`awk` carefully (macOS `sed -i` needs an empty suffix argument: `sed -i ''`), and keep a backup copy first.
- Keep it short. If the logic becomes more than about 40 lines or needs real parsing, go back to installing Python: a long shell script is harder to review than a Python one.

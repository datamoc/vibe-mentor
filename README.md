# vibe-mentor

**Stop the code your AI writes from turning into a mess.**

AI assistants write code fast. Left alone, they also leave behind 2,000-line files, the same function pasted five times, secrets committed by accident, and fifty files "fixed" by hand with no trace of what changed.

vibe-mentor is an [Agent Skill](https://agentskills.io/specification), so it works with any AI agent that supports the format. It plays a demanding but kind lead developer. It does not just say no: it explains *why* each habit matters, then helps you adopt it. It is made for people who build with AI without being developers, and it is useful to developers too.

## What you get

- **Learn.** Three throwaway exercises (fix many files, split a giant file, remove duplicates) that let you feel the difference between a good and a bad way to work with AI. Nothing can break.
- **Check.** An audit of any project: a score out of 100, the five things to fix first in plain language, and a ready-to-file issue plan.
- **Build safely.** Before your agent hands you code, it checks the basics and fixes what is missing.

## The habits it enforces

- Code lives in a Git repository connected to your forge, not in the chat.
- Files stay small: a warning at 400 lines, a stop at 500.
- More than five files to change? A replayable script does it, after a rehearsal you review. The AI never edits them by hand.
- A proven library beats home-made code. For passwords, tokens, encryption and escaping, always.
- Inputs are validated, outputs are escaped, secrets stay out of the repository.
- Every page is translated into French, English and Arabic, with a mirrored layout for Arabic.

## Try it

Ask your agent any of these once the skill is installed:

- "Audit my project and tell me where to start."
- "I'm a beginner, I want to learn good habits for building with AI."
- "Fix the formatting of these 60 JSON files." (it will push back, kindly, and write a script instead)

## Install

1. Download `vibe-mentor-X.Y.Z.zip` from the [latest release](https://github.com/datamoc/vibe-mentor/releases/latest).
2. **If your agent has a skills screen**: upload the zip there and switch the skill on.
3. **If it reads skills from a folder**: unzip the zip so that the `vibe-mentor/` folder sits in your agent's skills directory (check its documentation for the exact location).
4. Check it works: ask your agent "audit my project".

The skill itself lives in [`vibe-mentor/`](vibe-mentor/). Python 3 and Git are optional: every check has a manual equivalent.

## License

GPL-3.0-or-later. The full text is in [`LICENSE`](LICENSE), and it is also bundled in every release zip.

## Releasing

`python tools/release.py X.Y.Z` rehearses a release; add `--publish` to build the zip and publish it on GitHub.

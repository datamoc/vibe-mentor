# Audit indicators: what `audit.py` measures and its limits

The score starts at 100 and loses points for each problem found. The script measures; interpretation is still yours: read the limits below before commenting on a result.

| Indicator | Measure | Max penalty | Known limits |
|---|---|---|---|
| Git repository | `git rev-parse` | 20 | A folder without Git is a problem even for a small script. |
| Official remote | URL containing a host from `forge_hosts` | 10 | An internal forge (e.g. gitlab.company.com) must be added in `.vibe-mentor.json`. |
| Giant commits | more than `giant_commit_lines` lines added + removed | 10 | An initial import or generated files are legitimately big. |
| Mass data edits | a commit touching more than `mass_edit_files` data files with no code | 10 | May flag a legitimate data import. Check with the person. |
| Oversized files | active lines > `max_lines` | 25 | Counts active code (no blanks, comments, imports). Generated data files are not code files. |
| Files in warning zone | between `warn_lines` and `max_lines` | 5 | An anticipation indicator, not a fault. |
| Duplication | share of active lines in blocks of `dup_window` identical lines found in several places | 20 | Catches exact copy-paste (whitespace normalised), not functions rewritten differently. Repetitive tests produce false positives. |
| Structural copies | blocks of `struct_window` lines of the same shape (names, strings, numbers ignored) present at least `struct_min_copies` times | 15 | Catches copy-paste where only the names change. May flag legitimately repetitive code (declarations, routes). The copy count is a per-file maximum. |
| Languages outside the stack | code extensions outside the union of the `stack` languages | 15 | Based on the extension, not the real role of the file. |
| Complex shell | shell script > `max_shell_lines` active lines | 10 | Small shell wrappers are tolerated. |

## What the script does not see

- Semantic duplicates (same behaviour, code rewritten differently): reread functions with similar names.
- Naming quality, readability, absence of tests.
- Manual repeated tasks outside the Git history.
- Security, error handling, dead code, unvalidated inputs and hard-coded user-facing text: look for them by hand in the central file (see step 4 of Audit mode).

## Action plan as issues

For each of the top-5 priorities, write an issue:

- **Title**: action verb + target ("Split `server.js` into modules").
- **Context**: the audit's numbers and the risk.
- **Steps**: 3 to 6 concrete steps, each small enough for one commit.
- **Done**: a verifiable criterion (e.g. "`check_file.py` no longer reports a block").

Present the plan to the user and create the issues only after their agreement. Write the issues in the language the team uses.

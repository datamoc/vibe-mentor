# Workshop walkthrough (Initiation mode)

All workshops happen in `.sandbox/<workshop>/`, a local Git repository created by `scripts/make_sandbox.py`. Nothing reaches production code. No push to the forge in these exercises.

**Before each workshop**: say in two plain sentences what the person will practise and why it is safe (a throwaway folder). Offer the files as a download (`make_sandbox.py <n> --zip`, or the sample files directly in a chat, see `references/manual-checks.md`) and let them choose to follow along. Do not mention Git until the step that needs it, and then define it in one sentence. Tell them to unzip the exercise anywhere they like, then open the terminal **from that folder** (see `references/command-line-basics.md`, section 4); never give a command with a guessed path such as `$HOME\Desktop\...`.

Teaching principle: let the person try their natural method first, then show why a better method exists. Do not give the answer before they have run into the problem. Run the workshop in the person's language.

## Workshop 0 (optional): your first commands

For someone who has never opened a terminal. Follow `references/command-line-basics.md`: open the window, run a harmless command, read the result together, move into the practice folder. Two minutes, one visible win. Then continue with Workshop 1.

## Workshop 1: AI vs Script

`python scripts/make_sandbox.py 1` creates 50 files in `configs/`: varying indentation, minified JSON, and trailing commas (so invalid JSON).

1. **Setting the scene.** "Here are 50 messy configuration files. How would you like to clean them up?" Wait for the answer.
2. **Interception.** If the answer is "fix them one by one with the AI": explain in three points: risk of silent error (a missing comma, a changed value), cost (50 round trips, thousands of tokens), non-reproducibility (tomorrow, a 51st file: start over).
3. **Building.** Guide the writing of `fix_configs.py`: read each file, remove trailing commas, rewrite with 2-space indentation. Require a `--dry-run` mode that lists what would change. Prefer a library over a hand-written parser where one exists (rule 6).
4. **Run and proof.** Follow the review gate from `SKILL.md`: explain the script in plain words, let the person read it, run `--dry-run` and show three before/after examples, ask them to confirm those examples look right, and only then run it for real (after a backup or saved version). Verify: `python -m json.tool` on each file, or a small counter of valid files before/after (0 of 12 invalid → 50 of 50).
5. **Git.** A branch `fix/normalize-configs`, a commit of the script, a commit of the result. `git log` to see it.

**Done when**: the script is committed, replayable, and all 50 files are valid.

## Workshop 2: The Split and the Stack

`python scripts/make_sandbox.py 2` creates `server.js`: more than 500 lines mixing data access, business validation and HTML rendering.

1. **Measure.** `python scripts/check_file.py server.js`: see the block. Have the person say why it is a problem (where is the order validation function? how long to find it?).
2. **Split plan.** Separate by responsibility, following the web stack (Node.js / TypeScript): `data/` (load/save), `domain/` (validate/compute), `views/` (render), `routes.js` (handlers), `server.js` (startup). Validate the plan before moving anything.
3. **Moving in steps.** One module at a time, one commit per module, check the server still starts. Existing code does not change behaviour: move, do not rewrite. If Node.js is not installed, do not block the workshop: check the move by reading (every function still exported and imported, no file over the limit with `check_file.py` or `wc -l`) and note that the run check is left for a machine with Node.
4. **Demonstration.** Ask for the same small change (e.g. "reject a price with more than 2 decimals") on the old monolith (via an old commit) and on the split version. Compare the amount of context needed and the precision of the change.

**Done when**: no file is above 400 lines, `audit.py` no longer flags an oversized file, and the person can say where a new function belongs.

## Workshop 3: Duplicate hunting and the Git workflow

`python scripts/make_sandbox.py 3` creates three files in `src/`, each with its own copy of the same price formatting (`formatPrice`, `euroString`, `toEuros`).

1. **Setting the scene.** Ask the person to add price display in a new file `src/quote.js`. Watch whether they search before writing.
2. **Search reflex.** Show `grep -rn "toFixed" src/` then `grep -rn "€" src/`: the function exists three times. Explain: without a search, the AI creates a fourth, and fixing a bug means fixing it everywhere.
3. **Library before home-made code.** Before factoring, ask: "Is there already a library that formats amounts?" (in Node: `Intl.NumberFormat`, built into the language, which replaces the three home-made versions and also handles French, English and Arabic formats). Link it to rule 6: for anything security-related (passwords, tokens, HTML escaping) we never write our own version.
4. **Factoring.** Create `src/format.js` with a single `formatCurrency` function, replace the three usages, delete the old versions. Run `audit.py` to watch the duplication rate drop.
5. **Git workflow.** All of this on a branch `refactor/format-currency`. One commit per step (create the shared module, replace file by file, then delete).

**Done when**: a single formatting function remains, search-before-create has become a stated reflex, and the work is on its own branch.

## Closing the path

Summarise in a few lines what was covered and offer an audit (Audit mode) of one of the person's real projects. The three reflexes to remember: script rather than chat for repetitive work, small files, search before creating.

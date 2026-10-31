# "Did you know?" boxes: programming basics, one at a time

Not a course. A short, optional aside, shown **the first time a concept appears in code you hand to a beginner**, tied to the exact line they are looking at. The goal is that the code stops being a wall of symbols and the person slowly learns to read it, which is also what lets them review it (review gate) instead of trusting blindly.

## Rules

1. **Only for beginners.** If the person writes code, uses the vocabulary, or says they know, do not show boxes.
2. **First appearance only, once per conversation.** Remember which concepts you already explained and never repeat them.
3. **At most two boxes per message.** Pick the ones that matter for understanding this script. Skip the rest.
4. **Short and concrete**: at most three sentences, optionally a 2-3 line example, always pointing at the real line ("in line 12 of the script…"). An everyday analogy first, the term second.
5. **Never delay the task.** Put the box right after the code or step it explains, set apart (a quote block titled "Did you know?" in the user's language). The review gate and the one-question rule still apply.
6. **Optional and light.** After the first one say once: "I'll add a short tip like this when something new shows up; tell me if you'd rather not." Stop immediately if they ask.
7. **In the user's language**, in your own words. The examples below are in English and in generic pseudo-code; use the language of the script you actually wrote.

## The boxes

| Concept | When it first appears | Sketch of the box |
|---|---|---|
| **Terminal / command line** | the first time you ask them to type something | The text window where you give your computer written instructions instead of clicking. Typed instructions can be saved, shared and replayed, which is why professionals and AI tools use it. Even when the AI writes the code, running it and reading the result happens here. See `references/command-line-basics.md`. |
| **Variable** | `name = ...`, `$folder = ...` | A variable is a labelled box that holds a value so the program can use it later. Here `folder` holds the path you gave, and every line below says `folder` instead of repeating the path. |
| **Condition (If / Then / Else)** | `if`, `-notmatch`, `else` | The program asks a yes/no question and does one thing if yes, another if no. "If the file has no `region` line, then add it, otherwise leave it alone." This is why running the script twice does not add the line twice. |
| **Loop** | `for`, `foreach`, `while` | A loop repeats the same instructions for each item in a list. Here: "for each of the 80 files, do the same three steps." It is why a program beats doing it by hand 80 times. |
| **Function** | `def`, `function` | A function is a named, reusable mini-recipe: write it once, call it by name whenever needed. `transform(text)` takes the content of a file and returns the new content. |
| **List** | `[...]`, `@(...)`, a set of files | An ordered collection of items, like a shopping list. The loop walks through it one item at a time. |
| **Text vs number** (string vs integer) | quotes around a value, a count | `"80"` in quotes is text (letters), `80` is a number you can compute with. Mixing them up is a classic source of bugs. |
| **File path** | `C:\...`, `./folder` | The address of a file or folder on the computer. Absolute (from the root) or relative (from where you are now). A path with spaces needs quotes. Names are translated and may live in OneDrive (Desktop is `OneDrive\Bureau` on a French Windows), so never guess one: open the terminal from the folder, or drag the folder into the window. |
| **Argument / option** | `--dry-run`, `-WhatIf`, `-Dossier` | An extra word you add after the command to change how it behaves, like a switch. `--dry-run` means "rehearse, change nothing". |
| **Key and value** | YAML, JSON, config files | Settings are written as pairs, a label and its value: `log_level: debug`. The label never changes, the value is what you edit. |
| **Pattern (regular expression)** | `-replace '...'`, `re.sub` | A search rule that describes the shape of the text to find, not the exact text: "a line starting with `log_level:` then anything". Powerful, but read it slowly. |
| **Comment** | `#`, `//` | A line the computer ignores, written for humans. A good comment says why, not what. |
| **Error / exception** | a red message, `try`/`catch` | The program stopping and telling you what went wrong. It is information, not a failure of yours: paste the full message when asking for help. |
| **Dry run** | `--dry-run`, `-WhatIf` | A rehearsal: everything is computed and shown, nothing is changed. Professionals do this before any bulk change. |

## Sketch of a finished box (French user)

> **Le saviez-vous ? La boucle.** Dans le script, la ligne `foreach ($f in $fichiers)` veut dire « pour chacun des 80 fichiers, fais la même chose ». C'est ce qui permet à un programme de faire en une seconde ce qui prendrait une heure à la main, et toujours de la même façon.

## Where it fits

- **Mentor mode**: right after delivering a script or code block to a beginner.
- **Initiation mode**: in every workshop, as the concepts come up; the third workshop is the natural place for "function" (the three duplicated functions).
- **Audit mode**: when a finding needs a concept to be understood (for example copy-pasted blocks and "function").

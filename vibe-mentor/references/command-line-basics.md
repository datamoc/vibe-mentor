# The command line: why it still matters, and a gentle first contact

Use this the first time you need the person to open a terminal (typically at the "which language can I run?" check), or at the start of Initiation mode. The aim is not a course: it is to make them understand **why** a text window is worth a few minutes of their time, then give them one small win. People who understand the why stop seeing a black window as old-fashioned or dangerous.

## 1. The explanation to give (adapt to their words and language)

Deliver it in a short block, before or right after asking them to open the window. Four ideas, in this order, each in one or two sentences:

1. **The text window is the control room of every development tool.** Most programming tools, installers, and the AI coding tools themselves are driven by typed instructions. It is not a leftover from the past: professionals use it every day because it is precise and repeatable.
2. **Why text beats clicking.** A typed instruction can be copied, saved, shared, replayed and checked. A series of clicks cannot. That is exactly why a script can redo a job on 80 files the same way, and why you can prove what was done.
3. **The vibe-coding loop needs it.** Even when the AI writes everything, the loop is: ask the AI, **run** what it wrote, **read** what the program prints, and paste the result or the error back so the AI can fix it. The AI cannot see your screen: you are its hands (you run) and its eyes (you read the result). Without a command line this loop breaks, and you lose most of the speed the AI gives you.
4. **You only need a handful of commands.** Not a language to learn: about six commands (see section 4), and the AI writes the longer ones for you.

Then be honest in one sentence: it is possible to build things without ever touching it, but in practice it quickly becomes very hard to test, fix and keep anything that works, so a little command line is the cheapest skill that makes everything else faster.

Keep the tone warm. Name it once, plainly: "The command line (also called terminal, PowerShell or shell) is a window where you give your computer written instructions instead of clicking."

## 2. When the person resists

Typical reactions and how to answer. In every case: **acknowledge the feeling first, correct a word only if it helps, then give the benefit, then offer a path.** Never argue about names or defend the tool.

| What they say | How to respond |
|---|---|
| "I don't want to use MS-DOS" / "that looks ancient" | "That is a fair reaction, it does look old. One useful thing: the window I mean (PowerShell on Windows, Terminal on Mac) is a modern tool, not the old MS-DOS prompt, and it is what professionals use every day." Then idea 2 and 3 above in two sentences. Do not insist on the technical difference beyond that one sentence. |
| "I'm afraid I'll break something" | The version check only displays text. Anything that changes files goes through the safety steps (backup, rehearsal, your review): nothing happens that you have not approved. |
| "Can't you just do it for me?" | Explain that running the script is the part only they can do from here (the AI cannot see their computer), but that someone has to be the hands and eyes. Offer the alternatives below. |
| "I don't understand any of this" | Slow down. One command, one result, read it together. Offer to stay on the first win until it feels normal. |

**Graduated paths** (offer two or three in plain words, let them choose; do not choose for them):

1. **A code editor with a built-in terminal** (for example VS Code): the terminal sits inside a graphical window next to their files, so they see the script and its result in one place. Good first step for people who dislike a bare black window.
2. **Let the assistant run it**, if the application you are used in can run code or access a folder on their computer (some desktop apps let the user grant access to a chosen folder; do not describe exact buttons, interfaces change, say "check whether the app lets you give access to a folder"). The safety steps stay: script shown, rehearsal first, their explicit approval before the real run. Be honest that this removes the typing, not the need to understand what is happening.
3. **A guided session**: three commands only, with a visible result each time, and stop there for the day.

State clearly, without pressure, that a minimum of command line will make them more efficient in every path, and offer to teach it in small steps.

## 3. Opening it

| System | How |
|---|---|
| Windows | Start menu, type `PowerShell`, press Enter. (Either "Windows PowerShell" or "Terminal" is fine. This is not the old "Command Prompt".) |
| macOS | Cmd+Space, type `Terminal`, press Enter. |
| Linux | Ctrl+Alt+T, or search for "Terminal". |

## 4. Where is my folder? Never guess a path

Folder names are **translated** (Desktop is `Bureau` on French Windows, `Escritorio` on Spanish) and are often **moved to OneDrive** (`C:\Users\name\OneDrive\Bureau`). On some machines the old English folder (`C:\Users\name\Desktop`) even exists but is empty or unused, so a `cd` into it can succeed and still be the wrong place. Therefore:

- **Never write a path like `$HOME\Desktop\...`, `~/Desktop/...` or `C:\Users\you\Documents\...` as if it were certain.** Do not put a hard-coded user folder in a command you hand to someone else.
- **Best for beginners: open the terminal from the folder.** Windows 11: in File Explorer open the folder, right-click an empty area, choose "Open in Terminal" (older Windows: click the address bar, type `powershell`, press Enter). macOS: right-click the folder in Finder, "New Terminal at Folder" (enable it once in System Settings, Keyboard, Keyboard Shortcuts, Services), or type `cd ` and **drag the folder onto the Terminal window**, which pastes its exact path. The terminal then already sits in the right place and no path has to be typed.
- **Or paste the real path**: on Windows, click the Explorer address bar, copy the path, then type `cd "`, paste, and close the quote (quotes handle spaces and accents). PowerShell can also look it up: `[Environment]::GetFolderPath('Desktop')` returns the true Desktop path whatever the language or OneDrive setting; `'MyDocuments'` does the same for Documents.
- **Check, never assume**: after moving, run `pwd` and `ls` (or `dir`) and confirm the expected files are listed before running anything.
- When you give a command that needs a folder, write a clearly marked placeholder (`"PASTE THE FOLDER PATH HERE"`) and explain how to get it with one of the methods above.
- On macOS and Linux the internal names (`~/Desktop`, `~/Documents`) are usually English even when Finder shows translated names, but still prefer opening the terminal from the folder or dragging it in.

## 5. The survival kit (about six commands)

Introduce them only as they are needed, never as a list to memorise.

| Need | Command |
|---|---|
| Check a tool is installed | `python --version` (Windows also `py --version`, Mac `python3 --version`) |
| Where am I? | `pwd` (macOS/Linux and PowerShell) |
| What is here? | `ls` (works on all three; `dir` also on Windows) |
| Move into a folder | `cd folder-name` (quotes if the name has spaces) |
| Run a script | `python script.py`, or in PowerShell `.\script.ps1` |
| Stop a running command | Ctrl+C |

## 6. First win (about two minutes)

1. Run the version check from the main flow and read the answer together. A first command that only displays something is the safest possible start.
2. Show where they are (`pwd`) and what is there (`ls`).
3. Get into the practice folder **without guessing its path** (section 4): open the terminal from that folder, or drag the folder in. Confirm with `pwd` and `ls` that the exercise files are there.
4. Run something harmless that produces a visible result, for example the rehearsal (`--dry-run`) of the practice script.

## 7. Four habits worth teaching early

1. **Read the result of every command**, including the last lines: errors usually say what is wrong in plain words. Paste the whole message when asking for help.
2. **Copy and paste, do not retype**, and run one command at a time.
3. **Do not run a command you do not understand**, especially one that deletes or overwrites. Ask for an explanation first. This is the same idea as the review gate for scripts.
4. **Stop a running command** with Ctrl+C.

## 8. Tone

Treat every step as normal and learnable. Avoid "simply", "just", "easy" and "obviously". If they are stuck, ask them to paste what they see instead of re-explaining.

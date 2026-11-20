# Doc-factory kit: setup for team members

The doc-factory kit helps Claude Code write and check ELITEA user documentation with the house style, and with the code as the source of truth. This page explains how to set it up on your machine.

## What You Need

- Git, and these four repos cloned **as siblings** in one parent folder:

  ```
  <parent>/
    elitea.github.io/
    EliteaUI/
    elitea-sdk/
    elitea_core/
  ```

  If your code repos are somewhere else, see [Set Your Repo Paths](#set-your-repo-paths).
- Python 3.10 or later, available as `python`. On Windows, install it from python.org or with `winget install Python.Python.3.13`. The Microsoft Store placeholder does not work.
- Node.js and the Mintlify CLI (`npm i -g mint`), for `mint validate`.
- Claude Code (CLI or VS Code extension).

## Choose How You Open the Repos

Claude Code loads the kit only from the folder that a session **starts** in. Choose one of these setups.

### Option A: Open `elitea.github.io` (Recommended)

1. In VS Code, open the `elitea.github.io` folder itself. To see the code repos too, select **File** > **Add Folder to Workspace**, add them, and keep `elitea.github.io` first.
2. Start a new Claude Code chat.

Nothing else is needed: the repo's `.claude/settings.json` and `CLAUDE.md` turn the kit on.

### Option B: Open the Parent Folder

If you open the parent folder (with all four repos inside), the kit does not load automatically. To load it, add these two files in the **parent** folder. They are not in git and stay on your machine.

1. Create `<parent>/CLAUDE.md`:

   ```
   Doc repo: `elitea.github.io/`. All paths in the kit below are relative to it; run kit commands from inside it (`cd elitea.github.io`).

   @elitea.github.io/.claude/kit/KIT.md
   ```

2. In `<parent>/.claude/settings.local.json`, add the kit permissions and hooks next to your own settings. See the blocks in [Parent-Folder Settings](#parent-folder-settings).
3. Start a new Claude Code chat.

## Set Your Repo Paths

The kit finds the code repos at `../EliteaUI`, `../elitea-sdk` and `../elitea_core` (relative to `elitea.github.io`). If yours are elsewhere, run this in `elitea.github.io`:

```
python .claude/kit/df.py cfg repo EliteaUI <path>
python .claude/kit/df.py cfg repo elitea-sdk <path>
python .claude/kit/df.py cfg repo elitea_core <path>
```

The paths are saved in `.claude/local.json`, which is git-ignored and personal. To check the result, run `python .claude/kit/df.py cfg`.

## Check That the Kit Works

In a new chat, ask "what's the status?". Claude answers with a line like `doc-factory: code branch main; lock ON: docs/ read-only`. If Claude does not know this line, the kit did not load: check which folder the session started in.

### Testing on a Temp Copy

To try a routine without touching `docs/`, copy the page into the kit's temp folder (`doc-factory/` in your system temp folder). Rules do not load automatically there, so tell Claude to read `.claude/rules/` first. Add `--as <docs page>` to `df.py lint` and `df.py links` so the scripts apply the real page's rules, for example `python .claude/kit/df.py lint <temp copy> --as docs/how-tos/modules/web-search.mdx`.

## How the Kit Behaves

- **Branches are yours.** You check out, switch and pull every branch (doc and code) yourself. Claude never fetches, pulls, checks out or switches.
- **Code branch.** Before every task that reads code, Claude asks which code branch to use and offers the last one. Change it at any time: `python .claude/kit/df.py cfg branch <name>` (the name is validated in all three repos).
- **Approval first.** Claude reports numbered findings and changes only what you approve. It never commits, pushes or opens PRs.
- **Protection (guard hook).** Claude can write only to `docs/` (pages, `docs.json`, `img/`), the kit's own folders (`.claude/kit/`, `rules/`, `skills/`, `agents/`), `CLAUDE.md` and the system temp folder `doc-factory/`. It cannot write to the styleguides, `docs/archive/`, the release-notes skill, the code repos or any other folder. Edits to settings and hook files need your confirmation.
- **Setup lock.** `python .claude/kit/df.py cfg lock on` makes `docs/` read-only for Claude. Only you can turn it off, in your own terminal: `python .claude/kit/df.py cfg lock off`. Claude is blocked from running that command.
- **After-edit check.** After Claude edits a docs page, a script checks the changed lines and reports at most three issues to Claude. It never edits anything.
- **Temp folder.** Findings lists, digests and indexes go to the system temp folder (`doc-factory/`), never to the repo. Deleting that folder is safe.

## Known Limits

- The guard reads shell commands as plain text. A command that hides a path in a variable or wildcard, or writes to the temp folder and somewhere else at once, may not be caught. The Claude Code permission prompt still applies to such commands.
- The script checks only patterns. Oxford commas, word order, ambiguous pronouns and real UI labels such as "Personal Settings" need a review by the proofreader or a person.
- The VS Code extension does not show the session-start line. Ask "what's the status?" instead.

## Parent-Folder Settings

For [Option B](#option-b-open-the-parent-folder) only. Add these entries to `<parent>/.claude/settings.local.json`. Keep everything that is already in your file.

Inside `"permissions"` > `"allow"`:

```json
"Bash(cd elitea.github.io && python .claude/kit/df.py *)",
"Bash(python elitea.github.io/.claude/kit/df.py *)"
```

At the top level, next to `"permissions"`:

```json
"hooks": {
  "PreToolUse": [
    {
      "matcher": "Write|Edit|MultiEdit|NotebookEdit|Bash|PowerShell",
      "hooks": [{ "type": "command", "command": "python \"$CLAUDE_PROJECT_DIR/elitea.github.io/.claude/kit/hooks/guard.py\"", "timeout": 5 }]
    }
  ],
  "PostToolUse": [
    {
      "matcher": "Write|Edit|MultiEdit",
      "hooks": [{ "type": "command", "command": "python \"$CLAUDE_PROJECT_DIR/elitea.github.io/.claude/kit/hooks/post_edit.py\"", "timeout": 10 }]
    }
  ],
  "SessionStart": [
    {
      "matcher": "startup|clear|compact",
      "hooks": [{ "type": "command", "command": "python \"$CLAUDE_PROJECT_DIR/elitea.github.io/.claude/kit/hooks/session_start.py\"", "timeout": 5 }]
    }
  ]
}
```

## Merging with Another Docs Kit

The root `CLAUDE.md` contains one import line per kit. To add another kit, add its import line; the kits do not share files. The kit's command and skill names do not overlap with the skills in `origin/add/claude-docs-toolkit`.

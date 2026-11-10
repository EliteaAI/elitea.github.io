---
name: create-toolkit-guide
description: Use when asked to write a new toolkit integration guide (docs/integrations/toolkits/<name>_toolkit.mdx) for an ELITEA toolkit, e.g. "add a toolkit guide for Tavily".
---

# Create toolkit guide

Standards: rules in `.claude/rules/` (auto-loaded for `docs/**/*.mdx`). Structure: `skeleton.md` in this folder.

## 1. Scope
- Get: toolkit name, ticket number (optional), release branch (default: current `release/*` of the sibling repos; confirm with `git -C ../elitea-sdk branch --show-current`).
- If a ticket is given: `gh issue view <n> -R EliteaAI/elitea_issues --comments`. Scope = its acceptance criteria.
- Confirm the page path `docs/integrations/toolkits/<name>_toolkit.mdx` does not exist (if it does, use `update-doc`).

## 2. Research (delegate)
Call the `doc-researcher` agent once with: toolkit name, branch, and this checklist:
- credential model fields (name, label, required, default, secret) and Test Connection behavior/errors
- toolkit config fields (label, type, default, limits) and tool groups
- every tool: UI label, method name, description, key parameters, return shape, output caps
- UI labels for fields and tools: the schema's `title`/`label` if set; otherwise how EliteaUI renders the key (find the humanize function used by the toolkit form) — mark `UNVERIFIED` if neither is found
- flows for credential + toolkit forms (EliteaUI), including Test Connection messages and the MCP access toggle
- the toolkit's `categories` value (maps to the nav group)
- auth modes, error messages worth troubleshooting, chat_tools / special behavior
Do not read the code yourself unless the fact sheet leaves a specific gap.

## 3. Draft
1. Read `skeleton.md` (including its Depth list). Read `docs/integrations/toolkits/outlook_toolkit.mdx` only for the sections the skeleton says to copy (Testing, Step 3, Support Contact): grep for the heading and read that range.
2. Write the page section by section with Write once, then Edit per section. Keep each response short; never output the full page in chat.
3. Every credential and toolkit field from the fact sheet appears in a table. Every tool appears in Available Tools.
4. Images: insert final references with planned names `[x]-cred-navigate.png`, `[x]-cred-configs.png`, `[x]-toolkit-navigate.png`, `[x]-toolkit-configs.png`, `[x]-add-agent.png`, `[x]-add-pipeline.png`, `[x]-add-chat.png` under `../../img/integrations/toolkits/[x]/`. List them under Open questions as "screenshots needed".
5. Facts missing from the fact sheet: write nothing; add to Open questions.

## 4. Nav & checks
1. `python .claude/skills/update-nav/nav.py groups Toolkits`; choose the group matching the SDK `categories` value (e.g. `other` → Other); ask if none matches.
2. `python .claude/skills/update-nav/nav.py add integrations/toolkits/<name>_toolkit --group "<Group>" --sorted`
3. `python .claude/hooks/validate_doc.py docs/integrations/toolkits/<name>_toolkit.mdx` — fix all except missing planned screenshots.

## 5. Report
`Changed: <page>, docs/docs.json | Notes: <≤3 lines> | Open questions: <list>`
Suggested commit message: `Add [X] toolkit integration guide`.

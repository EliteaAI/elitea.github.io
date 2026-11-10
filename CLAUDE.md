# ELITEA Documentation

Mintlify site. Published content is `docs/`. Ignore `.github/copilot-instructions.md`, `.github/instructions/*`, the PR template and `README.md`: they describe the old MkDocs setup.

## Structure
- `docs/docs.json`: theme, nav (tabs > groups > pages, extensionless paths), `redirects`.
- `docs/<section>/**/*.mdx`: home, getting-started, how-tos, integrations, menus, migration, release-notes, support.
- `docs/img/<section>/<feature>/`: images, GIFs, videos.
- `docs/styleguides/*.mdx`: the house style (language, wording and formatting, visual standards, usage dictionary). Read-only.
- `docs/archive/`, `docs/mintlify.schema.json`: read-only.

## Sources of truth (sibling repos in `../`)
- `../EliteaUI`: UI labels, forms, flows.
- `../elitea-sdk`: toolkits (`elitea_sdk/tools/<name>`), credentials (`elitea_sdk/configurations`), runtime.
- `../repos/elitea_core`: backend, API.
- Use the current `release/*` branch; ask if unsure. Tickets: `gh issue view <n> -R EliteaAI/elitea_issues`.

## Commands
- Preview: `cd docs && mint dev` (port 3000).
- Checks: `cd docs && mint broken-links`, `mint validate`, `mint a11y`.
- Validate files: `python .claude/hooks/validate_doc.py <file|dir>...`.
- Nav: `python .claude/skills/update-nav/nav.py <find|add|rename|check> ...`.
- Use `python`, not `python3`.

## Core conventions
- Rules in `.claude/rules/` load by path; follow them.
- Document only what exists in code; stay within the ticket's acceptance criteria.
- Edit minimally; never reformat untouched text.
- Commits: short imperative sentence case, no prefix ("Add Tavily toolkit integration guide"). Commit only when asked.

## Skills
create-toolkit-guide, create-doc-page, update-doc, place-images, doc-review, fix-links, update-nav, maintain-toolkit. Release notes: the existing `release-notes` skill (do not edit it).

---
repo: <EliteaUI | elitea-sdk | elitea_core>
github: EliteaAI/<repo>
branch: <code branch, e.g. main>
sha: <short sha the map was built from>
refreshed: <YYYY-MM-DD>
---
## Lookup
Where each kind of fact lives and how to find it (one line each):
- <fact type, e.g. UI label> → <path pattern> → `git grep -n "<term>" <ref> -- '<glob>'`

## Features → modules + docs
One line per user-facing feature: `<feature>: <route or entry point> → <code folders/files> | docs: <doc folders>`

## Doc-relevant gotchas
What changes what a user sees (permissions, project type, entity-type differences, hidden/disabled states).

## Config & flags
Settings and flags that show, hide or change features: `<flag> → <effect> (<file>)`

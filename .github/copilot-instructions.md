# Copilot Global Instructions – ELITEA Documentation (Mintlify)

These instructions guide GitHub Copilot (Chat + inline) when generating, editing, or restructuring documentation in this repository. Documentation is served via Mintlify from the `mintlify` branch.

# ==================================================================== 0. STACK & BUILD CONTEXT

- Documentation platform: Mintlify (https://mintlify.com)
- Source branch: `mintlify` (Mintlify reads directly from this branch)
- Config file: `docs/docs.json` on the `mintlify` branch
- Live docs site: https://docs.elitea.ai
- File format: MDX (`.mdx`) — Markdown with JSX components
- Landing page: Next.js in `web/`, deployed to https://elitea.ai via GitHub Pages from `main`
- Navigation is declared in `docs/docs.json`. New pages require BOTH file creation AND a nav entry in `docs/docs.json`.

====================================================================

# ==================================================================== 1. AUDIENCE & VOICE

Audience: Non‑technical or light‑technical business/analyst users.
Tone: Clear, direct, reassuring, factual (no hype).
Voice: Active (“Click”, “Select”), second person (“You”).
Avoid: Over‑promising claims about AI determinism; unverified performance statements.

# ==================================================================== 2. NAVIGATION STRUCTURE (docs/docs.json on mintlify branch)

Top-level groups (current):

1. Home / Introduction
2. Getting Started
3. How-Tos
4. Integrations & Toolkits
5. Release Notes
6. Support

Copilot must:

- Map requests to an existing group when possible.
- Provide nav insertion snippet suggestions for `docs/docs.json` when proposing new pages.
- Not silently reorder or rename nav groups.
- Use `.mdx` file extension for all new documentation pages.

# ==================================================================== 3. FILE NAMING & PATHS

Observed mix: kebab-case (personal-access-token.md) and snake_case (very_quickstart_guide.md).
Rules for NEW files:

- Prefer kebab-case (create-agent-pipeline.md).
- Keep existing legacy names unchanged unless user authorizes a migration.
- Place pages in group-consistent directories mirroring current taxonomy.

Release Notes Pattern:

- Current: rn_current.md (label in nav shows active version).
- Archive: archived/rn{n}.md where nav label supplies semantic version (“RN 1.5.2”).
  Do NOT infer version from file name; rely on nav label or user prompt.

# ==================================================================== 4. MINTLIFY CONVENTIONS

Callouts (preferred syntax):
<Note>Body text.</Note>
<Warning>Body text.</Warning>
<Tip>Body text.</Tip>
<Info>Body text.</Info>

Supported types: Note, Warning, Tip, Info, Check.
Do NOT use MkDocs admonition syntax (!!!) — it will not render in Mintlify.

Tabs:
<Tabs>
<Tab title="UI">
UI instructions here
</Tab>
<Tab title="API">
API instructions here
</Tab>
</Tabs>

Code highlighting:
Use triple backticks with language hints (`json, `bash). Mintlify renders these natively.

Accordion (collapsible):
<Accordion title="Advanced configuration">
Content hidden by default.
</Accordion>

Cards:
<Card title="Title" icon="icon-name" href="/path">
Description text.
</Card>

Content notes:

- Prefer Mintlify callout components for warnings, tips, and conceptual disclaimers.
- MDX allows JSX components — use Mintlify's built-in component library before building custom HTML.

# ==================================================================== 5. STANDARD PAGE SKELETONS

(UNCHANGED logic, adapted to Material admonitions)

Platform Documentation (Menus / Extensions):

```
# <Menu or Extension Name>
Short purpose sentence.
## Key Capabilities
- …
## When to Use
## Access Path
## How It Works
## Common Tasks
- Task (link to How TO / Quick Start)
## Related
```

Feature Guide:

```
# <Feature Name> Guide
Intro (what + why).
## Concepts
## Setup / Prerequisites
## Usage Patterns
## Examples
## Best Practices
## Limitations
## Related
```

Quick Start:

```
# <Task Name> Quick Start
## Overview
## Prerequisites
## Steps
1. …
2. …
## Result
## Next Steps
```

How TO:

```
# <Action-Oriented Title>
## Goal
## Prerequisites
## Steps
## Verification
## Troubleshooting
```

Release Notes:

```
# Release <Version> (YYYY-MM-DD)
## Added
## Changed
## Fixed
## Deprecated
## Security
## Known Issues
```

Glossary (single page):
Bold term + single-sentence definition; optional brief extension.

# ==================================================================== 6. FRONT MATTER & METADATA

Mintlify requires front matter on every page:

```yaml
---
title: "Page Title"
description: "One-sentence description for SEO and sidebar tooltip."
---
```

Keep keys minimal. Do not fabricate version numbers. `title` and `description` are the most important fields.

# ==================================================================== 7. LINKING PRACTICES

- Use absolute paths from the docs root (e.g., `/getting-started/chat-quick-start`) for internal links.
- For links to the landing page use https://elitea.ai.
- Avoid relative paths between pages — Mintlify resolves from docs root, not file system.
- Do not use `/docs/...` prefix — that was the old MkDocs path. All Mintlify paths start from root of docs.elitea.ai.

# ==================================================================== 8. SCREENSHOTS & MEDIA

No entrenched convention detected; recommended:
docs/assets/images/<group>/<topic>-<state>-step<n>.png
Alt text = purpose (“Agents list displaying status badges”), not decorative description.
Material supports light/dark theme switching—prefer neutral images (cropped UI) that remain legible in both themes. If dark-specific, suffix -dark.

Embed:
![Agents list showing active agents](../../assets/images/platform/agents-list-step1.png)

Optional caption (Material):
![Alt text](path){ width="800" }

# ==================================================================== 9. ACCESSIBILITY & I18N

- Write neutral source English ready for localization (Greek config suggests per-locale expansion).
- Avoid idioms, humor requiring cultural context.
- Provide descriptive link text (“See Pipelines Menu”) not “click here”.

# ==================================================================== 10. AI FEATURE DISCLOSURE

If a page explains AI-generated outputs:
!!! note "AI Output Variability"
AI-generated responses may vary. Review outputs before acting on them.

Avoid deterministic claims (“always returns” → “can return”).

# ==================================================================== 11. RELEASE NOTES WORKFLOW

When new version is published:

1. Copy rn_current.md → archived/rn{nextNumber}.md (increment highest).
2. Insert archived file into nav under Archive with proper “RN X.Y.Z” label.
3. Replace rn_current.md contents with new version section template.
4. Update nav label of rn_current.md to new version (RN X.Y.Z).
   Copilot must provide instructions; not perform renames autonomously unless user explicitly requests.

# ==================================================================== 12. QUALITY CHECKLIST (COPILOT INTERNAL)

[ ] Category skeleton adhered to  
[ ] Navigation group suggested (with nav snippet)  
[ ] File naming consistent (kebab-case for new)  
[ ] Admonitions use Material syntax (no legacy blockquotes)  
[ ] Links sanitized (no double slashes)  
[ ] Glossary linkage (first occurrence only)  
[ ] No fabricated features/versions/CVEs  
[ ] Steps ≤7 in Quick Start unless justified  
[ ] Release note sections properly categorized  
[ ] Screenshots (if proposed) have semantic filenames + alt placeholders

# ==================================================================== 13. WHEN INFORMATION IS MISSING

Ask clarifying questions if:

- Target nav group unclear
- Version not specified for release notes
- Whether to archive previous release
- Need for screenshots / number of steps ambiguous
- Requirement for front matter unknown

# ==================================================================== 14. EXAMPLES

Admonition conversion:
Legacy:

> **Note:** Pipelines require a project.

Material:
!!! note
Pipelines require a project.

Tabs example for UI vs CLI (if CLI support documented):
=== "UI" 1. Open **Pipelines**.
=== "API"
`bash
    curl -X POST /pipelines
    `

# ==================================================================== 15. PROHIBITED

- Creating new top-level nav groups without user instruction
- Mixing Quick Start + deep Concept sections in one file
- Adding raw HTML replicating Material features
- Inventing version histories or security notices

End of Global Instructions.

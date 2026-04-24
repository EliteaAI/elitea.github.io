# Release Notes Skill — ELITEA Platform

## Purpose

This skill teaches GitHub Copilot how to produce publication-ready ELITEA
release notes in MDX format from a GitHub Projects JSON export.

---

## 1. Input Format

The JSON export is an array of issue objects. Each object has these fields:

| Field        | Type   | Description                                          |
| ------------ | ------ | ---------------------------------------------------- |
| `number`     | int    | GitHub issue number                                  |
| `title`      | string | Issue title (may have `[BUG]`, `[Enhancement]` etc.) |
| `issue_type` | string | `Bug`, `Enhancement`, `Story`, `Epic`                |
| `state`      | string | GitHub state (`OPEN`, `CLOSED`)                      |
| `url`        | string | GitHub issue URL to use in Fixed/Known sections      |
| `status`     | string | Project board column (see §2)                        |
| `content`    | string | Full issue body in Markdown                          |

---

## 2. Categorization Rules

Apply these rules strictly. A single issue falls into exactly one category.

Before finalising **Fixed Issues** and **Known Issues**, compare the export with
the existing release-notes file if one already exists (for example,
`docs/release-notes/rn_current.mdx`). Reconcile any issue already listed in
the existing **Known Issues** section by issue number:

- If the export now classifies it as Fixed, move it to **Fixed Issues**.
- If the export still classifies it as Known, keep it in **Known Issues**.
- If the issue is absent from the export, do not assume it is fixed.

### 🔴 Known Issues

**Criteria:** `status` is `"Bugs"` OR `"Development"`

These are bugs that are **not yet fixed** in this release. They are
acknowledged limitations users should be aware of.

### ✅ Fixed Issues

**Criteria:** `issue_type` is `"Bug"` AND `status` is one of:

- `"In Testing"`
- `"Verified on DEV Env"`
- `"Ready for Public Release"`
- `"Done"`

These are bugs that have been resolved in this release.

### 🆕 New Features & 🔄 Changed Features

**Criteria:** `issue_type` is `"Enhancement"`, `"Story"`, or `"Epic"` AND
`status` is one of:

- `"In Testing"`
- `"Verified on DEV Env"`
- `"Ready for Public Release"`
- `"Done"`

**New Feature** = a capability that did not exist before.  
**Changed Feature** = an improvement, redesign, or extension of an existing
capability. Use the issue title and content to determine which applies.

---

## 3. Functional Area Grouping

Group features (New + Changed) by the platform area they belong to.
Use the issue title and content to determine the area. Standard areas:

| Label                     | Keywords / Signals                                   |
| ------------------------- | ---------------------------------------------------- |
| Chat & Agents             | chat, conversation, agent, model settings            |
| Pipelines                 | pipeline, node, flow, canvas                         |
| Toolkits                  | toolkit, credential, indexing, SharePoint, Jira etc. |
| Artifacts                 | artifact, bucket, DOCX, canvas, file                 |
| Notifications             | notification, expiration, alert, email               |
| Administration & Settings | admin, project settings, analytics, environment      |
| Import / Export           | import, export, fork                                 |
| MCPs                      | MCP, remote MCP, OAuth                               |
| Other Improvements        | anything that doesn't fit above                      |

Fixed issues and Known issues do **not** need to be grouped by area — list
them as a flat numbered list.

---

## 4. Writing Rules

### Feature entries (New or Changed)

Each feature gets this structure:

```
### [Feature Title — short, human-readable, no issue codes]

[One paragraph explaining what this is and why it matters to the user.]

**What you can do now:**
- [Concrete action the user can take]
- [Another action]
- ...

**Benefits:** [One sentence on the key value: speed, safety, clarity, etc.]

For more information, see [Link Text](relative/doc/path).
```

The "For more information" line is optional — include it only when you know
a doc page exists. Verify the link target by checking the repository `docs/`
tree before adding it. Leave the line out rather than inventing a path.

### Bug fix entries

Single sentence per bug:

```
* [#1234](https://github.com/org/repo/issues/1234) **[Short description of what broke]**: [What now works correctly, in plain language.]
```

Always use the GitHub URL from the export's `url` field.

### Known issue entries

Single sentence per issue:

```
* [#1234](https://github.com/org/repo/issues/1234) **[Short description of the known limitation]**: [What users may observe and any workaround if known.]
```

Always use the GitHub URL from the export's `url` field.

---

## 5. MDX Output Template

```mdx
---
title: "Release Notes - {VERSION}"
description: "{ONE_LINE_SUMMARY_OF_RELEASE}"
---

## Release Overview

{2-3 sentence paragraph summarising the release themes and what users gain.}

## Information

- **Release Version**: {VERSION}
- **Released on**: {RELEASE_DATE}
- **Access**: [Next environment](https://next.elitea.ai)

## New Features

### {Functional Area}

#### {Feature Title}

{Feature body following the template in §4}

[... more features ...]

## Changed Features

### {Functional Area}

#### {Feature Title}

{Feature body following the template in §4}

[... more changed features ...]

## Fixed Issues

{Flat bullet list following the template in §4}

## Known Issues

{Flat bullet list following the template in §4}
```

---

## 6. Quality Checklist

Before outputting, verify:

- [ ] Every issue in the JSON appears in exactly one section.
- [ ] Existing Known Issues were reconciled against the export by issue number.
- [ ] No raw exception text, stack traces, or internal variable names are
      visible in the human-readable output.
- [ ] Issue titles have been rewritten into plain English (no `[BUG]`,
      `[Enhancement]` prefixes, no `#number` in body text).
- [ ] Every Fixed Issue and Known Issue bullet starts with a linked GitHub issue ID using the export `url` value.
- [ ] Every "For more information" link points to a doc page that actually exists in `docs/`.
- [ ] All MDX front-matter fields are filled in.
- [ ] The file is valid MDX (no unclosed JSX tags, no stray `<` characters).
- [ ] Tone is consistent: second person ("you"), active voice, present tense.

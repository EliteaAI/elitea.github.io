# ELITEA Release Notes — Style Guide

Audience: **end users without technical knowledge.** Notes must be short and easy to read. Describe what the user can do and see, never how it is built.

## Language

- Plain, active, present tense. Address the reader as **you**. Short sentences.
- UI names in **bold** exactly as shown in the product: **Settings → General**, **Run History**, **Pause and ask me**.
- Capitalize ELITEA entities: Agents, Pipelines, Skills, Toolkits, MCPs, Chats (as entities); "chat" as a common noun is fine.
- Code font only for things the user types or sees literally: `DELETE`, `~skill-name`, `· 3.2s`.
- Never mention: repos, PRs, file/function names, endpoints, database tables, feature flags by technical name, sub-issue numbers, story codes (S1, TS2, WS3), people.
- No marketing words ("powerful", "seamless", "revolutionary"). No "we".

## Feature block (New Features and Changed Features)

```mdx
### Feature Name

You can now <one sentence: what the user can do now>.

* <3–6 bullets: concrete things the user can do or see, most important first>
* <admin-only or off-by-default behaviour gets its own bullet>
* <compatibility: "Existing X keep working without changes." when relevant>

<Note>
<optional: an important limitation the user must know>
</Note>

**Benefits:** <one short phrase or sentence>.

Details: [Page or Section Title](../path/page#anchor), [Another](../path/page#anchor).

<img src="../img/path/image.png" alt="<what the image shows>" />
```

Rules:
- **Heading**: a short noun phrase in Title Case ("Scheduled Agents and Pipelines", "Export and Import Chats"). No issue numbers.
- **Opening sentence**: "You can now …" for most features. For admin features: "Platform administrators can now …". For a redesign or behaviour change: "The <thing> is redesigned to …" / "<Thing> now …".
- **Grouped issues**: one block that covers all of them. Use bold sub-labels (`**Usage**`, `**Analytics**`) with their own bullet lists when the group has two clear parts.
- **Bullets**: one idea each, ≤ 2 lines. Describe what the user can do, not navigation steps ("Open …, find …" belongs in the opening sentence: "…in the new **X** section in **Settings → General**").
- **Entity type names** in lists are bold when they are UI options the user selects (**Chats**, **Agents**). Start with a verb or the subject the user cares about ("Select …", "See …", "Existing Pipelines …").
- `<Note>` for limitations; `<Warning>` for irreversible actions, deprecations and data loss. At most one per feature.
- **Benefits**: one line, user value, no repetition of the bullets.
- **Details**: relative links from `docs/release-notes/` with real anchors (from `doc_index.py`). If no page exists yet, write `Details: {/* TODO: add link to the <feature> documentation */}` followed by the closest existing links, if any.
- **Image**: optional, one per feature. Use an existing doc image when one shows the feature (`doc_index.py images`). Otherwise a placeholder `../img/release-notes/rn_<X.Y.Z>_<N>_<short-name>.png` (new features `N` = 1, 2, …; changed features `N` = c1, c2, …). Small features (no new screen) get no image.
- **Order**: bigger features first (new pages, epics, many sub-issues), small enhancements last.

## Fixed Issues and Known Issues

One line each, sorted by issue ID **descending**:

```mdx
* [#7173](https://github.com/EliteaAI/elitea_issues/issues/7173) <one short sentence>.
```

- **Fixed**: describe the corrected behaviour as it is now: "X works …", "X no longer …", "X shows …". Not "Fixed a bug where …".
- **Known**: describe the problem as the user sees it: "X fails when …", "X shows … instead of …".
- One sentence, ≤ 25 words, no root causes, no technical terms (no "400", "SIO", "checkpoint", "payload").

## Intro paragraph

One paragraph, 3–4 sentences, directly under the front matter:
1. A one-line theme of the release ("ELITEA 2.0.8 lets your Agents and Pipelines work on their own and keeps your data safer.").
2. "This release introduces …" — the 3–5 biggest new features.
3. "It adds …" / "It also …" — remaining notable new features, then the main changed features.
Do not list Fixed or Known Issues. Small features may be left out.

## Scope rules (what to include)

- **Comments override the body.** Developer/QA comments with decisions, "scope update", "vs. spec", "final plan" or "verified" describe what actually shipped. Merged PR descriptions are the strongest evidence of shipped behaviour.
- **Sub-issues**: always read them. Include behaviour from sub-issues in the current milestone; leave out sub-issues in a later milestone (e.g. R-2.0.9) and say so in the report. Bug sub-issues that fix the feature are described as working behaviour.
- **Partial delivery**: if the parent describes more than the sub-issues deliver, write the version the issue describes and flag the gap in the report (unless a comment clearly says it was cut — then follow the comment).
- **Off by default / admin-only / enterprise**: say so in a bullet.
- **Superseded stories** (closed "as superseded"): use the replacement stories.
- When in doubt, write the best version and **flag it** in the report. Never stop to ask.

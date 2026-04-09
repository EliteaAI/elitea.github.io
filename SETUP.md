# ELITEA Setup And Development Guide

This file is the practical runbook for engineers and content authors working in this repository.

Use it when you need to:

- understand what can be edited here
- run the Mintlify docs locally
- update navigation or add new pages
- run the landing page locally
- understand how deployment works

## Repository Surfaces

This repository contains two different apps:

### 1. Documentation Site

Location: `docs/`

Tech stack:

- Mintlify
- MDX content
- JSON navigation/config in `docs/docs.json`
- CSS overrides in `docs/custom.css`

This is where you edit:

- product documentation
- getting started guides
- task-based how-tos
- integrations, MCP, toolkit, and UI reference docs
- release notes
- troubleshooting and support content

### 2. Landing Site

Location: `web/`

Tech stack:

- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- static export deployed to GitHub Pages

This is where you edit:

- the public marketing / landing experience
- landing page copy and layout
- website assets and styling in the web app

## Prerequisites

Required:

- Node.js 18+
- npm

For docs preview:

- Mintlify CLI available as the `mint` command

For basic validation:

- Python 3 for quick JSON validation commands used in this repo

## Documentation Workflow

### Where docs live

The documentation source is the `docs/` directory.

Important files:

- [docs/docs.json](docs/docs.json): site navigation and Mintlify configuration
- [docs/custom.css](docs/custom.css): Mintlify styling overrides
- [docs/index.mdx](docs/index.mdx): docs landing page
- [docs/img/](docs/img/): shared documentation assets

Important content sections:

- `docs/home/`
- `docs/getting-started/`
- `docs/how-tos/`
- `docs/integrations/`
- `docs/menus/`
- `docs/migration/`
- `docs/release-notes/`
- `docs/support/`

### Run Mintlify locally

From the repo root:

```bash
cd docs
mint dev
```

This starts the local docs preview, typically at `http://localhost:3000`.

Use this whenever you change:

- `.mdx` content
- `docs.json`
- `custom.css`
- images referenced by docs pages

### Typical docs edit loop

1. Open the target file in `docs/`
2. Start local preview:

```bash
cd docs
mint dev
```

3. Make the content, navigation, or style change
4. Refresh the browser if needed
5. Verify:

- page renders correctly
- left navigation placement is correct
- page title / description look correct
- links work
- images load
- light and dark theme styling still looks right

### Add a new docs page

1. Create a new file under the right section, for example:

```text
docs/how-tos/my-new-guide.mdx
```

2. Add frontmatter:

```mdx
---
title: "My New Guide"
description: "Short summary of what this page helps users do."
---
```

3. Add the page to the appropriate section in [docs/docs.json](docs/docs.json)
4. Run `mint dev` and verify the page appears in the expected navigation group

### Update docs navigation

Navigation is managed in [docs/docs.json](docs/docs.json).

Common changes:

- adding a new page path to an existing group
- renaming tabs, groups, or sidebar items
- regrouping pages under a new collapsible section
- updating navbar links and branding configuration

When editing `docs.json`:

- keep paths extensionless, for example `how-tos/chat-conversations/how-to-canvas`
- validate JSON before committing
- always preview navigation changes in Mintlify locally

Quick validation:

```bash
cd docs
python3 -m json.tool docs.json >/dev/null
```

### Docs authoring notes

Use root-relative paths for shared images:

```mdx
![Example](/img/example.png)
```

Built-in Mintlify components commonly used in this repo include:

- `Info`
- `Tip`
- `Warning`
- `Tabs`
- `Steps`
- `CardGroup`
- `Card`

### Docs troubleshooting

#### `mint dev` fails with invalid `docs.json`

Run:

```bash
cd docs
python3 -m json.tool docs.json >/dev/null
```

Common causes:

- invalid JSON syntax
- unsupported Mintlify config values
- non-URL values in fields that require URLs

#### Broken links in docs

Run:

```bash
cd docs
mint broken-links
```

In this repo, local markdown links must be explicit relative links such as `./page` or `../section/page`.

#### MDX parse errors

Common causes:

- invalid frontmatter
- unclosed JSX-style Mintlify components
- invalid braces in plain text
- malformed HTML inside MDX

Use local preview to identify the exact file and component causing the problem.

## Landing Site Workflow

### Where the landing site lives

The landing site source is under `web/`.

Important files:

- [web/package.json](web/package.json)
- [web/next.config.js](web/next.config.js)
- [web/src/](web/src/)

### Run the landing site locally

```bash
cd web
npm install
npm run dev
```

This starts the Next.js dev server, typically at `http://localhost:3000`.

Note: both the landing site and Mintlify preview usually default to port `3000`, so run one at a time unless you intentionally use different ports.

### Build the landing site locally

```bash
cd web
npm run build
```

The site is configured as a static export for GitHub Pages deployment.

## Deployment Model

### Docs deployment

Docs deployment is handled by Mintlify based on the configured repository, branch, and `docs/` directory.

This repo does not contain a GitHub Actions workflow that builds the Mintlify docs site.

### Landing site deployment

Landing deployment is handled by [deploy-unified.yml](.github/workflows/deploy-unified.yml).

It triggers on:

- pushes to `main` affecting `web/**`
- manual workflow dispatch

The workflow:

1. checks out the repo
2. installs dependencies in `web/`
3. runs `npm run build`
4. copies `web/out/` into the deployment artifact
5. deploys to GitHub Pages

## Recommended Workflow By Role

### For docs authors

Use this most of the time:

```bash
cd docs
mint dev
```

Edit:

- `.mdx` pages
- `docs.json`
- `custom.css`

### For frontend engineers

Use this most of the time:

```bash
cd web
npm install
npm run dev
```

Edit:

- `web/src/`
- styles and components in the landing app

## Quick Reference Commands

### Docs

```bash
cd docs
mint dev
python3 -m json.tool docs.json >/dev/null
mint broken-links
```

### Landing site

```bash
cd web
npm install
npm run dev
npm run build
```

## Common Issues

### Docs preview and landing page conflict on port 3000

Only run one local app at a time unless you deliberately reconfigure ports.

### JSON schema warning in VS Code for `docs.json`

You may see a VS Code warning about the Mintlify schema URL being untrusted. That warning does not necessarily mean `docs.json` is invalid. The source of truth for actual Mintlify compatibility is whether `mint dev` accepts the file.

### Landing build fails in `web/`

Try a clean rebuild:

```bash
cd web
rm -rf node_modules .next out
npm install
npm run build
```

## Final Check Before Committing

For docs changes:

1. run `mint dev`
2. validate `docs.json` if it changed
3. check navigation and links
4. confirm images and styles render correctly

For landing page changes:

1. run `npm run dev`
2. run `npm run build`
3. confirm the page still works as a static export

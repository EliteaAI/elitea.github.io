# ELITEA Repository

This repository contains two separately run and deployed surfaces:

- The ELITEA documentation site in `docs/`, built with Mintlify
- The ELITEA marketing / landing site in `web/`, built with Next.js and deployed as a static site

If you are editing docs, start in `docs/`. If you are editing the website, start in `web/`.

## What Is In This Repo

```text
elitea.github.io/
├── docs/                      # Mintlify documentation source
│   ├── docs.json              # Mintlify site configuration
│   ├── custom.css             # Mintlify styling overrides
│   ├── index.mdx              # Docs homepage
│   ├── home/                  # Product overview and core concepts
│   ├── getting-started/       # Quick starts and initial setup
│   ├── how-tos/               # Task-based guides
│   ├── integrations/          # MCPs, toolkits, extensions, apps
│   ├── menus/                 # Platform UI reference pages
│   ├── migration/             # Upgrade and migration content
│   ├── release-notes/         # Current and archived releases
│   ├── support/               # Troubleshooting and support content
│   └── img/                   # Documentation assets
├── web/                       # Next.js landing site
│   ├── src/                   # App source
│   ├── public/                # Public assets
│   ├── package.json           # Frontend scripts and dependencies
│   └── next.config.js         # Static export config
├── .github/workflows/
│   └── deploy-unified.yml     # GitHub Pages deployment for the landing site
├── CNAME                      # GitHub Pages custom domain
├── README.md
└── SETUP.md                   # Local development and deployment runbook
```

## What Documentation Is Available Here

The Mintlify docs in `docs/` are organized around the structure defined in `docs/docs.json`. At a high level, the site currently includes:

- Home: overview, onboarding, glossary, key concepts, platform overview
- Getting Started: quick starts, credentials, secrets, artifacts, system checks
- How-To Guides: chat, conversations, indexing, pipelines, agents, toolkits, entity management
- Integrations: MCP, toolkits, extensions, third-party integrations, applications
- Release Notes: current and archived releases
- Support: FAQs, troubleshooting, support, migration and legacy content

For content changes, expect to update both page files and navigation when necessary.

## Quick Start

### Prerequisites

- Node.js 18+
- npm
- Mintlify CLI installed and available as the `mint` command if you want to preview docs locally

### Run The Docs Locally

```bash
cd docs
mint dev
```

This starts the Mintlify preview server, typically on `http://localhost:3000`.

Use this workflow when you are changing:

- `.mdx` pages in `docs/`
- navigation in `docs/docs.json`
- styles in `docs/custom.css`
- images or other assets in `docs/img/`

### Run The Landing Page Locally

```bash
cd web
npm install
npm run dev
```

This starts the Next.js dev server, also typically on `http://localhost:3000`.

Because both apps usually use the same default port, run them one at a time unless you intentionally change one of the ports.

## Common Change Types

### Update Existing Documentation

1. Edit the relevant `.mdx` file under `docs/`
2. Run `mint dev` from `docs/`
3. Check the page, navigation, links, images, and callouts in the browser
4. If you changed page location or navigation, update `docs/docs.json`

### Add A New Documentation Page

1. Create a new `.mdx` file in the appropriate docs section
2. Add frontmatter with at least `title` and `description`
3. Add the page path to the appropriate section in `docs/docs.json`
4. Preview locally with `mint dev`

### Update Landing Page Content Or UI

1. Edit files under `web/src/`
2. Run `npm run dev` in `web/`
3. Validate responsive behavior and static export compatibility

## Validation

Useful local checks:

### Validate `docs.json`

```bash
cd docs
python3 -m json.tool docs.json >/dev/null
```

### Check Docs In Mintlify Preview

```bash
cd docs
mint dev
```

Use the preview to verify:

- page renders correctly
- sidebar/nav placement is correct
- local images resolve
- links work
- custom CSS changes behave in light and dark themes

## Deployment Model

### Documentation

The documentation site is deployed by Mintlify from the `docs/` directory. The exact target domain is controlled by Mintlify project configuration rather than by a GitHub Actions workflow in this repo.

### Landing Page

The landing page is deployed through [deploy-unified.yml](.github/workflows/deploy-unified.yml) to GitHub Pages when changes under `web/` are pushed to `main`.

The workflow:

1. Installs dependencies in `web/`
2. Builds the Next.js app
3. Publishes the static output to GitHub Pages

## Where To Look First

- Editing docs navigation: [docs/docs.json](docs/docs.json)
- Editing docs styles: [docs/custom.css](docs/custom.css)
- Editing docs content: [docs/](docs/)
- Editing landing page UI: [web/src/](web/src/)
- Landing page deployment: [.github/workflows/deploy-unified.yml](.github/workflows/deploy-unified.yml)

## More Detailed Setup

For a fuller local development and deployment runbook, including Mintlify editing workflow and common troubleshooting, see [SETUP.md](SETUP.md).

## License

See [LICENSE](LICENSE).

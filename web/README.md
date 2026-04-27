# Elitea.ai — Landing Page (`web/`)

Next.js landing page for [elitea.ai](https://elitea.ai).

> **Looking for documentation?**  
> Docs are managed in Mintlify on the `mintlify` branch and published at **[docs.elitea.ai](https://docs.elitea.ai)**.  
> Do **not** edit docs files in this repo — they live on the `mintlify` branch.

## Development

```bash
# Install dependencies
npm install

# Start dev server → http://localhost:3000
npm run dev
```

Or from the repository root:

```bash
./scripts/dev-landing.sh
```

## Build

```bash
npm run build
# Output: out/  (static export, deployed to GitHub Pages)
```

## Deployment

Deployment to GitHub Pages is triggered **manually**:

1. Go to **Actions** → **Deploy Landing to GitHub Pages**
2. Click **Run workflow**

The workflow builds `web/out/` and deploys it to `https://elitea.ai` via GitHub Pages.

## Project Structure

```
web/
├── src/
│   ├── app/              # Next.js App Router pages
│   ├── components/       # React components
│   └── lib/
│       └── constants.ts  # Centralised URLs (DOCS_URLS, etc.)
├── public/               # Static assets
├── out/                  # Build output (not committed)
└── package.json
```

## Key Configuration

| File | Purpose |
|------|---------|
| `next.config.js` | Next.js config (static export, basePath) |
| `src/lib/constants.ts` | Centralised docs URL constants |
| `tailwind.config.js` | Tailwind CSS theme |
| `tsconfig.json` | TypeScript config |

## Technology Stack

- **Next.js 14** — React framework with App Router + static export
- **TypeScript** — Type safety
- **Tailwind CSS** — Styling
- **Framer Motion** — Animations
- **Lucide React** — Icons

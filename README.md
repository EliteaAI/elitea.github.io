# elitea.ai — Landing Page

This repository contains the **Next.js landing page** for [elitea.ai](https://elitea.ai), deployed to GitHub Pages.

Documentation is maintained separately on the `mintlify` branch and served by Mintlify at **[docs.elitea.ai](https://docs.elitea.ai)**.

## 🌐 Sites

| Site          | URL                    | Source                       |
| ------------- | ---------------------- | ---------------------------- |
| Landing page  | https://elitea.ai      | `main` branch → GitHub Pages |
| Documentation | https://docs.elitea.ai | `mintlify` branch → Mintlify |

## 📁 Repository Structure

```
elitea.github.io/
├── web/                    # Next.js landing page
│   ├── src/               # Source code (app/, components/, lib/)
│   ├── public/            # Static assets
│   ├── out/               # Build output (generated, not committed)
│   └── package.json
├── scripts/               # Dev helper scripts
│   └── dev-landing.sh     # Start local dev server
└── .github/workflows/
    └── deploy-unified.yml # Deploys landing page to GitHub Pages
```

## 🚀 Local Development

```bash
# Install dependencies
cd web && npm ci

# Start dev server (http://localhost:3000)
./scripts/dev-landing.sh
# or
cd web && npm run dev
```

## 🏗️ Build

```bash
cd web && npm run build
# Output: web/out/
```

## 📦 Deployment

Deployment to GitHub Pages is triggered **manually** via GitHub Actions:

1. Go to the **Actions** tab
2. Select **Deploy Landing to GitHub Pages**
3. Click **Run workflow**

The workflow builds the Next.js app and deploys `web/out/` to GitHub Pages under the `elitea.ai` custom domain.

## ✏️ Updating Documentation

Documentation lives in the `mintlify` branch. To update docs:

1. Check out the `mintlify` branch
2. Edit `.mdx` files under `docs/`
3. Update navigation in `docs/docs.json` if adding new pages
4. Open a PR targeting the `mintlify` branch

Mintlify automatically picks up merged changes from the `mintlify` branch.

## 🔧 Configuration

- Landing page config: `web/next.config.js`
- Docs URL constants: `web/src/lib/constants.ts`
- Deployment workflow: `.github/workflows/deploy-unified.yml`

## 📄 License

See [LICENSE](LICENSE) file for details.

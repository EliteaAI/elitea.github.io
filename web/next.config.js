/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  // For custom domain (elitea.ai), we don't need basePath
  // All assets will be served from the root

  // Turbopack config (default in Next.js 16)
  // Fix for mermaid/cytoscape import issue - use browser-friendly shims
  turbopack: {
    resolveAlias: {
      fs: 'empty-module',
      path: 'path-browserify',
    },
  },

  // Keep webpack for backwards compatibility (only used if --webpack flag is passed)
  webpack: (config, { isServer }) => {
    if (!isServer) {
      // Fix for mermaid cytoscape import issue
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        path: false,
      }
    }
    return config
  },
}

module.exports = nextConfig

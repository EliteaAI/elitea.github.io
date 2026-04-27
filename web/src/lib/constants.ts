// Centralized documentation URLs — all pointing to Mintlify at docs.elitea.ai
export const DOCS_BASE_URL = 'https://docs.elitea.ai'

export const DOCS_URLS = {
  home: DOCS_BASE_URL,
  gettingStarted: `${DOCS_BASE_URL}/getting-started/chat-quick-start`,
  changelog: `${DOCS_BASE_URL}/release-notes/rn_current`,
  faq: `${DOCS_BASE_URL}/support/faqs`,
  mcpServerStdio: `${DOCS_BASE_URL}/integrations/mcp/mcp-server-stdio`,
} as const

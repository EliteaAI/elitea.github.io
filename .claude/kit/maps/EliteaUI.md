---
repo: EliteaUI
github: EliteaAI/EliteaUI
branch: main
sha: 55fe88c99
refreshed: 2026-11-17
---
## Lookup
- UI label (button, menu, tab, title) → hard-coded English string in JSX/hooks, near the feature. No i18n layer (no i18n package, no `useTranslation`) → `git grep -n "<label>" <ref> -- 'src/[fsd]' src/pages src/components` (e.g. "Publish": `src/[fsd]/features/skill/lib/hooks/usePublishSkillMenu.hooks.jsx:81`)
- Route URLs → `src/routes.js` (`RouteDefinitions`) → `git grep -n "<path>" <ref> -- src/routes.js`
- Route guards → `src/[fsd]/app/routes/` (ProtectedRoute.jsx, ProtectedRoutes.jsx, SkillsGuard.jsx, IntegrationGuard.jsx, router.jsx)
- Sidebar items and order → `src/[fsd]/widgets/sidebar-root/ui/Sidebar.jsx`, `SidebarBody.jsx`; route → item map in `widgets/sidebar-root/lib/constants/sidebar.constants.js`; "Create" menu → `widgets/sidebar-root/lib/constants/createEntity.constants.js`
- Entity words in headers/breadcrumbs ("AI Provider", "Token", "Secret") → `widgets/sidebar-root/lib/constants/createEntity.constants.js` (OptionsMap, RouteToLabelMap)
- Permission strings → `src/common/constants.js:537` (`PERMISSIONS` tree) → `git grep -n "PERMISSIONS.<area>.<action>" <ref> -- src`
- Permission check (who sees a control) → `src/hooks/useCheckPermission.js` (`checkPermission`, `checkPermissions`)
- Project type (private / public / team) → `src/[fsd]/shared/lib/hooks/useProjectType.hooks.js`; selected project → `useSelectedProject.hooks.js`
- Platform settings flags from backend → `src/api/platformSettings.js`; used in `src/[fsd]/pages/settings/Settings.jsx` (~lines 208-295) and `shared/lib/hooks/useMcpVisibility.hooks.js`
- Env / deploy config → `src/utils/env.js` (`getEnvVar`: `window.elitea_ui_config` key, lowercased, wins over Vite env), consts in `src/common/constants.js`, sample in `.env.example`
- Shared constants (limits, names, defaults) → `src/[fsd]/shared/lib/constants/*.constants.js`; feature-local ones in `<feature>/lib/constants/`
- Settings tab constants → `src/[fsd]/features/settings/lib/constants/` (tokens, usage, complexity, projectGeneral, ...)
- Repo conventions → `AGENTS.md`, `CLAUDE.md` (dev-only)

## Features → modules + docs
Code lives in `src/[fsd]/features/<f>`, pages in `src/[fsd]/pages/<p>`; legacy in `src/pages/<X>`.
- Chat and conversations: /chat, /chat/:conversationId, /shared/chat/:token → features/chat (conversation-list, participants, voice-config, ui), pages/shared-conversation, entities/folder | docs: how-tos/chat/*, how-tos/chat-conversations/*, menus/*
- Agents: /agents(/:tab/:agentId, /history, /evaluate, /schedules, /webhooks) → features/agent, pages/agent, widgets/agent-editor, widgets/entity-test-panel | docs: how-tos/agents-pipelines/*, menus/*
- Pipelines: /pipelines(...) → features/pipelines, pages/pipeline, widgets/pipeline-editor, widgets/pipeline-canvas-toolbar | docs: how-tos/pipelines/*, how-tos/pipelines/nodes/*, how-tos/agents-pipelines/*
- Skills and Skill Hub: /skills(/catalog/:skillId) → features/skill, features/skill-hub, pages/skills, widgets/skill-editor | docs: home/key-concepts/*, menus/*
- Agent Hub / ELITEA catalog: /agents-hub, /elitea-catalog → features/agent-hub, pages/agent-hub, pages/elitea-catalog | docs: menus/*
- Toolkits: /toolkits(/create/:toolkitType, /:tab/:toolkitId, /test) → features/toolkits, pages/toolkit, src/pages/Toolkits | docs: integrations/toolkits/*, how-tos/credentials-toolkits/*
- Indexes: /toolkits/:tab/:toolkitId/create-index, /index/:indexName(/history, /search) → pages/indexes, entities/indexing-report | docs: how-tos/indexing/*
- MCP: /mcps(...), /mcp-auth-callback → features/mcp, pages/mcp, features/openapi | docs: integrations/mcp/*
- Apps: /apps(/applications, /catalog, /create/:appType) → features/apps, pages/apps | docs: integrations/apps/*
- Credentials: /credentials(/create-credential/:credentialType) → features/credentials, src/pages/Credentials | docs: how-tos/credentials-toolkits/*, menus/*
- Artifacts: /artifacts (/create-bucket, /edit-bucket) → features/artifacts, src/pages/Artifacts | docs: menus/*, how-tos/entity-management/*
- Settings: /settings/:tab (project-general, ai-providers, tokens, secrets, users, project-context, schedules, webhooks, usage, analytics, governance, complexity) → pages/settings, features/settings, features/project, features/project-governance | docs: menus/settings/*
- Schedules and webhooks: .../schedules/..., .../webhooks/... → features/schedule, features/schedule-import-export, entities/schedule, widgets/schedules-table, pages/schedules | docs: menus/settings/*, how-tos/agents-pipelines/*
- Evaluation: .../evaluate(/datasets, /dimensions, /history) → widgets/evaluation, pages/agent-evaluate | docs: how-tos/agents-pipelines/*
- Run history and analytics: .../history(/analytics) → entities/run-history, widgets/run-history-page, widgets/skill-run-history | docs: how-tos/agents-pipelines/*
- Versions, compare, fork, publish → entities/version, entities/compare-versions, entities/fork | docs: how-tos/entity-management/*
- Import / export → entities/import-wizard | docs: how-tos/entity-management/*
- Onboarding and tours: /onboarding, /help-center → features/onboarding, features/interactive-tours, pages/resources, widgets/support-assistant | docs: getting-started/*, support/*
- Public user pages: /user-public/... → src/pages/UserPublic | docs: home/*
- Notifications → entities/notifications, src/pages/NotificationCenter | docs: menus/*
- Context budget / model selector → widgets/context-budget, widgets/llm-model-selector | docs: how-tos/chat/*
- Modules (internal tools: Web Search, Image Creation, Data Analysis, Ask User, Python Sandbox, Planner, Swarm Mode, Skill Builder, Project Context Builder, Agent & Pipeline Builder, Smart Tools Selection, Attachments): titles, tooltips and default fields in shared/lib/constants/internalTools.constants.js; availability in features/toolkits/lib/hooks/useAvailableInternalTools.hooks.js; chat + > Modules in features/chat/ui/chat-button/PlusChatButton.jsx; agent "+ Modules" in features/agent/ui/agent-details/configurations/modules/; defaults in features/settings/ui/project-general/DefaultModulesSettings.jsx | docs: how-tos/modules/*, menus/settings/*
- Web Search module: settings card features/settings/ui/project-general/WebSearchSettings.jsx; budget banner features/chat/ui/budget-warning/WebSearchBudgetWarning.jsx | docs: how-tos/modules/*, menus/settings/*
- Auth and consent → features/auth, features/owner-consent | docs: getting-started/*

## Doc-relevant gotchas
- No i18n: copy a label exactly from JSX; the same word may differ across modules (OptionsMap in `createEntity.constants.js` maps Credentials → "Credential", PersonalToken → "Personal Token").
- Two code trees: new code in `src/[fsd]/`, older screens still in `src/pages`, `src/components`, `src/hooks`, `src/api`, `src/common`. Search both.
- Permissions are checked against the project in use: in the public project (id from `VITE_PUBLIC_PROJECT_ID`) `publicPermissions` is used, in any other project `permissions` (`src/hooks/useCheckPermission.js:8-18`).
- Project types: private (selected project = the user's own project), public, team (everything else) (`useProjectType.hooks.js`).
- Own LLMs: when `allow_project_own_llms` is false and the project is not public, own-LLM controls are restricted (`shared/lib/hooks/useIsOwnLLMsRestricted.hooks.js:9`).
- Settings tabs hidden unless the backend enables them: analytics (`analytics_enabled === false` hides), usage (`cost_budgets_enabled`), complexity (`complexity_enabled`), governance (`governance_enforced`) (`pages/settings/Settings.jsx`).
- MCP entries are hidden from menu/toolkit lists when `mcp_exposure_enabled` or `mcp_in_menu_enabled` is false; the MCP category label comes from `mcp_category_name`, default "MCP" (`shared/lib/hooks/useMcpVisibility.hooks.js`).
- Skills routes are guarded (`app/routes/SkillsGuard.jsx`); skill run needs predict.post plus skills.details or catalog.details (`features/skill/lib/hooks/useCanRunSkill.hooks.js`).
- Disabled-with-tooltip states exist (e.g. publish: `features/skill/ui/skill-row-action/DisabledPublishMenuItem.jsx`); read the tooltip text from code.
- Editing a whole assistant message is switched off in code (`ALLOW_EDIT_WHOLE_MESSAGE = false`, `features/chat/ui/chat-box/application-answer/ApplicationAnswer.jsx:23`).
- Recent churn (45 days, 706 commits): permissions on notifications, index writes hidden from viewers, Complexity menu, Participants panel; re-check these areas before documenting.

## Config & flags
- `window.elitea_ui_config.<key lowercase>` → overrides Vite env at runtime (`src/utils/env.js`)
- `allow_project_own_llms` (default true) → restricts own LLM settings in non-public projects (`src/common/constants.js:19`)
- `blocked_toolkits` (default []) → toolkit types blocked by org guardrails, warned in UI (`src/common/constants.js`)
- `VITE_PUBLIC_PROJECT_ID` → id of the public project; drives permission source and project type (`src/common/constants.js:63`, `.env.example`)
- `VITE_ELITEA_ASSISTANT` → shows the ELITEA assistant (`src/common/constants.js:20`)
- `VITE_VOICE_FEATURES_ENABLED` (default on) / `VITE_VOICE_FEATURES_TEMPORARILY_DISABLED` → voice features in chat (`src/common/constants.js`)
- `VITE_SERVER_URL`, `VITE_BASE_URI` (/elitea_ui), `VITE_SOCKET_SERVER`, `VITE_SOCKET_PATH` → API and socket endpoints; dev-only: `VITE_DEV_SERVER`, `VITE_DEV_TOKEN` (`.env.example`)
- `VITE_USE_NEW_IMPORT`, `VITE_USE_COLLECTION` → in `.env.example` only; effect not traced
- Platform settings (backend, via `useGetPlatformSettingsQuery`): analytics_enabled, cost_budgets_enabled, complexity_enabled, governance_enforced, mcp_exposure_enabled, mcp_in_menu_enabled, mcp_category_name (`src/api/platformSettings.js`)
- Mid-turn message injection → gated by `useIsMidturnInjectionEnabled` (`features/chat/lib/hooks/useMidturnInjection.hooks.js:29`)

unverified:
- Exact sidebar item labels and their per-permission visibility (`Sidebar.jsx`/`SidebarBody.jsx` not opened).
- Settings tab ids beyond those seen in `Settings.jsx` and `routes.js`.
- Doc-folder assignments are inferred from feature names, not from page contents.
- Whether features/auth and features/owner-consent map to getting-started/*.
- Effect of `VITE_USE_NEW_IMPORT` and `VITE_USE_COLLECTION`.
- Condition inside `useIsMidturnInjectionEnabled` (hook body not read).
- That "no i18n" is complete: confirmed by no i18n package in package.json and no useTranslation/i18n matches in `src/[fsd]`.

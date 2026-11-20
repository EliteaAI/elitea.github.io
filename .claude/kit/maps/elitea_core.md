---
repo: elitea_core
github: EliteaAI/elitea_core
branch: main
sha: 8cb174b5c
refreshed: 2026-11-17
---
## Lookup
- API v2 endpoints (one file per endpoint, routes in `url_params`, modes `prompt_lib` / `administration`) → `api/v2/<feature>.py` → `git grep -n "<term>" <ref> -- 'api/v2/*.py'`
- Permission checks (who may do what) → decorator `@auth.decorators.check_api({"permissions": [...]})` above each handler in `api/v2/*.py`; strings look like `models.chat.conversations.share` → `git grep -n "models\.[a-z_.]*" <ref> -- 'api/v2/*.py'`
- Extra access rules (not permission strings) → `utils/project_settings_access.py` (team-project settings: project admin OR owner of own private project), `utils/permissions.py`, `utils/folder_access.py`, `utils/schedule_access.py`, `utils/schedule_rights.py`, `utils/project_access.py`
- Platform config defaults and caps → `config.yml` (scheduler, schedules caps, `max_published_versions_per_agent`, predict prefetch) → `git show <ref>:config.yml`
- Chat upload limits (read from project vault secrets, defaults in code) → `api/v2/chat_config.py:19-26`, `utils/attachments.py:592`, `utils/conversation_import.py:108` → `git grep -n "chat_max" <ref>`
- Skill limits (admin config `skills.*`) → `utils/skill_utils.py:45-90` (`DEFAULT_*`, `get_max_*`)
- Code constants (limits, caps, TTL) → `git grep -n -E "^\s*(DEFAULT_|MAX_|_MAX|[A-Z_]*LIMIT)[A-Z_0-9]* *=" <ref> -- 'api/v2/*.py' 'utils/*.py' 'models/pd/*.py'`
- Platform/governance settings and defaults → `api/v2/platform_settings.py`, `api/v2/governance_settings.py`, `utils/governance_settings.py`, `utils/schedule_settings.py` → `git grep -n "<settings key>" <ref> -- 'api/v2' 'utils'`
- Request/response fields and enums (what the UI sends) → `models/pd/*.py`, `models/enums/*.py`
- Background jobs, reapers, budget/expiry tasks → `rpc/*.py`, `methods/*.py`
- Streaming chat/ASR/TTS/MCP sockets → `sio/*.py`; MCP server HTTP → `routes/mcp_sse.py`
- Feature docs written by developers (credential governance) → `docs/credential-governance/*.md`

## Features → modules + docs
- Chat attachments and upload limits: `GET chat_config` → `api/v2/chat_config.py`, `api/v2/attachments.py`, `utils/attachments.py` | docs: how-tos/chat/*, how-tos/chat-conversations/*, menus/settings/*
- Conversations, participants, summaries, canvas: `api/v2/conversation.py`, `conversations.py`, `participants.py`, `conversation_summaries.py`, `canvas.py`, `canvases.py`, `message.py` | docs: how-tos/chat/*, how-tos/chat-conversations/*
- Chat export / import: `api/v2/conversation_export.py`, `conversation_import.py`, `utils/conversation_import.py` | docs: how-tos/chat-conversations/*
- Chat sharing (share links, public view): `api/v2/shared_chat_link.py`, `shared_chat_links.py`, `shared_chat_view.py`, `shared_chat_view_unlock.py`, `shared_chat_attachment.py`, `models/pd/shared_chat_link.py` | docs: how-tos/chat-conversations/*
- Chat templates (project-level): `api/v2/chat_templates.py`, `chat_template_default.py` | docs: how-tos/chat/*
- Agents and versions: `api/v2/application.py`, `applications.py`, `version.py`, `versions.py`, `default_version.py`, `fork.py`, `folder.py`, `tags.py` | docs: how-tos/agents-pipelines/*, menus/*
- Publish / unpublish / public catalog: `api/v2/publish.py`, `unpublish.py`, `publish_validate.py`, `public_application.py`, `public_applications.py`, `admin_published_agents.py` | docs: how-tos/agents-pipelines/*, menus/*
- AI-assisted drafts (agent, pipeline, skill, eval dimensions, project context): `api/v2/generate_*_draft.py`, `enhance_from_eval.py`, `predict_llm.py` | docs: how-tos/agents-pipelines/*, how-tos/pipelines/*
- Pipelines (run, validate, nodes, triggers): `api/v2/pipeline_run.py`, `validate_pipeline.py`, `pipeline_trigger.py`, `configure_pipeline_node.py`, `utils/pipeline_validator.py` | docs: how-tos/pipelines/*, how-tos/pipelines/nodes/*
- Skills (CRUD, files, import/export, publish, limits): `api/v2/skill.py`, `skills.py`, `skill_files.py`, `skill_import.py`, `skill_export.py`, `skills_limits.py`, `publish_skill.py`, `public_skills.py`, `project_skills_settings.py` | docs: how-tos/entity-management/*, home/key-concepts/*, menus/*
- Toolkits and credentials: `api/v2/toolkits.py`, `toolkit_types.py`, `toolkit_validator.py`, `test_toolkit_tool.py`, `export_toolkit.py`, `fork_toolkit.py` | docs: how-tos/credentials-toolkits/*, integrations/toolkits/*
- MCP (exposed agents, OAuth proxy, tool sync): `api/v2/mcp_exposed_versions.py` (cap 200 agents), `mcp_oauth_proxy.py`, `mcp_dcr_proxy.py`, `mcp_sync_tools.py`, `routes/mcp_sse.py`, `utils/mcp_*.py` | docs: integrations/mcp/*
- Indexes (config, schedule, cancel, vectorstore): `api/v2/index_config.py`, `index_schedule.py`, `index_cancel.py`, `index_meta.py`, `vectorstore.py`, `utils/index_scheduling.py` | docs: how-tos/indexing/*
- Schedules (agents/pipelines/indexes, test runs, approvals): `api/v2/schedules.py`, `utils/schedule_*.py`, `utils/schedule_settings.py` | docs: how-tos/agents-pipelines/*, how-tos/indexing/*, menus/settings/*
- Webhooks (trigger a run from outside): `api/v2/webhook.py`, `utils/webhook_door.py`, `utils/webhook_secrets.py`, `webhook_trigger_schema.py` | docs: how-tos/pipelines/*, how-tos/agents-pipelines/*
- Budgets / usage limits and warnings: `api/v2/project_budget.py`, `project_budgets.py`, `user_budget.py`, `user_budgets.py`, `budget_warning.py`, `utils/budget_door.py`, `utils/budget_periods.py`, `rpc/budget_*.py` | docs: menus/settings/*, menus/*
- Analytics / usage / audit / traces: `api/v2/analytics.py`, `context_analytics.py`, `audit.py`, `audit_traces.py`, `audit_heatmap.py`, `project_user_activity.py`, `trending_authors.py` | docs: menus/*, menus/settings/*
- Evaluations (suites, datasets, runs, dimensions, scheduled auto-run): `api/v2/eval_*.py`, `utils/evaluation_*.py`, `utils/eval_auto_*.py` | docs: how-tos/agents-pipelines/*, menus/*
- Autonomous agents / mandates and agent identities: `api/v2/autonomous_mandates.py`, `agent_identities.py`, `utils/mandate_*.py` | docs: how-tos/agents-pipelines/*, home/key-concepts/*
- Credential governance (settings, inbox, requests, readiness): `api/v2/governance_*.py`, `utils/governance*.py`, `docs/credential-governance/*.md` | docs: menus/settings/*, how-tos/credentials-toolkits/*
- Platform settings (catalog "new" window, usage mode, complexity): `api/v2/platform_settings.py`, `project_info.py`, `project_icon.py` | docs: menus/settings/*
- Export/import of entities and wizard: `api/v2/export_import.py`, `import_wizard.py`, `utils/export_import*.py` | docs: how-tos/entity-management/*, migration/*
- Modules (internal tools) on the backend: `utils/internal_tools.py` | docs: how-tos/modules/*
- Web Search module (availability, admin-picked shared toolkit in the public project, injection into runs, USD/month budgets, limit messages): `utils/web_search.py`, `utils/tool_spend*.py`, `rpc/feature_budget_limits.py`, `admin_schema.json` (cost_budgets.features.web_search), `config.yml` | docs: how-tos/modules/*, menus/settings/*
- Predict (run agent), tools, memory-aware runs: `api/v2/predict.py`, `tools_call.py`, `tools_list.py`, `utils/predict_utils.py`, `utils/summarization.py` | docs: how-tos/chat/*, how-tos/agents-pipelines/*

## Doc-relevant gotchas
- Chat upload limits live in project vault secrets, not in code or config.yml; code gives only fallbacks (see Config & flags).
- Team-project settings: only project admins (roles `admin`, `super_admin`, `system`) or the owner of their own private project may change them (`utils/project_settings_access.py:10-12`, message "Project settings are managed by project admins").
- Public project id comes from config `ai_project_id` (default 1) and is cached 24 h in Redis (`utils/utils.py:54`; `config.yml`). Publishing sends agents to this public project.
- Published versions are capped per agent/skill: `max_published_versions_per_agent` / `_per_skill`, default 3 (`api/v2/publish.py:59`, `publish_skill.py:60`).
- Chat templates: at most 5 per project (`api/v2/chat_templates.py:12`).
- Share links expire in 7d (default) or 30d (`models/pd/shared_chat_link.py:12-45`); shared-view cookie lasts 3600 s (`api/v2/shared_chat_view.py:17`).
- Budgets endpoints differ by permission: project view `models.project_context.view`, admin `models.admin.project_budgets.view/edit` (`api/v2/project_budget.py:166,185,222`); budget usage windows are 4 months (`utils/budget_periods.py:10`).
- Webhook body cap 512 KB, dedup 24 h; run caps per webhook, per project, and waiting runs come from `config.yml` and a project may set a lower value (`utils/webhook_door.py:18-19`, `utils/schedule_settings.py:28`).
- Agent/skill attach limits: max 50 skills per agent, 5 invoked per turn, instruction text 50000 chars, skill package 30 MB / 10 MB per file / 500 files (`utils/skill_utils.py:45-50`); conversation starters max 4 (`utils/conversation_starters_utils.py:7`).
- Evaluation limits: case time 10 to 900 s, suite steps up to 100 (`models/pd/evaluation.py:46-50`); eval auto-run is off by default (`config.yml`).
- Recent changes may alter wording: index write needs index rights (EL-7450); forking a published agent includes attached pipelines (EL-7062); scheduled evaluation switch moved to Features -> Schedules (EL-6972).

## Config & flags
- `scheduler.schedules.min_interval_minutes: 5`, `max_enabled_per_project: 50`, `stale_run_minutes: 120`, `approval_wait_hours: 24`, `max_parallel_runs: 100` → schedule caps (`config.yml`)
- `webhook_max_concurrent_runs: 3`, `_limit: 20`, `webhook_project_max_concurrent_runs: 10`, `webhook_max_waiting_runs: 10` → webhook run caps (`config.yml`)
- `toolkit_index_min_interval_minutes: 1440` → shortest toolkit index schedule interval (`config.yml`)
- `scheduler.eval_auto_run.enabled: false` → environment-wide scheduled evaluation (`config.yml`)
- `skills.max_skills_per_agent / max_invoked_skills_per_turn / max_instructions_length / max_package_size_mb / max_file_size_mb / max_package_files` → admin overrides of skill limits (`utils/skill_utils.py:55-90`)
- `chat_max_upload_count` 10, `chat_max_upload_size_mb` 150, `chat_max_file_upload_size_mb` 150, `chat_max_image_upload_count` 10, `chat_max_image_upload_size_mb` 3, `chat_bucket_retention_days` 365 → project vault secrets with these code defaults (`api/v2/chat_config.py:21-25`, `utils/conversation_import.py:110-115`)
- `catalog_new_item_days` (default 14, max 60) → how long an agent/skill shows as new (`api/v2/platform_settings.py:21-23`)
- `platform_settings.budgets_mode`, `warning_dismissible`, `complexity_enabled` → usage mode and complexity display (`api/v2/platform_settings.py:57,109-123`)
- `ai_project_id` 1, `ai_project_allowed_domains`, `public_messages_route` → public project and messages (`config.yml`)
- `chat_history.tool_call_stubs.enabled/last_n: 3` → replay of recent tool calls (`config.yml`)
- `predict.subagent_prefetch` max_nodes 200, max_bytes 15 MB, max_seconds 40 → sub-agent expansion bounds (`config.yml`)
- `ELITEA_CREDENTIAL_GOVERNANCE_MAX_MODE` env and governance `context_ttl_s` (60 to 86400, default 3600) → governance mode and TTL (`utils/governance_settings.py:37,48-49`)
- `cancel_on_timeout: true` → stop worker when blocking predict times out (`config.yml`)

unverified:
- Which doc folder maps to each feature is inferred from the folder names only.
- Public/private/team project behavior is not mapped in detail: only `utils/project_settings_access.py` and the public project id were read; no project-type enum was found.
- `chat_bucket_retention_days` is used in `utils/conversation_import.py` only as read; where it deletes data (maybe `rpc/chunk_cleanup.py`) is not checked.
- Memory feature: no dedicated v2 endpoint found; "memory" appears only as a toolkit type (`api/v2/toolkit_names_migration.py:12`).
- Exact route paths (`/api/v2/elitea_core/<name>/...`) and the permission strings for schedules, webhooks, vectorstore and index schedule were not read.
- Whether `skills.*` keys sit under the plugin config in `config.yml` (not present in the default file) or only in the admin UI is not confirmed.
- Per-endpoint budget and eval permission strings beyond those listed were not read.

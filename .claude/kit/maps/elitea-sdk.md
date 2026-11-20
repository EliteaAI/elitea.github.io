---
repo: elitea-sdk
github: EliteaAI/elitea-sdk
branch: main
sha: e9d96aa7a
refreshed: 2026-11-17
---
## Lookup
Toolkit code is in `elitea_sdk/tools/<folder>/`. Credential models are in `elitea_sdk/configurations/<type>.py`.
- Toolkit page → code folder: take the toolkit name from the doc page, find its registration in `elitea_sdk/tools/__init__.py` (`_safe_import_tool('<type>', '<folder>', 'get_tools', '<Class>')`), then open `elitea_sdk/tools/<folder>/__init__.py` → `git grep -n "_safe_import_tool('<type>'" <ref> -- elitea_sdk/tools/__init__.py`
- Type id vs folder can differ: `service_now`→`servicenow`, `xray_cloud`→`xray`, `azure_search`→`azure_ai.search`, `sonar`→`code.sonar`, `bigquery`→`google.bigquery`, `delta_lake`→`aws.delta_lake`, `ado_repos`/`ado_plans`/`ado_boards`/`ado_wiki`→`ado/repos`, `ado/test_plan`, `ado/work_item`, `ado/wiki`, `aws|azure|gcp|k8s`→`cloud/*`
- Display name (UI card title) → `"label": "<Name>"` in `__config__=ConfigDict(json_schema_extra={'metadata': {...}})` at the end of `toolkit_config_schema()` in `elitea_sdk/tools/<folder>/__init__.py` (e.g. `tools/jira/__init__.py:153`, "Jira"). Same block holds `categories` and `hidden: True` → `git grep -n '"label":' <ref> -- 'elitea_sdk/tools/<folder>/*'`
- Toolkit settings (limit, api_version, labels, verify_ssl, ...) → `create_model(name, field=(type, Field(description=..., default=...)))` in `toolkit_config_schema()`. `description` is the UI help text; `default` is the default; no `default` (or `...`) = required → `git grep -n "Field(" <ref> -- elitea_sdk/tools/<folder>/__init__.py`
- Tools a toolkit exposes → `get_available_tools()` in `elitea_sdk/tools/<folder>/api_wrapper.py` (list of `{"name", "description", "args_schema", "ref"}`); `name` is the tool name users see; `args_schema` holds argument names, descriptions, defaults (Jira: `tools/jira/api_wrapper.py:2602`). Some toolkits keep schemas in `schemas.py` (github) → `git grep -n '"name": "' <ref> -- elitea_sdk/tools/<folder>/api_wrapper.py`
- Tool groups (read / write / delete / execute in the tool picker) → `with_tool_groups` / `tool_group` in `elitea_sdk/runtime/utils/tool_groups.py` (re-exported by `elitea_sdk/tools/utils/tool_groups.py`)
- Credential model of a toolkit → toolkit field `<x>_configuration=(<X>Configuration, Field(..., json_schema_extra={'configuration_types': ['<type>']}))`; class in `elitea_sdk/configurations/<type>.py`, registered in `elitea_sdk/configurations/__init__.py` (`_safe_import_configuration`) → `git grep -n "_safe_import_configuration" <ref> -- elitea_sdk/configurations/__init__.py`
- Credential fields, labels, secrets, required → in the Configuration class: `json_schema_extra` metadata (`label`, `type`, `section: "credentials"`, `sections.auth.subsections` = auth variants and their fields, e.g. Basic/Bearer in `configurations/jira.py:84`); `SecretStr` = secret; `Optional[...]`/`default=` = optional; `placeholder` in `json_schema_extra`; help text is `description=` (often a `_<NAME>_TOOLTIP` constant at the top of the file)
- Shared help texts (credentials selector, PgVector, embedding model) → `elitea_sdk/tools/common_tooltips.py`
- Indexing tools (index_data, list_indexes, search_index, stepback_search_index, stepback_summary_index, remove_index) → `elitea_sdk/tools/base_indexer_toolkit.py:3639-3674`; parameters, defaults, ranges (top_k 10, cut-off) → `elitea_sdk/tools/index_params.py`; variants `code_indexer_toolkit.py`, `non_code_indexer_toolkit.py`
- Chunking defaults (Markdown/text `max_tokens` 512; code `chunk_size` 1024, `token_chunk_size` 256) → `elitea_sdk/tools/chunkers/models.py:33-53`
- Base wrapper classes (shared tools, `get_available_tools`) → `elitea_sdk/tools/elitea_base.py`; architecture → `.elitea/agents/ELITEA_ARCHITECTURE.md`

Toolkit folders in `elitea_sdk/tools/`: ado advanced_jira_mining aha aws azure_ai bitbucket carrier cloud code confluence custom_open_api dataverse elastic figma github gitlab gitlab_org gmail google google_places jira keycloak localgit memory ms_graph openapi outlook pandas postman pptx qtest rally report_portal salesforce servicenow sharepoint slack sql tavily teams testio testrail xray yagmail zephyr zephyr_enterprise zephyr_essential zephyr_scale zephyr_squad (helpers, not toolkits: base, chunkers, llm, utils, vector_adapters).

Credential models in `elitea_sdk/configurations/`: ado aha azure_search bigquery bitbucket carrier confluence dataverse delta_lake embedding figma github gitlab google_places jira langfuse ms_graph openapi outlook pgvector postman qtest rally report_portal salesforce service_now sharepoint slack sonar sql tavily teams testio testrail xray zephyr zephyr_enterprise zephyr_essential (helpers: microsoft_graph_scopes, oauth_app_mode, utils).

## Features → modules + docs
Display names come from `"label"` (GitHub, GitLab, Jira, Confluence, Bitbucket, Outlook, PPTX, Memory, Carrier, Figma, Aha!, Postman, OpenAPI, Microsoft Graph, Dataverse (OneCRM), AzureDevOps, AdvancedJIRAmining; grep the rest).
- Code hosting (github, gitlab, gitlab_org, bitbucket, localgit hidden): `tools/github`, `tools/gitlab`, `tools/gitlab_org`, `tools/bitbucket`, `tools/localgit` | docs: integrations/toolkits/*, how-tos/credentials-toolkits/*, how-tos/indexing/*
- Work tracking (jira, confluence, advanced_jira_mining, aha, rally, service_now, salesforce, dataverse): matching folders (`servicenow` for service_now) | docs: integrations/toolkits/*, how-tos/credentials-toolkits/*
- Azure DevOps (ado, ado_repos, ado_plans, ado_boards, ado_wiki): `tools/ado/{repos,test_plan,work_item,wiki}` | docs: integrations/toolkits/*
- Test management (zephyr*, testrail, testio, qtest, xray_cloud, report_portal): `tools/zephyr*`, `tools/testrail`, `tools/testio`, `tools/qtest`, `tools/xray`, `tools/report_portal` | docs: integrations/toolkits/*
- Microsoft (sharepoint, outlook, teams, ms_graph): matching folders | docs: integrations/toolkits/*, how-tos/credentials-toolkits/*
- Other (slack, figma, postman, openapi, tavily, google_places, yagmail, sql, sonar, pptx, carrier, azure_search, bigquery, delta_lake, elastic, keycloak, cloud aws/azure/gcp/k8s): matching folders (sonar in `tools/code`, azure_search in `tools/azure_ai`, bigquery in `tools/google`, delta_lake in `tools/aws`) | docs: integrations/toolkits/*
- Platform toolkits (not in the tools registry): Artifact `runtime/toolkits/artifact.py`, Remote MCP `runtime/toolkits/mcp.py` (config `mcp_config.py`), Application (agent as tool) `runtime/toolkits/application.py`, VectorStore `runtime/toolkits/vectorstore.py` | docs: integrations/mcp/*, how-tos/modules/*, how-tos/agents-pipelines/*
- Indexing and search: `tools/base_indexer_toolkit.py`, `tools/index_params.py`, `tools/chunkers/*`, `runtime/langchain/indexer.py` | docs: how-tos/indexing/*
- Agent/pipeline engine (nodes, LLM, router, loop): `runtime/langchain/assistant.py`, `runtime/langchain/langraph_agent.py` | docs: how-tos/pipelines/*, how-tos/pipelines/nodes/*, how-tos/agents-pipelines/*
- Memory toolkit: `tools/memory` | docs: how-tos/modules/*
- Web Search module: Tavily toolkit `tools/tavily/` (tools, limits, domain filters, per-run cap; `CHAT_TOOLS` = web_search, web_extract only), module copy added in `runtime/toolkits/tools.py`, spend checks `tools/utils/metering.py` | docs: how-tos/modules/*, integrations/toolkits/*

## Doc-relevant gotchas
- Toolkit type id (registry key), folder name and display label are three different things; always read the label in `toolkit_config_schema()`.
- `hidden: True` means the toolkit is not offered in the UI (cloud aws/azure/gcp/k8s, elastic, keycloak, localgit, azure_search, delta_lake variants); check before documenting. Pandas is labelled "Pandas (Deprecated)"; its registration is commented out.
- `custom_open_api` registration is commented out; `openapi` is the active one.
- Fields move between credential and toolkit across releases (e.g. SharePoint Site URL moved from credential to toolkit; ADO, GitHub, Bitbucket, QTest project/repository became optional defaults a tool call may override). Check both `configurations/<x>.py` and `tools/<x>/__init__.py`.
- Jira: toolkit-level `cloud` wins when set, else derived from credential `hosting` (Auto/Cloud/Server); `api_version` Auto/2/3 (`tools/jira/__init__.py`).
- Many credentials have auth variants (Basic/Bearer/OAuth) under `sections.auth.subsections`; required fields differ per variant.
- Deployments can block toolkits/tools via env (`ELITEA_BLOCKED_TOOLKITS`, `ELITEA_BLOCKED_TOOLS`) and mark sensitive tools (`ELITEA_SENSITIVE_TOOLS`), so a tool in code may be missing for a user (`runtime/toolkits/security.py:214-249`; `_filter_blocked_tools` in `tools/__init__.py:249`).
- Tool descriptions sent to the model are cut to 1000 characters; `selected_tools` empty = all tools.
- Indexing tools exist only on toolkits built on the indexer base classes.

## Config & flags
- `selected_tools` (empty = all tools) → which tools the agent gets (`tools/<folder>/__init__.py`)
- `<x>_configuration` → linked credential (Project or Private); `configuration_types` ties it to the credential type (`tools/common_tooltips.py:4`)
- `pgvector_configuration`, `embedding_model` → required for indexing/search (`tools/common_tooltips.py:21,28`)
- Jira options: `limit` (default 5), `verify_ssl` (default True), `custom_headers`, `labels`, `additional_fields` (`tools/jira/__init__.py`)
- `ELITEA_BLOCKED_TOOLKITS`, `ELITEA_BLOCKED_TOOLS`, `ELITEA_SENSITIVE_TOOLS`, `ELITEA_SENSITIVE_ACTION_COMPANY_NAME`, `ELITEA_INPUT_GUARDRAIL` → hide or guard toolkits and tools (`runtime/toolkits/security.py`)
- Chunk size defaults → `tools/chunkers/models.py`

unverified:
- Full list of display labels (only a partial sample seen).
- Which toolkits are hidden beyond those seen in the label grep.
- Exact doc page-to-toolkit mapping per `integrations/toolkits/*` page (doc page names not inspected).
- Memory and Application toolkit behavior (folders exist, not read).
- Line numbers for `index_params.py` and `security.py` are approximate ranges from grep hits.

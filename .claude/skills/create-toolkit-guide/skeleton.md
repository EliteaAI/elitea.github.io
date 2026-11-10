# Toolkit guide skeleton

Derived from `outlook_toolkit.mdx` and `tavily_toolkit.mdx`. Keep section order and heading text; replace `[X]` / `[x]` (lowercase, for paths) with the product name; replace every `[...]` placeholder and drop `{/* */}` comments. Drop a section only if the toolkit has nothing for it (e.g. no external setup). Wording follows the style guide, not legacy pages ("Select", not "Click"); when copying a block from an existing page, fix its wording.

Depth (committed pages are about 500 lines):
- Each section opens with one explanatory sentence before steps ("Before creating a toolkit, create credentials...").
- Field tables: `Field | Required | Description`; add a `Default` column when 3 or more fields have defaults. Put ranges and limits in Description.
- Use-case sections: 3-5 sentences each with a concrete prompt, which tools run, and what the user gets back.
- Troubleshooting: always "Credential Not Appearing in Toolkit Configuration", plus one accordion per real error message from code.
- FAQ: 5 or more; cover required credential fields, whether the endpoint can change, costs/limits, error behavior, and toolkit-specific behavior (chat tools, MCP).

```mdx
---
title: "[X]"
description: "Connect ELITEA to [X] — [what agents can do, one sentence]."
---

---

## Introduction

[One paragraph: what this page covers and what the reader can do after it.]

**Brief Overview of [X]**

[2-3 sentences on the product, then a bullet list of capability groups, one bullet per tool group:]

*   **[Capability]:** [what tools in this group do].

## Toolkit's Account Setup & Configuration in [X]

### [Task in X, e.g. Generate an API Key]

1. ... (steps in the external product; final step gets `[x]-api-key.png` or similar vendor screenshot)

## System Integration with ELITEA

To integrate [X] with ELITEA, follow a three-step process: **Create Credentials → Create Toolkit → Use in Agents**.

### Step 1: Create [X] Credentials

1. **Go to Credentials Menu:** In the sidebar, select **[Credentials](../../menus/credentials)**.
2. **Create New Credential:** Select **`+ Credential`**.
3. **Select [X]:** Choose **[X]** as the credential type.

     ![[X] credential type selection.](../../img/integrations/toolkits/[x]/[x]-cred-navigate.png)

4. **Configure Credential Fields:** Complete the fields:

   | Field | Required | Description |
   |-------|----------|-------------|
   | **Display Name** | Required | ... |
   | **ID** | Required | Auto-populated from the Display Name |
   | ... every field from the credential model ... |

5. **Test Connection:** (only if the form has it) ...
6. **Save Credential:** Select **Save**.

     <img src="../../img/integrations/toolkits/[x]/[x]-cred-configs.png" alt="[X] credential form with fields completed." width="500"/>

<Tip title="Security Recommendation">
Store the [secret field] in **[Secrets](../../menus/settings/secrets)** and reference it in the credential instead of entering it directly.
</Tip>

### Step 2: Create [X] Toolkit

1. **Go to Toolkits Menu:** In the sidebar, select **[Toolkits & Indexes](../../menus/toolkits)**.
2. **Create New Toolkit:** Select **`+ Toolkit`**.
3. **Select [X]:** Choose **[X]** from the list of toolkit types.
4. **Configure Toolkit Details:** (table: Toolkit Name, Description, Credential, every toolkit config field)
5. **Enable Desired Tools:** In the **Tools** section, select the tools your agents use.
       * **Enable MCP access for selected tools**: (optional) exposes the selected tools through the platform MCP server.
6. **Save Toolkit:** Select **Save**.

{/* Add a Note or Warning here for policy or limit fields that change runtime behavior (caps, allow/block lists, spend limits). One block per behavior. */}

#### Available Tools:

[Intro sentence with the tool count.]

| **Category** | **Tool Name** | **Description** |
|---|---|---|
| **Read** | **[Tool label from UI]** | [from tool docstring/schema] |

#### Testing Toolkit Tools

[Standard test-panel steps; copy from outlook_toolkit.mdx "Testing Toolkit Tools" and fix wording.]

### Step 3: Add [X] Toolkit to Your Workflows

#### In Agents:
#### In Pipelines:
#### In Chat:

[Copy the standard three blocks from outlook_toolkit.mdx, replacing the name and image refs [x]-add-agent.png, [x]-add-pipeline.png, [x]-add-chat.png; fix wording.]

## Instructions & Prompts for Using the [X] Toolkit

### Instruction Creation for OpenAI Agents

<Info title="Example Agent Instructions">...</Info>

## [Use-case heading, infinitive or noun phrase] (2-4 of these, from real tool capabilities)

## Conversation Starters

### Chat Usage Examples by Tool Category

<Accordion title="[Category] - [Tool]"> chat example in a code block </Accordion>

---

## <Icon icon="triangle-exclamation" size={24} /> Troubleshooting

<Accordion title="[Problem]"> **Problem:** / **Cause:** / **Troubleshooting Steps:** — only errors that exist in code </Accordion>

### <Icon icon="envelope" size={24} /> Support Contact

[Copy from outlook_toolkit.mdx.]

---

## <Icon icon="circle-question" size={24} /> FAQ

<Accordion title="[Question]"> ... </Accordion>
```

---
name: skill-radar
description: "Auto-discovers relevant skills, MCP servers, and tools from external sources (GitHub, registries) for any task — presents them for approval. No auto-install."
version: 1.0.0
tags: ["discovery", "recommendation", "skills", "mcp", "tools"]
risk: safe
---

# Skill Radar 🔍

**Discover skills, MCP servers, and tools relevant to any task — from external sources, not just your installed library.**

## When to Use

Use this skill when:
- You want relevant skills/tools suggested for a task without knowing what exists
- You need to discover MCP servers or agent skills from the broader ecosystem
- You want a periodic scan for new/updated skills
- You want recommendations presented for approval (never auto-installed)

## How to Invoke

- `@skill-radar discover <task description>` — search for skills relevant to a task
- `@skill-radar cron-scan` — find new/updated skills not seen before

## What It Does

1. Extracts keywords from your task description
2. Searches across enabled sources:
   - **GitHub**: top agent skills, Claude Code skills, MCP servers, Hermes skills
   - **MCP Registries**: awesome-mcp-servers lists
   - **Custom sources** you've added
3. Scores results by:
   - Keyword relevance to your task
   - GitHub stars (community popularity)
   - Recency of updates
4. Groups results by category (MCP Server, Agent Skill, Tool, Plugin, etc.)
5. Presents them for your approval

**Skill Radar NEVER auto-installs.** Every recommendation includes the exact command to install, but you run it yourself.

## Example

```
@skill-radar discover "Build a real-time chat app with WebSockets"

→ Searches GitHub + MCP registries
→ Finds 8 relevant results
→ Groups them: MCP Servers (3), Tools (4), Agent Skills (1)
→ Shows each with description, stars, and install instructions
→ You pick what to install
```

## Periodic Discovery

For cron-based periodic scanning:
```
@skill-radar cron-scan
```

This does a broad sweep for skills not yet in your known list and presents new discoveries.

## CLI Tool

Skill Radar is also available as a standalone CLI tool:

```bash
skill-radar discover "Build a Next.js app"
skill-radar list-sources
skill-radar add-source my-source https://example.com/registry
```

Install from: https://github.com/DeezGit21/skill-radar
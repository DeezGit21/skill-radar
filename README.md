# Skill Radar 🔍

**Discover AI agent skills, MCP servers, and tools relevant to any task.**

Skill Radar automatically searches GitHub, MCP registries, and skill directories for skills/tools relevant to whatever you're working on, then **recommends them for your approval**. Never auto-installs — safety by design.

## Features

- 🔍 **Task-driven discovery**: Describe what you want to do → get ranked recommendations
- 📡 **Cron scan mode**: Periodic discovery of new skills (run on a schedule)
- 🏷️ **Smart categorization**: Groups results into MCP Servers, Agent Skills, Tools, Plugins
- ⭐ **Relevance scoring**: Scores by keyword match + GitHub stars + recency
- 🚫 **No auto-install**: Everything is presented for human approval
- 🔌 **Extensible sources**: Add custom registries, URLs, or GitHub search queries

## Quick Start

```bash
# Install
pip install -e .

# Search for skills relevant to your task
skill-radar discover "Build a Next.js SaaS with Stripe and Supabase"

# Cron-friendly periodic scan
skill-radar cron-scan

# Output as JSON (for programmatic use)
skill-radar discover "Set up CI/CD pipeline" --json

# Show install instructions for a specific result
skill-radar discover "MCP server for web search" --install "awesome-mcp-server"

# Manage sources
skill-radar list-sources
skill-radar add-source my-list https://my-tools.dev/registry
skill-radar remove-source outdated-source
```

## How It Works

1. **On demand** (`skill-radar discover "..."`): extracts keywords from your task, searches all enabled sources (GitHub, MCP registries, etc.), scores results by relevance + popularity, and presents them grouped by category
2. **Cron scan** (`skill-radar cron-scan`): broad sweep for new/updated skills not seen before — ideal for a weekly cron job
3. **Install is manual**: each recommendation shows the exact command to install, but you run it yourself

## Sources

Default sources (all enabled):

| Source | Type | What It Searches |
|--------|------|-----------------|
| GitHub: Top Agent Skills | `github_search` | Claude Code skills, agent skills, MCP servers |
| GitHub: Hermes Skills | `github_search` | Hermes agent skills |
| GitHub: MCP Servers | `github_search` | Model Context Protocol servers |
| GitHub: Cursor Rules | `github_search` | .cursorrules, CLAUDE.md, agent configs |

Add any custom source:
```bash
skill-radar add-source my-awesome-skills https://github.com/myorg/awesome-skills
```

## Integrations

### Hermes Agent (installed as a skill)
When loaded as a Hermes skill (via `@skill-radar`), Skill Radar automatically runs before every task, searches for relevant skills, and presents them. No manual invocation needed.

### Cron Job (periodic discovery)
```bash
# Every Monday at 9 AM
skill-radar cron-scan | while IFS= read -r line; do
  echo "$line"
done | mail -s "Skill Radar: New Discoveries" you@email.com
```

## Design Philosophy

- **Recommend, don't install** — the user stays in control
- **Transparent scoring** — each result shows why it was suggested
- **Broad then narrow** — cast a wide net, then rank by relevance
- **Privacy-respecting** — no telemetry, no data collection, runs locally

## License

MIT
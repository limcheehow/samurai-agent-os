# SamurAI Agent OS

A curated collection of **Agent Skills** for AI agents — following the [Agent Skills specification](https://agentskills.io). Drop them into any compliant agent (Hermes, OpenClaw, Claude Code, Cline, etc.) to extend their capabilities.

## Quick Start

```bash
# Option 1: Install skills individually
git clone https://github.com/limcheehow/samurai-agent-os.git ~/samurai-agent-os
ln -s ~/samurai-agent-os/skills/profile-enrichment ~/.hermes/skills/

# Option 2: Install the full Kizuna CRM plugin
hermes plugins install limcheehow/samurai-agent-os
hermes plugins enable kizuna-crm
```

## Skills

### [profile-enrichment](./skills/profile-enrichment/)

Enrich people and company profiles from emails, meetings, calendar events, and contact lists. Researches contacts via web search, LinkedIn, and Apollo.io — then writes structured profile files.

**Important prerequisites before using:**
- `web_search` / `web_extract` tools available in your agent
- [Jina AI Reader](https://jina.ai/reader) (optional, free) — for web_extract fallback
- Chrome with remote debugging (optional) — for LinkedIn scraping
- Apollo.io API key (optional) — for structured company/person data

```bash
# Install optional prerequisites
pip install ddgs  # DuckDuckGo search backend (free, no key)
```

---

## What are Agent Skills?

An **Agent Skill** is a standardized package that teaches an AI agent how to perform a specific task. Each skill is a directory containing:

```
skill-name/
├── SKILL.md       # YAML frontmatter + instructions the agent reads
├── scripts/       # Executable code the agent can run
├── references/    # Extra documentation
├── assets/        # Templates and resources
└── LICENSE        # License file
```

The `SKILL.md` file has two parts:
1. **YAML frontmatter** — metadata (name, description, license, compatibility)
2. **Markdown body** — instructions and workflows the agent follows

This format follows the open [Agent Skills specification](https://agentskills.io) originally developed at Anthropic and adopted by multiple agent platforms.

## Installing Skills

### On Hermes Agent

```bash
# Option A: Symlink the whole collection
ln -s ~/samurai-agent-os/skills/* ~/.hermes/skills/

# Option B: Copy specific skills
cp -r ~/samurai-agent-os/skills/profile-enrichment ~/.hermes/skills/

# Verify
hermes skill list | grep profile-enrichment
```

Skills take effect immediately — no restart required.

### On OpenClaw

Point your skill directory to the repo:

```bash
# In your agent config
SKILL_DIR: ~/samurai-agent-os/skills/

# Or add individual skills
SKILL_DIR: ~/samurai-agent-os/skills/profile-enrichment
```

### On Claude Code / Cline / Other Agents

Most agents discover skills by scanning a directory. Point them to any subdirectory of `skills/`:

```bash
# For agents that use CLAUDE.md or .cursorrules:
echo "SKILL_DIR: ~/samurai-agent-os/skills/profile-enrichment" >> CLAUDE.md
```

## Publishing Your Own Skills

This repo is designed to grow. To add a new skill:

1. **Follow the agentskills.io format:**

```
your-skill-name/
├── SKILL.md          # Required: frontmatter + instructions
├── scripts/          # Optional: Python, bash, or any executable
├── references/       # Optional: docs the agent should read
├── assets/           # Optional: templates, configs, resources
└── LICENSE           # Optional: license file
```

2. **SKILL.md must have:**
   - `name` field matching the directory name (lowercase, hyphens)
   - `description` field telling what the skill does (under 1024 chars)
   - Instructions: clear, step-by-step, with exact commands

3. **Submit via PR** to this repo, or open an issue to discuss.

## License

All skills in this repository are MIT licensed unless otherwise noted in their individual directories.

## About

Built for the SamurAI ecosystem — a collection of agent workflows designed for real business operations. Skills cover contact management, research, content creation, and business development workflows.
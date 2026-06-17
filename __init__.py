"""
samurai-agent-os — root plugin that registers the Kizuna CRM skills.
"""

from pathlib import Path


def register(ctx):
    plugin_dir = Path(__file__).parent
    skills_dir = plugin_dir / "plugins" / "kizuna-crm" / "skills"

    skill_mappings = [
        ("crm-assistant", skills_dir / "crm-assistant" / "SKILL.md"),
        ("client-meeting-prep", skills_dir / "client-meeting-prep" / "SKILL.md"),
        ("deal-project-activity-sync", skills_dir / "deal-project-activity-sync" / "SKILL.md"),
        ("domain-intel", skills_dir / "domain-intel" / "SKILL.md"),
    ]

    for name, path in skill_mappings:
        if path.exists():
            ctx.register_skill(name=name, path=path)
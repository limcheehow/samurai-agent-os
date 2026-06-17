"""
Kizuna CRM — Hermes plugin.
Registers 4 CRM skills and bundles the Kizuna persona definition.
"""

from pathlib import Path


def register(ctx):
    plugin_dir = Path(__file__).parent

    # Register bundled skills (namespaced as "plugin:kizuna-crm/<skill-name>")
    skills = [
        ("kizuna-crm/crm-assistant", str(plugin_dir / "skills" / "crm-assistant" / "SKILL.md")),
        ("kizuna-crm/client-meeting-prep", str(plugin_dir / "skills" / "client-meeting-prep" / "SKILL.md")),
        ("kizuna-crm/deal-project-activity-sync", str(plugin_dir / "skills" / "deal-project-activity-sync" / "SKILL.md")),
        ("kizuna-crm/domain-intel", str(plugin_dir / "skills" / "domain-intel" / "SKILL.md")),
    ]

    for name, path in skills:
        ctx.register_skill(name=name, path=path)

    # Reference: profile-enrichment skill available from samurai-agent-os/skills/
    # `hermes skills tap add https://github.com/limcheehow/samurai-agent-os`
    # Then: skill_view("profile-enrichment")
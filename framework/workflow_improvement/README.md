# ResearchFlow OS Self-Improvement System

`framework/workflow_improvement/` defines the long-term mechanism for letting Codex safely improve ResearchFlow OS while preserving `workflow1` CLI compatibility.

The system scans local skills, recipes, model registries, orchestration code, CLI stages, project state, Zotero/PDF/literature tooling, and run-package practices. It may search trusted open-source sources for design ideas, apply only low-risk local upgrades, and route high-risk plugins, MCP servers, API integrations, database writes, or dependency changes to an approval queue.

It does not install external code automatically and does not run formal models.

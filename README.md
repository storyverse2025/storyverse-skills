# storyverse-skills

Claude Code custom slash commands for creating AI short films with the [StoryVerse](https://github.com/storyverse2025) platform.

## What is this?

This repo contains 11 Claude Code skills (slash commands) that guide you through every step of AI short film production:

1. **Intake** — Capture your story idea
2. **Planning** — Configure project settings
3. **Script** — Generate screenplays
4. **Assets** — Create character and scene images
5. **Storyboard** — Generate keyframe images
6. **Shots** — Generate video clips
7. **Voice** — Transform character voices
8. **Consistency** — QA and fix AI-generated images
9. **Edit** — Assemble final video with subtitles and music
10. **Review** — Review and annotate the final cut
11. **Judge** — Evaluate quality and collect feedback for continuous improvement
12. **Pipeline** — Run the full workflow end-to-end

## Quick Start

```bash
# Clone this repo
git clone https://github.com/storyverse2025/storyverse-skills.git

# Symlink skills into your project
ln -s $(pwd)/storyverse-skills/.claude/commands/*.md /your/project/.claude/commands/

# In Claude Code, run any skill:
# /sv-intake A love story set in 1920s Shanghai...
# /sv-pipeline A sci-fi thriller about time travel...
```

## Prerequisites

- [Claude Code](https://claude.ai/claude-code) CLI
- [StoryVerse MCP Server](https://github.com/storyverse2025/storyverse_mcp) (for image/video generation)
- [StoryVerse Backend](https://github.com/storyverse2025/mvp_backend) (optional, for full API integration)

See [CLAUDE.md](./CLAUDE.md) for detailed setup instructions and **development principles** for working effectively with Claude Code.

## Project Structure

```
storyverse-skills/
├── CLAUDE.md                    # Setup and configuration guide
├── .claude/commands/            # Claude Code slash commands
│   ├── sv-intake.md             # /sv-intake
│   ├── sv-plan.md               # /sv-plan
│   ├── sv-script.md             # /sv-script
│   ├── sv-assets.md             # /sv-assets
│   ├── sv-storyboard.md         # /sv-storyboard
│   ├── sv-shots.md              # /sv-shots
│   ├── sv-voice.md              # /sv-voice
│   ├── sv-consistency.md        # /sv-consistency
│   ├── sv-edit.md               # /sv-edit
│   ├── sv-review.md             # /sv-review
│   ├── sv-judge.md              # /sv-judge
│   └── sv-pipeline.md           # /sv-pipeline
├── utils/                       # Python utilities
│   ├── __init__.py
│   └── langsmith_feedback.py    # LangSmith integration
├── docs/                        # Documentation
│   └── SELF_IMPROVEMENT.md      # Self-improvement system guide
├── context/                     # Shared reference documentation
│   ├── workflow-overview.md
│   ├── backend-api-reference.md
│   ├── mcp-tools-reference.md
│   └── conventions.md
└── examples/                    # Sample inputs
    ├── sample-inspiration.txt
    ├── sample-settings.json
    └── sample-voice-mapping.yaml
```

## Related Repos

| Repo | Description |
|------|-------------|
| [storyverse](https://github.com/storyverse2025/storyverse) | Core pipelines (voice, image consistency, edit) |
| [storyverse_mcp](https://github.com/storyverse2025/storyverse_mcp) | MCP server with 9 AI generation tools |
| [mvp_backend](https://github.com/storyverse2025/mvp_backend) | FastAPI backend |
| [mvp_frontend_ui](https://github.com/storyverse2025/mvp_frontend_ui) | Vanilla JS frontend |
| [frontend_ui](https://github.com/storyverse2025/frontend_ui) | React + TypeScript frontend |

## Features

### 🎯 Quality Judging & Self-Improvement

StoryVerse learns from your feedback to continuously improve content quality:

- **Quality Evaluation**: Rate AI-generated content across multiple dimensions
- **LangSmith Integration**: Log feedback to cloud datasets for analytics
- **Insights Generation**: Identify patterns and optimization opportunities
- **Continuous Learning**: System improves with each feedback cycle

```bash
# Judge content quality
/sv-judge all

# View insights
cat quality_insights.json
```

See [docs/SELF_IMPROVEMENT.md](docs/SELF_IMPROVEMENT.md) for details.

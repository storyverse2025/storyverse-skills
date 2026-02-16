# storyverse-skills

Claude Code custom slash commands for creating AI short films with the [StoryVerse](https://github.com/storyverse2025) platform.

## What is this?

This repo contains 14 Claude Code skills (slash commands) for production workflow, quality control, development tasks, and end-to-end orchestration:

1. **Intake** — Capture your story idea
2. **Planning** — Configure project settings
3. **Script** — Generate screenplays
4. **Assets** — Create character and scene images
5. **System Script** — Convert scripts + assets into beat-by-beat system script
6. **Storyboard** — Generate keyframe images
7. **Shots** — Generate video clips
8. **Voice** — Transform character voices
9. **Consistency** — QA and fix AI-generated images
10. **Edit** — Assemble final video with subtitles and music
11. **Review** — Review and annotate the final cut
12. **Judge** — Evaluate quality and collect feedback for continuous improvement
13. **Issue** — Handle GitHub issues end-to-end
14. **Pipeline** — Run the full workflow end-to-end

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

## Style Selection

Before generating visual assets, the system asks the user which visual style to use (2D Animation, 3D Animation, Live-Action Cinematic, Anime, or Stylized/Painterly). If the user doesn't specify, the system auto-selects the most appropriate style based on the project's genre and tone. The chosen style is stored in `project_settings.json` and applied to all downstream visual generation prompts.

## Script Generation: Two-Phase LangSmith Pipeline

`/sv-script` generates the script bible through two mandatory LangSmith agent phases using prompt templates in `langsmith-prompts/`:

### Phase 1: Episode Outline Agent (`langsmith-prompts/mvp_episode_outline.md`)

Splits source text into a structured episode outline:

1. **Extract Global Events** (E1...En) — in source order with evidence sentences
2. **Score Event Intensity** — Drama (1-5), Visual (1-5), Turn type per event
3. **Episode Splitting** — by drama density; high-intensity events get more space
4. **Output** — Main character table, global event list, intensity table, episode outline with: `cover_events`, `main_locations`, `characters_present`, `core_conflict`, `hook_type`, `hook_line`, `target_beats`, `source_text` (verbatim)

### Phase 2: Episode Script Agent (`langsmith-prompts/mvp_episode.md`)

Converts the episode outline into beat-level scripts:

1. **Source-Slice Binding** — each episode uses only its own `source_text` as facts
2. **Locked Line Extraction** — all source dialogue preserved verbatim in source order
3. **Beat Decomposition** — 8-12 beats per episode, each beat = 12 seconds, one key point + one location per beat
4. **Hard Rules** — 3-6 △ action lines per beat, 2-4 Audio lines per beat, no camera jargon, no event leakage between episodes
5. **Compliance Validation** — mandatory validator checks all beats before output

```
Source Text → Episode Outline Agent → Episode Script Agent → script_bible.json
                (Phase 1)                 (Phase 2)
```

## Project Structure

```
storyverse-skills/
├── CLAUDE.md                    # Setup and configuration guide
├── .claude/commands/            # Claude Code slash commands
│   ├── sv-intake.md             # /sv-intake
│   ├── sv-plan.md               # /sv-plan
│   ├── sv-script.md             # /sv-script
│   ├── sv-assets.md             # /sv-assets
│   ├── sv-system-script.md      # /sv-system-script
│   ├── sv-storyboard.md         # /sv-storyboard
│   ├── sv-shots.md              # /sv-shots
│   ├── sv-voice.md              # /sv-voice
│   ├── sv-consistency.md        # /sv-consistency
│   ├── sv-edit.md               # /sv-edit
│   ├── sv-review.md             # /sv-review
│   ├── sv-judge.md              # /sv-judge
│   ├── sv-issue.md              # /sv-issue
│   └── sv-pipeline.md           # /sv-pipeline
├── langsmith-prompts/           # LangSmith prompt templates (mandatory for script/storyboard/shots)
│   ├── mvp_episode_outline.md   # Phase 1: Episode Outline Agent
│   ├── mvp_episode.md           # Phase 2: Episode Script Agent
│   ├── mvp_casting.md           # Asset generation prompts
│   ├── mvp_system_script.md     # System script generation
│   ├── mvp_storyboard.md        # Keyframe generation prompts
│   ├── mvp_video_shot.md        # Video shot generation prompts
│   └── agents-archive/          # Archived prompts (anime, 3D, live-action, etc.)
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

## Keeping Docs Current

Use the manifest at `context/skills-manifest.json` as source of truth, then run:

```bash
python3 utils/check_skill_drift.py
```

This validates:
- command file set vs manifest
- unknown `/sv-*` references in markdown docs

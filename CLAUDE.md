# StoryVerse Skills

Claude Code custom slash commands for the StoryVerse AI short film creation platform. Each skill covers a distinct step in the filmmaking workflow, from story inspiration to final video review.

## Setup

### 1. Install Skills

Copy or symlink the commands into your project's `.claude/commands/` directory:

```bash
# Symlink (recommended for development)
ln -s /path/to/storyverse-skills/.claude/commands/*.md /your/project/.claude/commands/

# Or copy
cp /path/to/storyverse-skills/.claude/commands/*.md /your/project/.claude/commands/
```

### 2. Configure MCP Server

Add the StoryVerse MCP server to your Claude Code MCP settings for image/video generation tools:

```json
{
  "mcpServers": {
    "storyverse": {
      "url": "https://storyverse-ea52ee7d210d5d989df7aa66511a263c.us.langgraph.app/mcp",
      "headers": {
        "Authorization": "Bearer ${BEARER_TOKEN}"
      }
    }
  }
}
```

### 3. Required Environment Variables

| Variable | Required For | Description |
|----------|-------------|-------------|
| `FAL_KEY` | MCP tools | fal.ai API key for image/video generation |
| `BEARER_TOKEN` | MCP tools | MCP server authentication token |
| `STORYVERSE_BACKEND_URL` | Backend API | URL of the mvp_backend FastAPI server (default: `http://34.204.80.155/api/v1`) |
| `STORYVERSE_API_TOKEN` | Backend API | JWT token for backend authentication |
| `ELEVENLABS_API_KEY` | Voice, Edit | ElevenLabs API key (voice, STT, music) |
| `GEMINI_API_KEY` | Edit | Google Gemini API key (BGM analysis, transitions) |

### 4. Required Services

- **mvp_backend** running at `$STORYVERSE_BACKEND_URL` (for full API integration)
- **storyverse_mcp** running at `http://localhost:8000/mcp` (for image/video generation)

## Available Skills

| Command | Step | Description |
|---------|------|-------------|
| `/sv-intake` | 1 | Capture story inspiration from text, files, images |
| `/sv-plan` | 2 | Set project settings (language, episodes, aspect ratio) |
| `/sv-script` | 3 | Generate script bible with episode outlines and screenplays |
| `/sv-assets` | 4 | Generate character, scene, and prop images |
| `/sv-storyboard` | 5 | Generate keyframe images for each episode |
| `/sv-shots` | 6 | Generate video clips from keyframes |
| `/sv-voice` | 7 | Transform speaker voices in video clips |
| `/sv-consistency` | 8 | Detect and fix image consistency issues |
| `/sv-edit` | 9 | Edit pipeline: concat, subtitles, BGM, final compose |
| `/sv-review` | 10 | Review final video with timecode comments |
| `/sv-pipeline` | ALL | Full end-to-end orchestration of all steps |

## Workflow

```
/sv-intake → /sv-plan → /sv-script → /sv-assets → /sv-storyboard
    → /sv-shots → /sv-voice → /sv-consistency → /sv-edit → /sv-review
```

Steps are designed to run in sequence but can also run independently. Each skill reads/writes JSON state files in the working directory to pass data between steps.

## State Files

Each skill produces a JSON state file consumed by subsequent skills:

| File | Produced By | Consumed By |
|------|------------|-------------|
| `project_brief.json` | sv-intake | sv-plan, sv-script |
| `project_settings.json` | sv-plan | sv-script, sv-assets, sv-storyboard |
| `script_bible.json` | sv-script | sv-assets, sv-storyboard, sv-voice |
| `assets.json` | sv-assets | sv-storyboard |
| `storyboard.json` | sv-storyboard | sv-shots, sv-consistency |
| `shots.json` | sv-shots | sv-voice, sv-edit |
| `harmonized_shots.json` | sv-voice | sv-edit |
| `edit_output.json` | sv-edit | sv-review |
| `review_notes.json` | sv-review | — |
| `pipeline_state.json` | sv-pipeline | sv-pipeline (resume) |

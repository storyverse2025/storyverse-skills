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
      "url": "https://cdpx7nw32d.us-east-1.awsapprunner.com/mcp",
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
| `BEARER_TOKEN` | MCP tools | MCP server authentication token (default: `storyverse2026`) |
| `FAL_KEY` | Fallback | fal.ai API key for direct API calls when MCP server is unavailable |
| `STORYVERSE_BACKEND_URL` | Backend API | URL of the mvp_backend FastAPI server (default: `http://34.204.80.155/api/v1`) |
| `STORYVERSE_API_TOKEN` | Backend API | JWT token for backend authentication |
| `ELEVENLABS_API_KEY` | Voice, Edit | ElevenLabs API key (voice, STT, music) |
| `GEMINI_API_KEY` | Edit | Google Gemini API key (BGM analysis, transitions) |
| `LANGSMITH_API_KEY` | Quality/Judge | LangSmith API key for quality feedback logging |
| `LANGSMITH_PROJECT` | Quality/Judge | LangSmith project name (default: `storyverse-quality`) |

### 4. Required Services

- **mvp_backend** running at `$STORYVERSE_BACKEND_URL` (for full API integration)
- **storyverse_mcp** running at `https://cdpx7nw32d.us-east-1.awsapprunner.com/mcp` (for image/video generation)

### 5. Install Python Dependencies (Optional)

For quality feedback and self-improvement features:

```bash
pip install -r requirements.txt
```

This installs:
- `langsmith` - For logging quality feedback to LangSmith datasets
- `pandas`, `numpy` - For advanced analytics (optional)

## Available Skills

| Command | Step | Description |
|---------|------|-------------|
| `/sv-intake` | 1 | Capture story inspiration from text, files, images |
| `/sv-plan` | 2 | Set project settings (language, episodes, aspect ratio) |
| `/sv-script` | 3 | Generate script bible via Episode Outline Agent → Episode Script Agent (see LangSmith Prompts below) |
| `/sv-assets` | 4 | Generate character, scene, and prop images (casting) |
| `/sv-system-script` | 4.5 | Convert scripts + assets into beat-by-beat system script |
| `/sv-storyboard` | 5 | Generate adaptive multi-panel keyframe images (1/4/6/9 grids) |
| `/sv-shots` | 6 | Generate video clips from keyframes |
| `/sv-voice` | 7 | Transform speaker voices in video clips |
| `/sv-consistency` | 8 | Detect and fix image consistency issues |
| `/sv-edit` | 9 | Edit pipeline: concat, subtitles, BGM, final compose |
| `/sv-review` | 10 | Review final video with timecode comments |
| `/sv-judge` | QA | Judge AI-generated content quality and collect feedback |
| `/sv-issue` | DEV | Handle GitHub issue: analyze, clarify, implement, test, PR |
| `/sv-pipeline` | ALL | Full end-to-end orchestration of all steps |

## Workflow

```
/sv-intake → /sv-plan → /sv-script → /sv-assets → /sv-system-script
    → /sv-storyboard → /sv-shots → /sv-voice → /sv-consistency → /sv-edit → /sv-review
```

Steps are designed to run in sequence but can also run independently. Each skill reads/writes JSON state files in the working directory to pass data between steps.

## State Files

Each skill produces a JSON state file consumed by subsequent skills:

| File | Produced By | Consumed By |
|------|------------|-------------|
| `project_brief.json` | sv-intake | sv-plan, sv-script |
| `project_settings.json` | sv-plan | sv-script, sv-assets, sv-storyboard |
| `script_bible.json` | sv-script | sv-assets, sv-system-script, sv-voice |
| `assets.json` | sv-assets | sv-system-script, sv-storyboard, sv-judge |
| `system_script.json` | sv-system-script | sv-storyboard, sv-shots |
| `storyboard.json` | sv-storyboard | sv-shots, sv-consistency, sv-judge |
| `shots.json` | sv-shots | sv-voice, sv-edit, sv-judge |
| `harmonized_shots.json` | sv-voice | sv-edit, sv-judge |
| `edit_output.json` | sv-edit | sv-review |
| `review_notes.json` | sv-review | — |
| `quality_feedback.json` | sv-judge | — |
| `quality_insights.json` | sv-judge | — |
| `consistency_report.json` | sv-consistency | — |
| `pipeline_state.json` | sv-pipeline | sv-pipeline (resume) |

For complete JSON schemas with all fields, see `context/json-schemas.md`.

## JSON Schemas (PRD/Backend Aligned)

All JSON state files are aligned with the PRD and backend model schemas. Key enrichments include:

- **project_brief.json**: Added `title`, `suggested_settings` block for smart defaults
- **project_settings.json**: Added `project_id` (UUID), `status`, `current_step`, `created_at/updated_at` timestamps, nested `settings` object
- **script_bible.json**: Added `title`, `outline_beats` (6-beat structure), `script_elements` (structured screenplay), episode `title`/`summary`/`duration`/`status`
- **assets.json**: Characters get `persona` object, `look_references` with version tracking, `locked_look_id`; Scenes get `story_facts`, `visual_look`; Props get `appearances`
- **storyboard.json**: Added `id`, `prop_ids`, `versions` array for multi-generation tracking
- **shots.json**: Added `id`, `storyboard_frame_id`, `beat` structure with `segments` and `locks`, `versions` array
- **review_notes.json**: Added `id`, `x_position`/`y_position`, `linked_shot_id`, `author`, `status`, `overall_rating`

See `context/json-schemas.md` for the complete schema reference with field descriptions and types.

## Multi-Version Generation

Media-generating steps (assets, storyboard, shots, voice, edit) support multiple generation attempts with version tracking:

### Directory Structure
```
assets/characters/char_001_v1.png      # Version 1
assets/characters/char_001_v2.png      # Version 2
assets/characters/char_001_selected.png # Currently selected
```

### Version Tracking in JSON
- **Characters**: Use `look_references` array with `locked_look_id`
- **Other media**: Use `versions` array with `selected: true/false`
- `image_url`/`video_url` always points to the `_selected` file

### Convention
- Version files: `{id}_v{N}.{ext}` (never deleted)
- Selected files: `{id}_selected.{ext}` (copy of chosen version)
- First successful generation is selected by default
- Regeneration creates v2, v3, etc.

See `context/conventions.md` for full naming and versioning conventions.

## Git + Git LFS Management

Each project output folder is its own independent git repository with Git LFS for large media files.

### Auto-Initialization
- `sv-intake` (or `sv-pipeline`) initializes the repo: `git init`, `git lfs install`
- Creates `.gitattributes` for LFS tracking (video, audio, PSD files)
- Creates `.gitignore` for temp files

### Auto-Commit After Each Step
Every skill commits its output with a descriptive message:
```
step 1: sv-intake - capture project brief
step 4: sv-assets - generate 5 characters, 3 scenes, 2 props
step 4: sv-assets - regenerate char_001 v3
```

### LFS-Tracked File Types
`.mp4`, `.webm`, `.mov` (video), `.wav`, `.mp3`, `.flac` (audio), `.psd` (images)

See `context/git-management.md` for full git conventions, commit message format, and LFS configuration.

## Backend API Data Flow

When calling backend APIs, always **re-read the JSON state file** immediately before making the API call. This ensures that any external modifications the user made to JSON files (outside of Claude Code) are picked up and sent to the backend. The JSON file is the source of truth for each pipeline step.

## LangSmith Prompt Templates

The `langsmith-prompts/` directory contains mandatory prompt templates that define agent behavior for key pipeline steps. Skills **MUST** follow these templates — they are not optional guidelines.

### Script Generation: Two-Phase Agent Pipeline

`/sv-script` generates the script bible through two sequential agent phases:

#### Phase 1: Episode Outline Agent (`langsmith-prompts/mvp_episode_outline.md`)

Splits source text into a structured, paced episode outline:

1. **Extract Global Events** (E1...En) in source order with evidence sentences
2. **Score Event Intensity** — Drama score (1-5), Visual score (1-5), Turn type per event
3. **Episode Splitting Strategy** — high-intensity events (Drama+Visual ≥ 8) get more episodes/beats; low-intensity events get merged
4. **Output**: Main character table, global event list, intensity table, episode outline table with required fields: `episode_index`, `cover_events`, `main_locations`, `characters_present`, `core_conflict`, `hook_type`, `hook_line`, `target_beats`, `source_text` (verbatim from source)

Non-negotiable rules: event order matches source, episode slices are contiguous, every episode ends with a hook, `source_text` is verbatim, 8-12 beats per episode.

#### Phase 2: Episode Script Agent (`langsmith-prompts/mvp_episode.md`)

Converts the episode outline into beat-level performable scripts:

1. **Source-Slice Binding** — episode i uses only row i `source_text` as facts (no event leakage)
2. **Locked Line Extraction** — all source dialogue lines preserved verbatim, placed in source order
3. **Beat Decomposition** — one key point + one location per beat, 3-6 △ action lines, 2-4 Audio lines
4. **12-Second Beat Structure** — each beat has Setup → Turn → Button internal progression
5. **Hard Compliance Validation** — mandatory validator checks all beats before output (location, key point count, action line count, audio format, dialogue integrity)

```
Source Text → Episode Outline Agent → Episode Script Agent → script_bible.json
                 (Phase 1)                (Phase 2)
```

### Style Selection (User Preference)

Before generating any visual assets (characters, scenes, storyboards, video shots), the system **MUST** ask the user which visual style to use. This applies to `/sv-assets`, `/sv-storyboard`, and `/sv-shots`.

**Available styles:**
- **2D Animation** — flat illustration, anime-influenced, cel-shaded
- **3D Animation** — Pixar/CG-style, volumetric lighting, sculpted characters
- **Live-Action Cinematic** — photorealistic, film grain, natural lighting
- **Anime** — Japanese animation style, expressive eyes, dynamic poses
- **Stylized/Painterly** — digital painting, concept art, hand-crafted feel

**Workflow:**
1. During `/sv-plan` or `/sv-assets`, ask the user: "Which visual style would you like for this project?"
2. If the user does not respond or skips, auto-select the most appropriate style based on genre/tone:
   - Romance/Drama → Live-Action Cinematic
   - Fantasy/Xianni/Wuxia → 3D Animation or Anime
   - Comedy → 2D Animation
   - Sci-fi → 3D Animation
   - Horror → Live-Action Cinematic
3. Store the chosen style in `project_settings.json` under `settings.visual_style`
4. All downstream prompts must incorporate the selected style into their generation prompts

### Other LangSmith Prompt Templates

| Template | Used By | Purpose |
|----------|---------|---------|
| `mvp_casting.md` | `/sv-assets` | Character/scene/prop image generation with 4-bucket classification |
| `mvp_system_script.md` | `/sv-system-script` | Beat-level production directives with asset continuity |
| `mvp_storyboard.md` | `/sv-storyboard` | Keyframe image generation with multi-panel grids |
| `mvp_video_shot.md` | `/sv-shots` | Video shot generation with GOAL/SHOT_PLAN/DIALOGUE/EXPORT structure |

## Context Reference Files

| File | Description |
|------|-------------|
| `context/json-schemas.md` | Complete JSON schema reference for all pipeline outputs |
| `context/git-management.md` | Git/LFS initialization, commit conventions, directory structure |
| `context/conventions.md` | File naming, versioning, ID formats, path conventions |
| `context/workflow-overview.md` | Pipeline flow, step dependencies, directory structure |
| `context/mcp-tools-reference.md` | MCP tool signatures for image/video generation |
| `context/backend-api-reference.md` | Backend API endpoints and request formats |

---

## Development Principles & Best Practices

This section documents best practices for working with Claude Code in the StoryVerse project, based on learnings from the AI coding community.

### Core Coding Principles (Inspired by Andrej Karpathy)

#### 1. Think Before Coding
**Eliminate hidden confusion by making assumptions explicit**

- State your understanding of the task before writing code
- Present multiple interpretations when requirements are ambiguous
- Ask for clarification rather than making silent assumptions
- Example: "I understand you want X. Should I implement it as A or B?"

#### 2. Simplicity First
**Deliver minimum viable code—no speculative features**

- Write code that solves the immediate problem, nothing more
- Avoid single-use abstractions and unnecessary helper functions
- Skip error handling for scenarios that can't realistically happen
- Test: Would a senior engineer call this overcomplicated?
- Remember: Three similar lines > premature abstraction

#### 3. Surgical Changes
**Only modify what's necessary**

- Don't "improve" adjacent code you didn't need to touch
- Don't refactor working systems while fixing bugs
- Remove only the dead code your changes created
- Trust internal code and framework guarantees
- Validate only at system boundaries (user input, external APIs)

#### 4. Goal-Driven Execution
**Transform tasks into verifiable success criteria**

- Define explicit verification steps for each task
- Enable independent looping toward completion
- Provide success criteria rather than step-by-step instructions
- LLMs excel at iterating toward specific, measurable goals

### Working with Claude Code Effectively (Based on Boris Cherny's Tips)

#### Parallel Processing & Organization
- Run multiple Claude sessions simultaneously (3-5 instances)
- Use `git worktree` to isolate work across sessions
- Assign different tasks to different sessions for concurrent progress
- Example: One session for backend API, another for frontend UI

#### Planning Before Execution
- For complex work, dedicate a session to planning first
- Spend effort on a solid plan before implementation
- Use one session to review another session's plan
- Document the plan in the task or use `/sv-plan` for project planning

#### Documentation & Institutional Memory
- Maintain this `CLAUDE.md` as living documentation
- Capture project conventions, common mistakes, and corrections
- Add patterns you discover to `context/conventions.md`
- Prevents repeated errors across sessions
- Update when you learn something valuable

#### Automation of Repetitive Workflows
- Convert frequent tasks into reusable slash commands (`.claude/commands/`)
- Store skills in git for team sharing
- Examples in this repo: `/sv-intake`, `/sv-script`, etc.
- Create custom commands for project-specific workflows

#### Enhanced Prompting Techniques
- Challenge Claude to justify changes before implementing
- Request fresh rewrites if initial solution is mediocre
- Provide detailed specifications to improve autonomy
- Use examples from `examples/` folder as reference
- Be specific about constraints and requirements

#### Tool Integration
- Leverage MCPs (Model Context Protocols) for extended capabilities
- Use database CLIs and APIs for bug fixes and analytics
- StoryVerse MCP: 9 AI generation tools for image/video
- Backend API: Full CRUD operations for film projects

#### Learning Orientation
- Request explanatory output to understand decisions
- Ask for visual diagrams of complex workflows
- Use Claude to create documentation as you build
- Example: "Explain why you chose this architecture"

### Video Generation Principles (Adapted from Seedance2 Skill)

When working with AI video generation in StoryVerse:

#### Prompt Structure & Clarity
- Be explicit about camera movements, angles, and positioning
- Use structured templates for consistency (see `/sv-storyboard`, `/sv-shots`)
- Reference existing assets using clear identifiers
- Specify technical constraints upfront (aspect ratio, duration, style)

#### Input & Technical Guidelines
- Understand model capabilities and limitations
- Use the `@` notation for referencing characters/scenes
- Document parameters in JSON state files
- Maintain consistency across shots using asset references

#### Creative Framework
- Define camera language: shots, angles, movements
- Organize prompts by scene structure
- Use composition techniques from filmmaking
- Leverage templates for different content types (commercial, narrative, MV)

### Anti-Patterns to Avoid

❌ **Don't:** Make silent assumptions about requirements
✅ **Do:** Ask clarifying questions upfront

❌ **Don't:** Add features "for future extensibility"
✅ **Do:** Solve the current problem simply

❌ **Don't:** Refactor working code while adding features
✅ **Do:** Make surgical changes only

❌ **Don't:** Use `--no-verify` to bypass pre-commit hooks
✅ **Do:** Fix the underlying issue that caused the hook to fail

❌ **Don't:** Add error handling for impossible scenarios
✅ **Do:** Validate only at system boundaries

❌ **Don't:** Create helpers for one-time operations
✅ **Do:** Keep code inline until abstraction is clearly needed

### Success Criteria for Pull Requests

Before submitting code:

1. **Clarity**: Can another developer understand your changes?
2. **Simplicity**: Is this the simplest solution that works?
3. **Scope**: Did you only change what was necessary?
4. **Tests**: Do existing tests pass? Are new tests needed?
5. **Documentation**: Are new features documented?
6. **State Files**: Do JSON state files validate correctly?

### Resources

- [Andrej Karpathy Skills](https://github.com/forrestchang/andrej-karpathy-skills) - Core coding principles
- [Boris Cherny's Claude Code Tips](https://gist.github.com/joyrexus/e20ead11b3df4de46ab32b4a7269abe0) - Workflow optimization
- [Seedance2 Skill](https://github.com/dexhunter/seedance2-skill) - Video generation prompt guidelines

---

## Self-Improvement System

StoryVerse includes a self-improvement system that learns from user feedback to continuously improve content quality. See [docs/SELF_IMPROVEMENT.md](docs/SELF_IMPROVEMENT.md) for complete documentation.

### Quick Start

1. **Setup LangSmith** (get free API key at [smith.langchain.com](https://smith.langchain.com)):
   ```bash
   export LANGSMITH_API_KEY="your-api-key"
   export LANGSMITH_PROJECT="storyverse-quality"
   ```

2. **Judge content quality** after generation:
   ```bash
   /sv-judge assets      # Judge character/scene images
   /sv-judge storyboard  # Judge keyframes
   /sv-judge shots       # Judge video clips
   /sv-judge all         # Judge everything
   ```

3. **Review feedback and insights**:
   - `quality_feedback.json` - Detailed ratings and comments
   - `quality_insights.json` - Patterns and recommendations

4. **Apply improvements**:
   - Regenerate low-quality items
   - Update prompts based on insights
   - Switch to better-performing models

### How It Works

```
Generate → Judge → Log to LangSmith → Analyze → Improve → Repeat
   ↓         ↓            ↓              ↓          ↓
Assets   Ratings    Datasets       Insights   Better
Shots    Comments   Analytics      Patterns   Prompts
Script   Issues     Trends         Models     Results
```

### Benefits

- **Data-Driven**: Decisions based on real quality metrics
- **Continuous Learning**: System improves over time
- **Team Collaboration**: Share insights across team
- **Quality Tracking**: Monitor trends and improvements
- **Automated Optimization**: Identify best models and prompts

### Example Workflow

```bash
# 1. Generate content
/sv-assets

# 2. Judge quality
/sv-judge assets

# 3. Generate insights
python -c "from utils import QualityFeedbackLogger; \
           logger = QualityFeedbackLogger(); \
           logger.generate_insights('storyverse-assets')"

# 4. Apply recommendations from quality_insights.json

# 5. Regenerate improved content
/sv-assets  # with updated prompts

# 6. Re-judge to verify improvement
/sv-judge assets
```

See [docs/SELF_IMPROVEMENT.md](docs/SELF_IMPROVEMENT.md) for detailed documentation on:
- Quality evaluation framework
- LangSmith dataset structure
- Prompt optimization strategies
- Model selection criteria
- Analytics and metrics
- Advanced features

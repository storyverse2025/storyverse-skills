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
| `LANGSMITH_API_KEY` | Quality/Judge | LangSmith API key for quality feedback logging |
| `LANGSMITH_PROJECT` | Quality/Judge | LangSmith project name (default: `storyverse-quality`) |

### 4. Required Services

- **mvp_backend** running at `$STORYVERSE_BACKEND_URL` (for full API integration)
- **storyverse_mcp** running at `http://localhost:8000/mcp` (for image/video generation)

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
| `/sv-script` | 3 | Generate script bible with episode outlines and screenplays |
| `/sv-assets` | 4 | Generate character, scene, and prop images |
| `/sv-storyboard` | 5 | Generate keyframe images for each episode |
| `/sv-shots` | 6 | Generate video clips from keyframes |
| `/sv-voice` | 7 | Transform speaker voices in video clips |
| `/sv-consistency` | 8 | Detect and fix image consistency issues |
| `/sv-edit` | 9 | Edit pipeline: concat, subtitles, BGM, final compose |
| `/sv-review` | 10 | Review final video with timecode comments |
| `/sv-judge` | QA | Judge AI-generated content quality and collect feedback |
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
| `assets.json` | sv-assets | sv-storyboard, sv-judge |
| `storyboard.json` | sv-storyboard | sv-shots, sv-consistency, sv-judge |
| `shots.json` | sv-shots | sv-voice, sv-edit, sv-judge |
| `harmonized_shots.json` | sv-voice | sv-edit, sv-judge |
| `edit_output.json` | sv-edit | sv-review |
| `review_notes.json` | sv-review | — |
| `quality_feedback.json` | sv-judge | — |
| `quality_insights.json` | sv-judge | — |
| `pipeline_state.json` | sv-pipeline | sv-pipeline (resume) |

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

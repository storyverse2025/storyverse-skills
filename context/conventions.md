# StoryVerse Conventions

## Language Support

StoryVerse supports bilingual production:
- **Chinese (zh)**: Default for Chinese short drama market. UI labels, schema descriptions, and generated content use Chinese.
- **English (en)**: Full English support for international content.

The `language` field in project settings controls the script generation language.

## Aspect Ratio

| Aspect Ratio | Use Case | Resolution |
|-------------|----------|------------|
| `9:16` (Portrait) | Mobile-first, TikTok/Douyin, short drama apps | 720x1280, 1080x1920 |
| `16:9` (Landscape) | YouTube, desktop viewing, cinematic | 1280x720, 1920x1080 |

Default is `9:16` (portrait) for the Chinese short drama market.

When generating images/videos with MCP tools, always match the project's `aspect_ratio` setting.

## Target Channel

| Channel | Description | Content Style |
|---------|------------|---------------|
| `female` | Female audience (女频) | Romance, family drama, emotional |
| `male` | Male audience (男频) | Action, power fantasy, business |
| `general` | General audience | Mixed themes |

## Shot Types

Used for storyboard keyframes. Maps to camera framing:

| Shot Type | Chinese | Usage |
|-----------|---------|-------|
| `extreme_wide` | 大远景 | Establishing shots, landscapes |
| `wide` | 远景 | Full environment context |
| `full` | 全景 | Full body of characters |
| `medium_wide` | 中远景 | Characters in environment |
| `medium` | 中景 | Waist-up framing |
| `medium_close` | 中近景 | Chest-up framing |
| `close` | 近景 | Face and shoulders |
| `extreme_close` | 特写 | Detail shots, eyes, objects |

## Screenplay Format Elements

| Element | Description |
|---------|-------------|
| `scene-heading` | Location and time (INT./EXT.) |
| `action` | Visual description of action |
| `character` | Character name before dialogue |
| `parenthetical` | Acting direction in parentheses |
| `dialogue` | Spoken lines |
| `transition` | Scene transition (CUT TO, FADE OUT) |

## File Naming Conventions

### ID Formats

| Asset Type | ID Format | Example |
|-----------|-----------|---------|
| Character | `char_NNN` | `char_001`, `char_002` |
| Scene | `scene_NNN` | `scene_001`, `scene_002` |
| Prop | `prop_NNN` | `prop_001`, `prop_002` |
| Frame | `frame_NNN` | `frame_001`, `frame_002` |
| Shot | `shot_NNN` | `shot_001`, `shot_002` |
| Look | `look_NNN` | `look_001`, `look_002` |
| Note | `note_NNN` | `note_001`, `note_002` |

### Version Numbering

All generated media uses version suffixes:
- **Version format**: `_v{N}` where N starts at 1, increments per regeneration
- **Selected format**: `_selected` suffix for the currently chosen version
- Versions are **never deleted** — they accumulate as v1, v2, v3, etc.

### Versioned File Naming

| Asset Type | Pattern | Example |
|-----------|---------|---------|
| Character image | `{id}_v{N}.png` | `char_001_v1.png`, `char_001_v2.png` |
| Character selected | `{id}_selected.png` | `char_001_selected.png` |
| Scene image | `{id}_v{N}.png` | `scene_001_v1.png` |
| Prop image | `{id}_selected.png` | `prop_001_selected.png` |
| Storyboard frame | `{id}_v{N}.png` | `frame_001_v1.png` |
| Video shot | `{id}_v{N}.mp4` | `shot_001_v1.mp4` |
| Harmonized clip | `beat_{NNN}_v{N}.mp4` | `beat_001_v1.mp4` |
| Final video | `final_v{N}.mp4` | `final_v1.mp4` |

### Selected File Convention

The `_selected` file is a **copy** of the currently chosen version:
- When a new version is generated, save as `{id}_v{N}.{ext}`
- The first successful generation is selected by default
- Copy the selected version to `{id}_selected.{ext}`
- When user picks a different version, update the `_selected` copy
- JSON `image_url`/`video_url` fields always point to the `_selected` file

### Relative Path Convention

All file paths in JSON state files use **relative paths** from the project root:
- `assets/characters/char_001_selected.png` (correct)
- `/home/user/project/assets/characters/char_001_selected.png` (wrong — no absolute paths)
- `https://fal.ai/...` (wrong — no remote URLs in final JSON; download first)

When media is generated via MCP tools, the skill should:
1. Receive the remote URL from the tool
2. Download the file to the local versioned path
3. Store the **relative local path** in the JSON file

### Directory Structure

```
assets/
├── characters/        # Character reference images
├── scenes/            # Scene/location images
└── props/             # Prop images
storyboard/
└── episode_{N}/       # Keyframe images per episode
shots/
└── episode_{N}/       # Video clips per episode (LFS)
harmonized/
└── episode_{N}/       # Voice-harmonized clips (LFS)
output/
└── episode_{N}/       # Final edited videos (LFS)
```

## Character Roles

| Role | Chinese | Typical Count |
|------|---------|---------------|
| `protagonist_female` / `女主角` | 女主角 | 1 |
| `protagonist_male` / `男主角` | 男主角 | 1 |
| `supporting_female` / `女配角` | 女配角 | 1-3 |
| `supporting_male` / `男配角` | 男配角 | 1-3 |
| `antagonist` / `反派` | 反派 | 1-2 |
| `minor` / `路人` | 路人 | 0-5 |

## Episode Structure

Each episode follows a beat structure. The Chinese storytelling beats:
- 起 (Setup) - Establish the situation
- 因 (Cause) - Inciting incident
- 反 (Reversal) - Conflict and opposition
- 升 (Escalation) - Rising tension
- 爽 (Payoff) - Satisfying moment
- 合 (Resolution) - Wrap up

Typical episodes have 7-12 beats, each beat corresponding to one storyboard frame and one video shot.

## Prompt Engineering Tips

### Character Consistency
When generating images, always include:
1. Character name and role
2. Physical appearance description from character persona
3. Clothing/style consistent with the scene
4. Reference to existing character images when using I2I tools

### Storyboard Prompts
Structure prompts as:
```
[Shot type], [Scene description], [Character(s) and their action],
[Lighting/mood], [Style keywords]
```

### Video Motion Prompts
Structure I2V prompts as:
```
[Camera movement], [Character action/motion], [Environmental changes],
[Emotional tone]
```

## I2V Model Content Sensitivity & Fallback Priority

Different I2V models have different content moderation thresholds. When a model blocks content, fall back to a less restrictive model.

### Content-Sensitivity Order (most restrictive → least restrictive)

| Rank | Model | Content Strictness | Notes |
|------|-------|-------------------|-------|
| 1 (strictest) | `sora2_i2v` | Very strict | Blocks death, blood, violence, age references, and reference images with violent content |
| 2 | `kling_o3_pro_i2v` | Strict | Similar to Sora but slightly more permissive |
| 3 | `kling_o3_i2v` | Moderate | Handles most narrative content; may block extreme violence |
| 4 (most permissive) | `grok_imagine_i2v` | Permissive | Most lenient content policy; best fallback for censored content |

### Content Moderation Fallback Chain

When a shot fails due to content moderation, apply this 3-tier strategy (see `sv-shots` Step 6.2 for full details):

1. **Tier 1 — Prompt Sanitization**: Replace sensitive words using the I2V substitution table (same model)
2. **Tier 2 — Dialogue Stripping**: Remove dialogue from prompt; generate visual-only video (same model)
3. **Tier 3 — Model Switch**: Fall back to less restrictive model in the order above

### Default Fallback Chains by Starting Model

| Starting Model | Fallback Order |
|---|---|
| `sora2_i2v` | → `kling_o3_i2v` → `grok_imagine_i2v` |
| `kling_o3_i2v` | → `grok_imagine_i2v` → `kling_o3_pro_i2v` |
| `kling_o3_pro_i2v` | → `kling_o3_i2v` → `grok_imagine_i2v` |
| `grok_imagine_i2v` | → `kling_o3_i2v` → `kling_o3_pro_i2v` |

### Dialogue-Stripped Shots

When `dialogue_stripped: true`, the video was generated without dialogue in the I2V prompt. The original dialogue is preserved in the shot's `dialogue` field and must be added back via `/sv-voice` as a separate audio track.

## Backend API Data Flow

When calling backend APIs, always **re-read the JSON state file** immediately before making the API call. This ensures that any external modifications the user made to JSON files (outside of Claude Code) are picked up and sent to the backend. The JSON file is the source of truth for each pipeline step.

Pattern:
1. Read the current JSON state file
2. Use its contents to construct the API request body
3. Make the API call
4. Update the JSON file with any response data (e.g., IDs, URLs)

---

## Development Best Practices

For comprehensive development principles and best practices when working with Claude Code on this project, see the **Development Principles & Best Practices** section in [CLAUDE.md](../CLAUDE.md).

Key principles include:
- **Think Before Coding**: Make assumptions explicit, ask rather than guess
- **Simplicity First**: Minimum viable code, no speculative features
- **Surgical Changes**: Only modify what's necessary
- **Goal-Driven Execution**: Define clear success criteria
- **Parallel Processing**: Run multiple Claude sessions for complex work
- **Documentation**: Maintain institutional memory in this file and CLAUDE.md

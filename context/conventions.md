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

### Generated Assets
- Characters: `bc_{character_name_pinyin}.png` (e.g., `bc_fu_si_nian.png`)
- Scenes: `scene_{scene_id}.png`
- Props: `prop_{prop_id}.png`

### Storyboard Frames
- `beat_{NNN}.png` (e.g., `beat_001.png`, `beat_002.png`)

### Video Shots
- `beat_{NNN}.mp4` (e.g., `beat_001.mp4`, `beat_002.mp4`)

### Edit Pipeline Output
- `merged.mp4` - Concatenated video
- `subtitles.srt` / `subtitles.ass` - Subtitle files
- `bgm.wav` - Background music
- `final.mp4` - Final composed video

## Character Roles

| Role | Chinese | Typical Count |
|------|---------|---------------|
| `protagonist_female` | 女主角 | 1 |
| `protagonist_male` | 男主角 | 1 |
| `supporting_female` | 女配角 | 1-3 |
| `supporting_male` | 男配角 | 1-3 |
| `antagonist` | 反派 | 1-2 |
| `minor` | 路人 | 0-5 |

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

# StoryVerse JSON Schemas Reference

Central reference for all JSON output schemas used in the StoryVerse pipeline. Each skill produces a JSON state file that downstream skills consume.

For backend model alignment, see `/home/ubuntu/repos/mvp_backend/app/schemas/`.

---

## Step 1: project_brief.json (sv-intake)

```json
{
  "title": "项目标题",
  "inspiration": "故事灵感描述",
  "file_summaries": [
    {"filename": "ref.pdf", "summary": "Summary of file contents"}
  ],
  "genre": "romance",
  "tone": "dramatic",
  "themes": ["love", "betrayal"],
  "visual_style": "cinematic, warm tones",
  "target_audience": "young adults",
  "key_characters": [
    {"name": "林小夏", "description": "24岁咖啡店店员", "role": "女主角"}
  ],
  "setting": "Modern Shanghai",
  "language_preference": "zh",
  "suggested_episode_count": 10,
  "suggested_settings": {
    "target_channel": "female",
    "language": "zh",
    "episode_count": 10,
    "episode_duration": 90,
    "aspect_ratio": "9:16"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | yes | Project title derived from inspiration |
| `inspiration` | string | yes | Original inspiration text |
| `file_summaries` | array | no | Summaries of uploaded reference files |
| `genre` | string | yes | One of: romance, thriller, sci-fi, drama, comedy, horror, fantasy, action |
| `tone` | string | yes | dramatic, lighthearted, dark, suspenseful, romantic, etc. |
| `themes` | string[] | yes | Key thematic elements |
| `visual_style` | string | yes | Visual style description for image generation |
| `target_audience` | string | yes | young adults, general, female-oriented, male-oriented |
| `key_characters` | array | yes | Characters with name, description, role |
| `setting` | string | yes | Time period, location, world details |
| `language_preference` | string | yes | "zh" or "en" |
| `suggested_episode_count` | integer | yes | Recommended number of episodes |
| `suggested_settings` | object | no | Pre-filled settings for sv-plan based on analysis |

---

## Step 2: project_settings.json (sv-plan)

```json
{
  "project_id": "uuid-generated",
  "title": "霸道总裁爱上我",
  "inspiration": "故事灵感描述",
  "settings": {
    "target_channel": "female",
    "language": "zh",
    "episode_count": 10,
    "episode_duration": 90,
    "aspect_ratio": "9:16",
    "visual_style": "mvp",
    "video_purpose": "story",
    "style_playbook_id": "roar_of_steel"
  },
  "status": "draft",
  "current_step": 2,
  "created_at": "2026-02-14T10:00:00Z",
  "updated_at": "2026-02-14T10:00:00Z"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `project_id` | string (UUID) | yes | Unique project identifier |
| `title` | string | yes | Project title (1-200 chars) |
| `inspiration` | string | yes | Carried forward from brief |
| `settings.target_channel` | string | yes | "female", "male", or "general" |
| `settings.language` | string | yes | "zh" or "en" |
| `settings.episode_count` | integer | yes | 1-100 |
| `settings.episode_duration` | integer | yes | Seconds per episode |
| `settings.aspect_ratio` | string | yes | "9:16" or "16:9" |
| `settings.visual_style` | string | no | "mvp", "threed", "liveaction", "anime". Default "mvp" |
| `settings.video_purpose` | string | no | "story", "commercial", "musicvideo", "educational". Default "story" |
| `settings.style_playbook_id` | string | no | ID of a style playbook YAML file from `style_playbooks/` (e.g., "roar_of_steel"). When set, sv-shots and sv-system-script inject the playbook's cinematic style constraints into prompt generation. |
| `status` | string | yes | "draft", "in_progress", "completed" |
| `current_step` | integer | yes | Current pipeline step number |
| `created_at` | string (ISO) | yes | Creation timestamp |
| `updated_at` | string (ISO) | yes | Last update timestamp |

---

## Step 3: script_bible.json (sv-script)

```json
{
  "title": "霸道总裁爱上我",
  "logline": "一句话故事概要",
  "outline_beats": [
    {"id": 1, "label": "起", "description": "相遇冲突"},
    {"id": 2, "label": "因", "description": "被迫同处"},
    {"id": 3, "label": "反", "description": "误会加深"},
    {"id": 4, "label": "升", "description": "情感萌芽"},
    {"id": 5, "label": "爽", "description": "高能时刻"},
    {"id": 6, "label": "合", "description": "情感确认"}
  ],
  "episodes": [
    {
      "episode_number": 1,
      "title": "咖啡洒了",
      "summary": "剧情概要",
      "duration": 90,
      "status": "completed",
      "core_conflict": "Central tension of this episode",
      "script_elements": [
        {"type": "scene-heading", "content": "第一场 内景 咖啡店 - 日"},
        {"type": "action", "content": "林小夏端着咖啡走过来"},
        {"type": "character", "content": "林小夏"},
        {"type": "dialogue", "content": "千万别洒..."}
      ],
      "content": "Full screenplay text with beat markers..."
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | yes | Story title |
| `logline` | string | yes | One-sentence story summary |
| `outline_beats` | array | yes | 6-beat story structure template |
| `outline_beats[].id` | integer | yes | Beat sequence number |
| `outline_beats[].label` | string | yes | Beat label (起/因/反/升/爽/合) |
| `outline_beats[].description` | string | yes | What happens in this beat arc |
| `episodes[].episode_number` | integer | yes | Sequential episode number (1-based) |
| `episodes[].title` | string | yes | Episode title |
| `episodes[].summary` | string | yes | Brief episode synopsis |
| `episodes[].duration` | integer | yes | Target duration in seconds |
| `episodes[].status` | string | yes | "draft", "completed", "needs_revision" |
| `episodes[].core_conflict` | string | yes | Central tension (1-2 sentences) |
| `episodes[].script_elements` | array | yes | Structured screenplay elements |
| `episodes[].script_elements[].type` | string | yes | scene-heading, action, character, parenthetical, dialogue, transition |
| `episodes[].script_elements[].content` | string | yes | Element text content |
| `episodes[].content` | string | yes | Full screenplay text with beat markers |

---

## Step 4: assets.json (sv-assets)

```json
{
  "characters": [
    {
      "id": "char_001",
      "name": "林小夏",
      "role": "女主角",
      "age": 24,
      "occupation": "咖啡店店员",
      "persona": {
        "appearance": "清纯甜美，马尾辫",
        "personality": "善良倔强",
        "weakness": "容易心软",
        "specialty": "制作咖啡"
      },
      "prompt": "AI generation prompt",
      "image_url": "assets/characters/char_001_selected.png",
      "look_references": [
        {"id": "look_001", "image_url": "assets/characters/char_001_v1.png", "is_locked": false, "prompt": "..."},
        {"id": "look_002", "image_url": "assets/characters/char_001_v2.png", "is_locked": true, "prompt": "..."}
      ],
      "locked_look_id": "look_002",
      "first_episode": 1
    }
  ],
  "scenes": [
    {
      "id": "scene_001",
      "name": "咖啡店内景",
      "story_facts": {
        "location": "城市咖啡店",
        "time": "日",
        "event": "女主工作场景"
      },
      "visual_look": {
        "material": "木质温馨",
        "lighting": "暖黄色调",
        "era": "现代都市",
        "mood": "温馨"
      },
      "prompt": "AI generation prompt",
      "image_url": "assets/scenes/scene_001_selected.png",
      "locked_facts": true
    }
  ],
  "props": [
    {
      "id": "prop_001",
      "name": "咖啡杯",
      "description": "精美的陶瓷咖啡杯",
      "prompt": "AI generation prompt",
      "image_url": "assets/props/prop_001_selected.png",
      "appearances": [
        {"episode_number": 1, "scene_number": 1, "shot_number": 3}
      ]
    }
  ]
}
```

### Character Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique ID (char_NNN format) |
| `name` | string | yes | Character name |
| `role` | string | yes | 女主角, 男主角, 女配角, 男配角, 反派, 路人 |
| `age` | integer | no | Character age |
| `occupation` | string | no | Character occupation |
| `persona` | object | yes | Character personality profile |
| `persona.appearance` | string | yes | Physical appearance description |
| `persona.personality` | string | yes | Personality traits |
| `persona.weakness` | string | no | Character weakness |
| `persona.specialty` | string | no | Character specialty |
| `prompt` | string | yes | Prompt used for current selected image |
| `image_url` | string | yes | Relative path to selected image |
| `look_references` | array | yes | All generated versions |
| `look_references[].id` | string | yes | Version ID (look_NNN) |
| `look_references[].image_url` | string | yes | Relative path to version image |
| `look_references[].is_locked` | boolean | yes | Whether this look is locked/selected |
| `look_references[].prompt` | string | yes | Prompt used for this version |
| `locked_look_id` | string | no | ID of the locked/selected look |
| `first_episode` | integer | yes | First episode this character appears in |

### Scene Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique ID (scene_NNN format) |
| `name` | string | yes | Scene/location name |
| `story_facts` | object | yes | Narrative context for this scene |
| `story_facts.location` | string | yes | Location description |
| `story_facts.time` | string | yes | Time of day (日/夜/晨/昏) |
| `story_facts.event` | string | yes | What happens here narratively |
| `visual_look` | object | yes | Visual style parameters |
| `visual_look.material` | string | yes | Material/texture description |
| `visual_look.lighting` | string | yes | Lighting description |
| `visual_look.era` | string | yes | Time period / style era |
| `visual_look.mood` | string | yes | Emotional mood |
| `prompt` | string | yes | AI generation prompt |
| `image_url` | string | yes | Relative path to selected image |
| `locked_facts` | boolean | no | Whether story facts are finalized |

### Prop Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique ID (prop_NNN format) |
| `name` | string | yes | Prop name |
| `description` | string | yes | Prop description |
| `prompt` | string | yes | AI generation prompt |
| `image_url` | string | yes | Relative path to selected image |
| `appearances` | array | no | Where this prop appears in the story |

---

## Step 5: storyboard.json (sv-storyboard)

```json
{
  "episodes": [
    {
      "episode_number": 1,
      "frames": [
        {
          "id": "frame_001",
          "frame_number": 1,
          "beat_number": 1,
          "summary": "林小夏端着咖啡穿过大堂",
          "shot_type": "wide",
          "dialogue": {
            "character_name": "林小夏",
            "text": "千万别洒...",
            "emotion": "nervous"
          },
          "character_ids": ["char_001"],
          "scene_id": "scene_001",
          "prop_ids": ["prop_001"],
          "prompt": "AI generation prompt",
          "image_url": "storyboard/episode_1/frame_001_selected.png",
          "versions": [
            {"version": 1, "image_url": "storyboard/episode_1/frame_001_v1.png", "prompt": "...", "selected": false},
            {"version": 2, "image_url": "storyboard/episode_1/frame_001_v2.png", "prompt": "...", "selected": true}
          ]
        }
      ]
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `episodes[].episode_number` | integer | yes | Episode number (1-based) |
| `frames[].id` | string | yes | Unique frame ID (frame_NNN) |
| `frames[].frame_number` | integer | yes | Sequential frame number within episode |
| `frames[].beat_number` | integer | yes | Corresponding beat number |
| `frames[].summary` | string | yes | Visual description of the frame |
| `frames[].shot_type` | string | yes | Camera shot type (see conventions.md) |
| `frames[].dialogue` | object | no | Dialogue in this frame |
| `frames[].dialogue.character_name` | string | yes | Speaking character |
| `frames[].dialogue.text` | string | yes | Dialogue text |
| `frames[].dialogue.emotion` | string | yes | Emotional delivery |
| `frames[].character_ids` | string[] | yes | Character IDs present in frame |
| `frames[].scene_id` | string | yes | Scene/location ID |
| `frames[].prop_ids` | string[] | no | Prop IDs visible in frame |
| `frames[].prompt` | string | yes | Generation prompt for selected version |
| `frames[].image_url` | string | yes | Relative path to selected image |
| `frames[].versions` | array | no | All generated versions |

---

## Step 6: shots.json (sv-shots)

```json
{
  "episodes": [
    {
      "episode_number": 1,
      "shots": [
        {
          "id": "shot_001",
          "shot_number": 1,
          "beat_number": 1,
          "description": "林小夏端着咖啡穿过大堂",
          "dialogue": "千万别洒...",
          "duration": 5,
          "storyboard_frame_id": "frame_001",
          "character_ids": ["char_001"],
          "scene_id": "scene_001",
          "beat": {
            "segments": [
              {"time_range": "0-2s", "action": "林小夏端着咖啡", "locked": false},
              {"time_range": "2-5s", "action": "穿过大堂", "locked": false}
            ],
            "locks": {"character": true, "scene": true, "style": false}
          },
          "prompt": "AI generation prompt",
          "video_url": "shots/episode_1/shot_001_selected.mp4",
          "image_url": "storyboard/episode_1/frame_001_selected.png",
          "status": "completed",
          "failure_reason": null,
          "tool_used": "kling_o3_i2v",
          "dialogue_stripped": false,
          "quality_score": null,
          "quality_issues": [],
          "versions": [
            {
              "version": 1,
              "video_url": "shots/episode_1/shot_001_v1.mp4",
              "prompt": "...",
              "tool_used": "kling_o3_i2v",
              "dialogue_stripped": false,
              "fallback_attempts": [],
              "quality_score": null,
              "quality_issues": [],
              "selected": true
            }
          ]
        }
      ]
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `shots[].id` | string | yes | Unique shot ID (shot_NNN) |
| `shots[].shot_number` | integer | yes | Sequential shot number |
| `shots[].beat_number` | integer | yes | Corresponding beat number |
| `shots[].description` | string | yes | Visual description |
| `shots[].dialogue` | string | no | Dialogue text |
| `shots[].duration` | integer | yes | Duration in seconds |
| `shots[].storyboard_frame_id` | string | yes | Link to source storyboard frame |
| `shots[].character_ids` | string[] | yes | Character IDs in this shot |
| `shots[].scene_id` | string | yes | Scene/location ID |
| `shots[].beat` | object | no | Beat structure with segments |
| `shots[].beat.segments` | array | no | Time-based action segments |
| `shots[].beat.locks` | object | no | Lock status for character/scene/style |
| `shots[].prompt` | string | yes | Motion/generation prompt |
| `shots[].video_url` | string | yes | Relative path to selected video |
| `shots[].image_url` | string | yes | Relative path to source keyframe |
| `shots[].status` | string | yes | "completed", "failed", "pending" |
| `shots[].failure_reason` | string | no | `null` (success), `"content_moderation"`, `"quality"`, or `"api_error"` — classifies failure type |
| `shots[].tool_used` | string | yes | I2V tool used for generation |
| `shots[].dialogue_stripped` | boolean | no | `true` if dialogue was removed from prompt due to content moderation — dialogue preserved in `dialogue` field for `/sv-voice` |
| `shots[].quality_score` | float | no | Average quality score (1.0-5.0), populated by `/sv-eval` |
| `shots[].quality_issues` | string[] | no | Identified quality issues |
| `shots[].versions` | array | no | All generated versions |
| `shots[].versions[].dialogue_stripped` | boolean | no | `true` if this version was generated without dialogue in prompt |
| `shots[].versions[].fallback_attempts` | array | no | Array of `{tier, strategy, model, result, error}` tracking content moderation fallback |
| `shots[].versions[].quality_score` | float | no | Quality score for this version |
| `shots[].versions[].quality_issues` | string[] | no | Quality issues for this version |

---

## Step 7: harmonized_shots.json (sv-voice)

```json
{
  "voice_mapping": {
    "林小夏": {"voice_id": "...", "description": "Young female, warm, gentle"}
  },
  "episodes": [
    {
      "episode_number": 1,
      "shots": [
        {
          "beat_number": 1,
          "original_video_url": "shots/episode_1/shot_001_selected.mp4",
          "harmonized_video_url": "harmonized/episode_1/beat_001_selected.mp4",
          "dialogue": "千万别洒...",
          "speaking_character": "林小夏",
          "voice_mapping": {"林小夏": "voice_id_1"},
          "versions": [
            {"version": 1, "video_url": "harmonized/episode_1/beat_001_v1.mp4", "selected": true}
          ]
        }
      ]
    }
  ]
}
```

---

## Step 8: consistency_report.json (sv-consistency)

```json
{
  "episodes": [
    {
      "episode_number": 1,
      "results": [
        {
          "frame_number": 1,
          "beat_number": 1,
          "status": "PASS",
          "issues": [],
          "action": "none"
        },
        {
          "frame_number": 2,
          "beat_number": 2,
          "status": "FAIL",
          "issues": ["Extra person in background", "Wrong lighting"],
          "action": "regenerated",
          "original_image_url": "storyboard/episode_1/frame_002_v1.png",
          "fixed_image_url": "storyboard/episode_1/frame_002_v2.png"
        }
      ]
    }
  ]
}
```

---

## Step 9: edit_output.json (sv-edit)

```json
{
  "episodes": [
    {
      "episode_number": 1,
      "merged_url": "output/episode_1/merged.mp4",
      "subtitles_url": "output/episode_1/subtitles.srt",
      "bgm_url": "output/episode_1/bgm.wav",
      "final_url": "output/episode_1/final_selected.mp4",
      "settings": {
        "enable_transitions": true,
        "bgm_volume": 0.3,
        "no_vocals": true
      },
      "versions": [
        {"version": 1, "video_url": "output/episode_1/final_v1.mp4", "selected": true}
      ]
    }
  ]
}
```

---

## Step 10: review_notes.json (sv-review)

```json
{
  "review_date": "2026-02-14",
  "episodes": [
    {
      "episode_number": 1,
      "status": "needs_revision",
      "notes": [
        {
          "id": "note_001",
          "timecode": "00:01:23",
          "x_position": 45,
          "y_position": 30,
          "text": "这里的表情可以再夸张一点",
          "linked_shot_id": "shot_003",
          "author": "AI导演",
          "status": "open",
          "category": "visual",
          "severity": "minor",
          "suggested_fix_step": "sv-storyboard",
          "suggested_fix_action": "Regenerate frame 5 with stronger expression"
        }
      ],
      "overall_rating": 7,
      "summary": "Good pacing, needs expression adjustments"
    }
  ],
  "overall_status": "needs_revision",
  "priority_fixes": [
    "Regenerate frame 5 in episode 1 for stronger expression"
  ]
}
```

---

## QA: quality_feedback.json (sv-judge)

```json
{
  "feedback_date": "2026-02-14T10:30:00Z",
  "feedback_session_id": "uuid-generated",
  "project_id": "project-uuid",
  "content_evaluated": {
    "assets": [...],
    "storyboard": [...],
    "shots": [...],
    "script": null,
    "voice": [...]
  },
  "overall_summary": {
    "total_items_evaluated": 8,
    "excellent_count": 2,
    "good_count": 5,
    "acceptable_count": 1,
    "needs_rework_count": 0,
    "average_quality_score": 4.1,
    "recommendations": [...]
  }
}
```

## QA: quality_insights.json (sv-judge)

```json
{
  "insights_date": "2026-02-14",
  "patterns": [...],
  "model_performance": {...},
  "prompt_recommendations": [...],
  "items_to_regenerate": [...]
}
```

---

## Version Tracking Convention

Media-generating steps track all generation attempts via version arrays:

### Character Versions (uses `look_references`)
```json
{
  "look_references": [
    {"id": "look_001", "image_url": "assets/characters/char_001_v1.png", "is_locked": false, "prompt": "..."},
    {"id": "look_002", "image_url": "assets/characters/char_001_v2.png", "is_locked": true, "prompt": "..."}
  ],
  "locked_look_id": "look_002",
  "image_url": "assets/characters/char_001_v2.png"
}
```

### Generic Versions (storyboard frames, shots, edits)
```json
{
  "versions": [
    {"version": 1, "image_url": "path/to/v1.png", "prompt": "...", "selected": false},
    {"version": 2, "image_url": "path/to/v2.png", "prompt": "...", "selected": true}
  ],
  "image_url": "path/to/v2.png"
}
```

### Video Versions
```json
{
  "versions": [
    {"version": 1, "video_url": "path/to/v1.mp4", "prompt": "...", "tool_used": "kling_o3_i2v", "selected": true}
  ],
  "video_url": "path/to/v1.mp4"
}
```

---

## Cross-References

- **Backend schemas**: `/home/ubuntu/repos/mvp_backend/app/schemas/`
  - `project.py` → project_settings.json
  - `script.py` → script_bible.json
  - `character.py` → assets.json characters
  - `scene.py` → assets.json scenes
  - `prop.py` → assets.json props
  - `storyboard.py`, `keyframes.py` → storyboard.json
  - `shots.py`, `shot2.py` → shots.json
  - `review.py` → review_notes.json
  - `edit.py` → edit_output.json
  - `version.py` → version tracking
- **Conventions**: `context/conventions.md` — file naming, versioning rules
- **Git management**: `context/git-management.md` — commit conventions
- **Workflow**: `context/workflow-overview.md` — pipeline dependencies

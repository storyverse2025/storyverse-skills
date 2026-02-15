# StoryVerse Workflow Overview

## 10-Step AI Short Film Production Pipeline

```
Step 1: INTAKE          Step 2: PLAN           Step 3: SCRIPT
[Story Inspiration] --> [Project Settings] --> [Script Bible]
                                                    |
                    +-------------------------------+
                    |
                    v
Step 4: ASSETS          Step 5: STORYBOARD     Step 6: SHOTS
[Characters/Scenes] --> [Keyframe Images]  --> [Video Clips]
                              |                     |
                              v                     v
                    Step 8: CONSISTENCY     Step 7: VOICE
                    [Image QA & Fix]       [Voice Transform]
                              |                     |
                              +----------+----------+
                                         |
                                         v
                              Step 9: EDIT
                              [Concat + STT + BGM + Compose]
                                         |
                                         v
                              Step 10: REVIEW
                              [Final Review + Notes]
```

## Step Dependencies

| Step | Skill | Reads | Produces |
|------|-------|-------|----------|
| 1 | `/sv-intake` | User input (text, files) | `project_brief.json` |
| 2 | `/sv-plan` | `project_brief.json` | `project_settings.json` |
| 3 | `/sv-script` | `project_brief.json`, `project_settings.json` | `script_bible.json` |
| 4 | `/sv-assets` | `script_bible.json`, `project_settings.json` | `assets.json` |
| 5 | `/sv-storyboard` | `script_bible.json`, `assets.json`, `project_settings.json` | `storyboard.json` |
| 6 | `/sv-shots` | `storyboard.json`, `project_settings.json` | `shots.json` |
| 7 | `/sv-voice` | `shots.json`, `script_bible.json` | `harmonized_shots.json` |
| 8 | `/sv-consistency` | `storyboard.json` | Updates `storyboard.json`, `consistency_report.json` |
| 9 | `/sv-edit` | `harmonized_shots.json` or `shots.json` | `edit_output.json` |
| 10 | `/sv-review` | `edit_output.json` | `review_notes.json` |

## State File Formats

For complete JSON schemas with all fields, see `context/json-schemas.md`.

### project_brief.json
```json
{
  "title": "项目标题",
  "inspiration": "Story inspiration text...",
  "file_summaries": [{"filename": "ref.pdf", "summary": "..."}],
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

### project_settings.json
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
    "aspect_ratio": "9:16"
  },
  "status": "draft",
  "current_step": 2,
  "created_at": "2026-02-14T10:00:00Z",
  "updated_at": "2026-02-14T10:00:00Z"
}
```

### script_bible.json
```json
{
  "title": "霸道总裁爱上我",
  "logline": "One-line story summary",
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
      "core_conflict": "Central tension",
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

### assets.json
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
        {"id": "look_001", "image_url": "assets/characters/char_001_v1.png", "is_locked": false, "prompt": "..."}
      ],
      "locked_look_id": "look_001",
      "first_episode": 1
    }
  ],
  "scenes": [
    {
      "id": "scene_001",
      "name": "咖啡店内景",
      "story_facts": {"location": "城市咖啡店", "time": "日", "event": "女主工作场景"},
      "visual_look": {"material": "木质温馨", "lighting": "暖黄色调", "era": "现代都市", "mood": "温馨"},
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
      "appearances": [{"episode_number": 1, "scene_number": 1, "shot_number": 3}]
    }
  ]
}
```

### storyboard.json
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
          "summary": "Visual description",
          "shot_type": "medium",
          "dialogue": {"character_name": "林小夏", "text": "...", "emotion": "sad"},
          "character_ids": ["char_001"],
          "scene_id": "scene_001",
          "prop_ids": ["prop_001"],
          "prompt": "...",
          "image_url": "storyboard/episode_1/frame_001_selected.png",
          "versions": [
            {"version": 1, "image_url": "storyboard/episode_1/frame_001_v1.png", "prompt": "...", "selected": true}
          ]
        }
      ]
    }
  ]
}
```

### shots.json
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
          "description": "Visual description",
          "dialogue": "Dialogue text",
          "duration": 5,
          "storyboard_frame_id": "frame_001",
          "character_ids": ["char_001"],
          "scene_id": "scene_001",
          "beat": {
            "segments": [{"time_range": "0-2s", "action": "...", "locked": false}],
            "locks": {"character": true, "scene": true, "style": false}
          },
          "prompt": "Motion prompt",
          "video_url": "shots/episode_1/shot_001_selected.mp4",
          "image_url": "storyboard/episode_1/frame_001_selected.png",
          "status": "completed",
          "tool_used": "kling_o3_i2v",
          "versions": [
            {"version": 1, "video_url": "shots/episode_1/shot_001_v1.mp4", "prompt": "...", "tool_used": "kling_o3_i2v", "selected": true}
          ]
        }
      ]
    }
  ]
}
```

### harmonized_shots.json
```json
{
  "voice_mapping": {
    "林小夏": {"voice_id": "...", "description": "Young female, warm"}
  },
  "episodes": [
    {
      "episode_number": 1,
      "shots": [
        {
          "beat_number": 1,
          "original_video_url": "shots/episode_1/shot_001_selected.mp4",
          "harmonized_video_url": "harmonized/episode_1/beat_001_selected.mp4",
          "dialogue": "...",
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

### edit_output.json
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

### review_notes.json
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
          "text": "Feedback text",
          "linked_shot_id": "shot_003",
          "author": "AI导演",
          "status": "open",
          "category": "visual",
          "severity": "minor",
          "suggested_fix_step": "sv-storyboard",
          "suggested_fix_action": "Regenerate frame with adjustments"
        }
      ],
      "overall_rating": 7,
      "summary": "Good pacing, needs adjustments"
    }
  ],
  "overall_status": "needs_revision",
  "priority_fixes": [...]
}
```

## Working Directory Convention

All state files are stored in the current working directory. Each project is an independent git repository with Git LFS for large media files.

See `context/git-management.md` for git initialization, commit conventions, and LFS configuration.

### Recommended Project Structure

```
my-film-project/
├── .git/
├── .gitattributes          # LFS tracking rules
├── .gitignore              # Ignore temp files
├── project_brief.json
├── project_settings.json
├── script_bible.json
├── assets.json
├── storyboard.json
├── shots.json
├── harmonized_shots.json
├── edit_output.json
├── review_notes.json
├── quality_feedback.json
├── quality_insights.json
├── pipeline_state.json
├── assets/
│   ├── characters/
│   │   ├── char_001_v1.png          # Version 1
│   │   ├── char_001_v2.png          # Version 2
│   │   └── char_001_selected.png    # Selected version
│   ├── scenes/
│   │   ├── scene_001_v1.png
│   │   └── scene_001_selected.png
│   └── props/
│       └── prop_001_selected.png
├── storyboard/
│   └── episode_1/
│       ├── frame_001_v1.png
│       ├── frame_001_v2.png
│       └── frame_001_selected.png
├── shots/                           # LFS-tracked
│   └── episode_1/
│       ├── shot_001_v1.mp4
│       └── shot_001_selected.mp4
├── harmonized/                      # LFS-tracked
│   └── episode_1/
│       └── beat_001_selected.mp4
└── output/                          # LFS-tracked
    └── episode_1/
        ├── merged.mp4
        ├── subtitles.srt
        ├── bgm.wav
        ├── final_v1.mp4
        └── final_selected.mp4
```

### Version File Naming

All media files use versioned naming:
- `{id}_v{N}.{ext}` — Version N of the asset (e.g., `char_001_v1.png`)
- `{id}_selected.{ext}` — Copy of the currently selected version

See `context/conventions.md` for full naming conventions.

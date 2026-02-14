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
| 8 | `/sv-consistency` | `storyboard.json` | Updates `storyboard.json` |
| 9 | `/sv-edit` | `harmonized_shots.json` or `shots.json` | `edit_output.json` |
| 10 | `/sv-review` | `edit_output.json` | `review_notes.json` |

## State File Formats

### project_brief.json
```json
{
  "inspiration": "Story inspiration text...",
  "file_summaries": [{"filename": "ref.pdf", "summary": "..."}],
  "genre": "romance",
  "tone": "dramatic",
  "themes": ["love", "betrayal"],
  "visual_style": "cinematic, warm tones",
  "target_audience": "young adults"
}
```

### project_settings.json
```json
{
  "title": "My Short Film",
  "language": "zh",
  "target_channel": "female",
  "episode_count": 10,
  "episode_duration": 90,
  "aspect_ratio": "9:16"
}
```

### script_bible.json
```json
{
  "logline": "One-line story summary",
  "episodes": [
    {
      "episode_index": 1,
      "core_conflict": "Character A vs Character B",
      "content": "Full screenplay text..."
    }
  ]
}
```

### assets.json
```json
{
  "characters": [
    {
      "asset_id": "character_1",
      "name": "Character Name",
      "role": "protagonist",
      "image_url": "https://...",
      "prompt": "Generation prompt used"
    }
  ],
  "scenes": [
    {
      "asset_id": "scene_1",
      "name": "Scene Name",
      "image_url": "https://...",
      "prompt": "Generation prompt used"
    }
  ],
  "props": []
}
```

### storyboard.json
```json
{
  "episodes": [
    {
      "episode_index": 1,
      "frames": [
        {
          "frame_number": 1,
          "beat_number": 1,
          "summary": "Visual description of the frame",
          "shot_type": "medium",
          "dialogue": {"character_name": "A", "text": "...", "emotion": "sad"},
          "character_ids": ["character_1"],
          "image_url": "https://..."
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
      "episode_index": 1,
      "shots": [
        {
          "beat_number": 1,
          "status": "success",
          "video_url": "https://...",
          "image_url": "https://...",
          "generation_prompt": "Motion prompt...",
          "dialogue": "Dialogue text..."
        }
      ]
    }
  ]
}
```

### harmonized_shots.json
```json
{
  "episodes": [
    {
      "episode_index": 1,
      "shots": [
        {
          "beat_number": 1,
          "original_video_url": "https://...",
          "harmonized_video_url": "/path/to/harmonized.mp4",
          "voice_mapping": {"Character A": "voice_id_1"}
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
      "episode_index": 1,
      "merged_url": "/path/to/merged.mp4",
      "subtitles_url": "/path/to/subtitles.srt",
      "bgm_url": "/path/to/bgm.wav",
      "final_url": "/path/to/final.mp4"
    }
  ]
}
```

### review_notes.json
```json
{
  "episodes": [
    {
      "episode_index": 1,
      "notes": [
        {
          "timecode": "00:01:23",
          "text": "Audio sync issue here",
          "category": "audio",
          "suggested_fix_step": "sv-voice"
        }
      ],
      "status": "approved"
    }
  ]
}
```

## Working Directory Convention

All state files are stored in the current working directory. Recommended project structure:

```
my-film-project/
├── project_brief.json
├── project_settings.json
├── script_bible.json
├── assets.json
├── storyboard.json
├── shots.json
├── harmonized_shots.json
├── edit_output.json
├── review_notes.json
├── pipeline_state.json
├── assets/                  # Downloaded/generated asset images
│   ├── characters/
│   ├── scenes/
│   └── props/
├── storyboard/              # Keyframe images
│   └── episode_1/
├── shots/                   # Video clips
│   └── episode_1/
├── harmonized/              # Voice-transformed clips
│   └── episode_1/
└── output/                  # Final edited videos
    └── episode_1/
```

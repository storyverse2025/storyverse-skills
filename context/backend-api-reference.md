# StoryVerse Backend API Reference

Base URL: `$STORYVERSE_BACKEND_URL` (default: `http://34.204.80.155/api/v1`)

Authentication: Bearer token via `Authorization: Bearer $STORYVERSE_API_TOKEN` header.

## Authentication

### Register
```
POST /auth/register
Body: { "username": str, "email": str, "password": str }
Response: { "id": str, "username": str, "email": str }
```

### Login
```
POST /auth/login
Body: { "username": str, "password": str }
Response: { "access_token": str, "token_type": "bearer" }
```

## Projects

### Create Project
```
POST /projects2/{project_id}
Body: {
    "title": str (1-200 chars),
    "inspiration": str (max 2000 chars, optional),
    "settings": {
        "target_channel": "female" | "male" | "general",
        "language": "zh" | "en",
        "episode_count": int (1-100, default 10),
        "episode_duration": int (seconds, default 90),
        "aspect_ratio": "16:9" | "9:16"
    }
}
```

### Get Project
```
GET /projects2/{project_id}
Response: Project with status, settings, counts
```

## Scripts (Bible & Episodes)

### Generate Script Bible
```
POST /projects/{project_id}/scripts
Body: {
    "inspiration": str (max 2000 chars),
    "file_ids": list[int],
    "settings": {
        "language": "zh" | "en",
        "episode_duration": 90,
        "episode_count": 10,
        "target_channel": "female",
        "aspect_ratio": "9:16"
    }
}
Response: {
    "logline": str,
    "episodes": [
        {
            "episode_index": int,
            "core_conflict": str,
            "content": str (full screenplay)
        }
    ]
}
```

## Characters

### Generate Base Characters (Casting)
```
POST /projects/{project_id}/characters
Body: {
    "language": "Chinese" | "English",
    "episodes": [
        {
            "index": int,
            "core_conflict": str,
            "content": str (episode script)
        }
    ]
}
Response: [
    {
        "asset_id": str,
        "img_url": str,
        "prompt": str
    }
]
```

### Regenerate Character Image
```
PUT /projects/{project_id}/characters/{character_id}/regenerate
Body: {
    "prompt": str,
    "image_url": str,
    "gacha": 0 | 1
}
Response: { "image_url": str }
```

### Stylize Character Image
```
POST /projects/{project_id}/characters/stylization
Body: {
    "uploaded_image_url": str,
    "reference_image_url": str,
    "aspect_ratio": "16:9" | "9:16",
    "output_format": "png"
}
Response: { "image_url": str }
```

## Keyframes (Storyboard)

### Generate Keyframes
```
GET /projects/{project_id}/episodes/{episode_id}/keyframes?language={lang}&timestamp=0
Response: {
    "frames": [
        {
            "frame_number": int,
            "beat_number": int,
            "summary": str,
            "shot_type": "extreme_wide" | "wide" | "full" | "medium_wide" | "medium" | "medium_close" | "close" | "extreme_close",
            "dialogue": { "character_name": str, "text": str, "emotion": str },
            "image_url": str
        }
    ]
}
```

### Regenerate Keyframe
```
PUT /projects/{project_id}/episodes/{episode_id}/keyframes/{keyframe_id}/regenerate
Body: { "prompt": str }
Response: { "frame_id": str, "image_url": str }
```

## Video Shots

### Generate Video Shots
```
GET /projects/{project_id}/shots?episode_index={n}&language={lang}
Response: {
    "videos": [
        {
            "beat_number": int,
            "status": "success" | "failed",
            "error": str | null,
            "prompt": str,
            "dialogue": str,
            "video_url": str | null,
            "image_url": str | null
        }
    ]
}
```

### Regenerate Video Shot
```
PUT /projects/{project_id}/shots/{beat_number}/regenerate
Body: {
    "prompt": str,
    "image_url": str,
    "shot_url": str,
    "resolution": "720p",
    "aspect_ratio": "16:9",
    "duration": 4,
    "in_place": true
}
Response: {
    "status": str,
    "message": str,
    "data": { "prompt": str, "img_url": str, "video_url": str }
}
```

## Edit Pipeline

### Run Full Pipeline
```
POST /projects/{project_id}/episodes/{episode_id}/edits/pipeline
Body: {
    "clip_paths": list[str],
    "output_dir": str,
    "width": 1280,
    "height": 720,
    "fps": 30,
    "language_code": str | null,
    "diarize": false,
    "no_vocals": false,
    "bgm_volume": 0.3,
    "main_volume": 1.0,
    "fade_seconds": 2.0,
    "enable_transitions": false,
    "overlap_seconds": 0.25,
    "vlm_model": "gemini-2.5-flash"
}
Response: {
    "success": true,
    "message": str,
    "files": {
        "merged_url": str,
        "subtitles_url": str,
        "bgm_url": str,
        "final_url": str
    }
}
```

### Individual Pipeline Steps

#### Concatenate Videos
```
POST /projects/{project_id}/episodes/{episode_id}/edits/concat
Body: { "clip_paths": list[str], "output_path": str, "enable_transitions": false, ... }
```

#### Speech-to-Text
```
POST /projects/{project_id}/episodes/{episode_id}/edits/stt
Body: { "input_video_path": str, "srt_output_path": str, "language_code": str }
```

#### Generate Background Music
```
POST /projects/{project_id}/episodes/{episode_id}/edits/music
Body: { "input_video_path": str, "output_path": str, "no_vocals": true }
```

#### Final Composition
```
POST /projects/{project_id}/episodes/{episode_id}/edits/compose
Body: { "input_video_path": str, "bgm_audio_path": str, "output_path": str, "subtitles_path": str }
```

## File Uploads

### Upload File
```
POST /uploads
Body: multipart/form-data with file
Response: { "file_id": int, "filename": str, "url": str }
```

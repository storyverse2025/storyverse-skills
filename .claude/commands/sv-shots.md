You are the StoryVerse Video Shot Generator. Your job is to generate video clips from storyboard keyframe images.

## Your Task

Convert each keyframe image into a video clip using image-to-video generation, and save results as `shots.json`.

## User Input (optional — episode number or regeneration instructions)

$ARGUMENTS

## Prerequisites

Read these files from the current directory:
- `storyboard.json` — Keyframe images and their descriptions
- `project_settings.json` — Aspect ratio and settings
- `assets.json` — Character and scene references (for IDs)

If any file is missing, tell the user which skill to run first.

## MCP Tools Available

**Image-to-Video tools** (listed by recommendation):

### kling_o3_i2v (Recommended)
Best quality. Supports start+end frame for smooth transitions between consecutive shots.
```
kling_o3_i2v(
    image_url: str,           # Start frame (required)
    prompt: str = "",         # Motion guidance (max 5000 chars)
    end_image_url: str = "",  # End frame for transitions (optional)
    duration: int = 5,        # 3-15 seconds
    aspect_ratio: str = "16:9", # 16:9, 9:16, 1:1
    generate_audio: bool = True,
    negative_prompt: str = "blur, distort, and low quality",
    cfg_scale: float = 0.5
)
```

### kling_o3_pro_i2v (Higher quality, supports multi-prompt)
```
kling_o3_pro_i2v(
    image_url: str,
    prompt: str | None = None,
    end_image_url: str | None = None,
    duration: int = 5,        # 3-15 seconds
    generate_audio: bool = True,
    multi_prompt: list[dict] | None = None,  # [{prompt, duration}]
    aspect_ratio: str = "16:9"
)
```

### sora2_i2v (Alternative style)
```
sora2_i2v(
    prompt: str,
    image_url: str,
    duration: int = 4,        # 4, 8, or 12 seconds
    aspect_ratio: str = "auto" # auto, 9:16, 16:9
)
```

### grok_imagine_i2v (Fast generation)
```
grok_imagine_i2v(
    prompt: str,
    image_url: str,
    duration: int = 6,        # 1-15 seconds
    aspect_ratio: str = "auto"
)
```

## Procedure

### 1. Plan Video Shots

For each episode in `storyboard.json`:
- Read the frames in sequence
- For each frame, plan the video shot:
  - **Start image**: The keyframe's `image_url` (use the `_selected.png` local path)
  - **Grid layout**: Check the frame's `grid_layout` field (1, 3, 6, or 9) — this affects how you craft the motion prompt
  - **End image**: The next keyframe's `image_url` (for smooth transitions with Kling)
  - **Motion prompt**: Describe camera movement and character action based on:
    - The frame's `summary` (what's happening visually)
    - The frame's `dialogue` (lip movement, gestures)
    - The `shot_type` (determines camera behavior)
    - The `grid_layout` (see Grid-Aware Prompts below)
  - **Duration**: Calculate based on dialogue length and action complexity (typically 3-5 seconds per beat)
  - **Character/scene IDs**: Carry forward from storyboard frame
  - **Storyboard frame link**: Record `storyboard_frame_id` for traceability

#### Grid-Aware Motion Prompts

The `grid_layout` of the input keyframe affects how the video model interprets the image:

- **grid_layout: 1** — Single long-take keyframe. Prompt describes motion from this single scene.
- **grid_layout: 4** — Four panels (2×2) show a dialogue/progression sequence. Prompt should reference the grid: "Starting from the top-left panel, transition through the top-right action, continuing to bottom-left escalation, and resolving in bottom-right..."
- **grid_layout: 6** — Six panels (2×3) show balanced progression. Prompt should describe flowing through the grid: "Animate the sequence shown in the 2×3 storyboard grid, from establishing shot through the action to the resolution..."
- **grid_layout: 9** — Nine panels (3×3) provide maximum continuity detail for action-heavy beats. Prompt should guide the model through the full arc: "Follow the 3×3 storyboard sequence panel by panel, creating smooth motion from the establishing shot through the dramatic peak to the transition..."

**Tip**: Multi-panel grids generally produce better video continuity because the model has more visual context. If a 1-panel shot produces jerky or incoherent video, suggest returning to `/sv-storyboard` and switching to a higher grid count.

### 2. Craft Generation Prompts (Backend Format)

Each shot's `generation_prompt` must follow this structured format from the backend:

```
GOAL: [One sentence — what this beat achieves narratively]
SHOT_PLAN:
  00.00s-03.00s: [Camera phrase from library] — [character action with asset_identifier]
  03.00s-06.00s: [Camera phrase] — [action]
  06.00s-09.00s: [Camera phrase] — [action]
  09.00s-12.00s: [Camera phrase] — [action/button]
DIALOGUE:
  01.00s 【asset_identifier】: Utterance text
  05.00s 【asset_identifier】: Utterance text
EXPORT: [Visual summary for rendering — lighting, atmosphere, motion carriers]
VISUAL_PROMPT: [Concise scene description for the video model, ≤180 chars]
```

**Camera Library (use exact phrases):**

Low-motion preferred (default first choice):
- Static Hold (No Movement)
- Static Floating
- Wide Shot + Fog Drift
- Push In (Killer Intent)
- Rack Focus (Fast)

Core coverage:
- Reverse Pullback (Vacuum)
- Profile Tracking (Handheld Shake)
- Low Angle Truck Left (Slider)
- Over-Shoulder Whip
- Snap Zoom (Face)
- Return Snap (Reaction)
- Dutch Angle Close Up (Tension)
- Silhouette Reveal (Backlight)

Stylized (use sparingly, max 1 per beat):
- Crash Zoom In (Head on)
- 360 Bullet Time
- Tumble Cam (Chaos)
- Orbital Spin

**Segment rules:**
- Timeline starts at 00.00s (no buffer)
- Allowed segment lengths: 2s, 3s, 4s, 5s, 6s
- Segment count per beat: 3-8
- Lengths must sum exactly to `duration_seconds`
- Adapt by beat type:
  - action_high: shorter (2-3s) segments
  - dialogue_heavy: longer (3-4s) segments
  - emotion_hold: include at least one 4-6s hold
- Every segment must include a visible motion carrier (rain/fog/smoke/light/cloth/debris)
- Each segment action must include a character-action clause with [asset_identifier]
- Generation prompt total ≤ 4800 characters

### 3. Define Beat Segments

For each shot, define the `beat` structure with time-based segments:
```json
"beat": {
  "segments": [
    {"time_range": "0-2s", "action": "林小夏端着咖啡", "locked": false},
    {"time_range": "2-5s", "action": "穿过大堂", "locked": false}
  ],
  "locks": {"character": true, "scene": true, "style": false}
}
```

The `locks` object tracks which aspects are finalized:
- `character`: true = character appearance is locked
- `scene`: true = scene/background is locked
- `style`: true = visual style is locked

### 4. Generate Video Clips

For each beat, generate using the recommended tool:

```
kling_o3_i2v(
    image_url=frame["image_url"],
    prompt="[motion prompt]",
    end_image_url=next_frame["image_url"],  # For transition continuity
    duration=5,
    aspect_ratio=<project aspect_ratio>,
    generate_audio=True
)
```

**Download and save locally** with versioned naming:
- Create directory: `shots/episode_{N}/`
- Save to `shots/episode_{N}/shot_{NNN}_v1.mp4`
- Copy to `shots/episode_{N}/shot_{NNN}_selected.mp4`
- Use relative paths in JSON output

**Tips:**
- Use `end_image_url` to create smooth visual transitions between consecutive shots
- For the last beat of an episode, omit `end_image_url`
- Set `generate_audio=True` for initial audio (will be replaced by voice harmonization later)
- Use `negative_prompt` to avoid common artifacts

### 5. Save Results

Write `shots.json` (see `context/json-schemas.md` for full field reference):
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
              {"time_range": "0-2s", "action": "端着咖啡", "locked": false},
              {"time_range": "2-5s", "action": "穿过大堂", "locked": false}
            ],
            "locks": {"character": true, "scene": true, "style": false}
          },
          "prompt": "Motion prompt used",
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

### 6. Handle Failures

- If a shot fails, record `status: "failed"` with the error message
- Offer to retry with a different tool (e.g., switch from Kling to Sora2)
- Offer to adjust the prompt and regenerate
- Failed shots don't get a version entry

### 7. Present Results

- Show each generated shot with its beat number, duration, and status
- Report success/failure counts
- Offer to regenerate specific shots
- For regeneration:
  - Save new version as `shot_{NNN}_v2.mp4`
  - Add to `versions` array, set as selected
  - Update `video_url` to new `_selected.mp4`

### 8. Backend Integration (optional)

If `$STORYVERSE_BACKEND_URL` is set, **re-read `shots.json`** to pick up any user modifications, then sync:
```
GET http://34.204.80.155/api/v1/projects/{project_id}/shots?episode_index={n}&language={lang}
```

**Important**: Always re-read the JSON file immediately before API calls.

## Git Management

After saving `shots.json` and video files, commit:

```bash
git add shots.json shots/episode_*/
git commit -m "step 6: sv-shots - generate video shots for episode N"
```

For regenerations:
```bash
git add shots.json shots/episode_1/shot_003_v2.mp4 shots/episode_1/shot_003_selected.mp4
git commit -m "step 6: sv-shots - regenerate shot_003 v2"
```

## After Completion

Suggest running `/sv-voice` to add character voices, or `/sv-edit` to skip voice and go straight to editing.

## Guidelines

- Process one episode at a time to manage context
- If `$ARGUMENTS` specifies an episode number, only generate shots for that episode
- Keep shot durations between 3-8 seconds for short drama pacing
- Use Kling O3 as the default; fall back to Sora2 or Grok if Kling fails
- Monitor for moderation blocks — adjust prompts if content is flagged
- Always download generated videos locally and use relative paths
- The `storyboard_frame_id` links each shot to its source keyframe for traceability
- **Grid retry**: If video quality is poor for a shot, check `storyboard.json` — the frame likely has other grid variants (1, 4, 6, 9) already generated. Suggest switching to a different grid layout via `/sv-storyboard` before regenerating the video. Higher grid counts (6, 9) generally improve continuity for action beats; lower counts (1, 4) improve visual clarity for dialogue and close-ups.

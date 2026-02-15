# StoryVerse Git & Git LFS Management

## Design: Each Project is an Independent Git Repo

Each project output folder (e.g., `my-film-project/`) is its own independent git repository. This enables:
- Full version history of all assets, scripts, and generated media
- Git LFS for large binary files (video, audio)
- Multiple collaborators working on the same project via push/pull
- Branching for experimental variations

The project folder is **not** a subfolder of the `storyverse-skills` repo — it's a standalone repo.

---

## Repo Initialization

On the first skill run (`sv-intake` or `sv-pipeline`), initialize the project repo:

### 1. Check if already a git repo
```bash
git rev-parse --is-inside-work-tree 2>/dev/null
```

### 2. If not, initialize
```bash
git init
git lfs install
```

### 3. Create `.gitattributes` for LFS
```
# Video files
*.mp4 filter=lfs diff=lfs merge=lfs -text
*.webm filter=lfs diff=lfs merge=lfs -text
*.mov filter=lfs diff=lfs merge=lfs -text
# Audio files
*.wav filter=lfs diff=lfs merge=lfs -text
*.mp3 filter=lfs diff=lfs merge=lfs -text
*.flac filter=lfs diff=lfs merge=lfs -text
# Large image files (optional, for high-res assets)
*.psd filter=lfs diff=lfs merge=lfs -text
```

### 4. Create `.gitignore`
```
*.log
__pycache__/
.env
*.tmp
.DS_Store
```

### 5. Initial commit
```bash
git add .gitattributes .gitignore
git commit -m "init: project repository with LFS config"
```

**Note:** Always check `git rev-parse` before `git init` to avoid re-initializing an existing repo.

---

## Auto-Commit After Each Step

Each skill ends with a git commit. Follow this pattern:

### 1. Stage output files
```bash
git add <output_json_file>
git add <generated_media_files>
```

### 2. Commit with descriptive message
```bash
git commit -m "step N: <skill_name> - <brief description>"
```

### Commit Message Examples

| Step | Example Message |
|------|----------------|
| 1 | `step 1: sv-intake - capture project brief` |
| 2 | `step 2: sv-plan - configure project settings` |
| 3 | `step 3: sv-script - generate script bible with 10 episodes` |
| 4 | `step 4: sv-assets - generate 5 characters, 3 scenes, 2 props` |
| 5 | `step 5: sv-storyboard - generate keyframes for episode 1` |
| 6 | `step 6: sv-shots - generate video shots for episode 1` |
| 7 | `step 7: sv-voice - harmonize voices for episode 1` |
| 8 | `step 8: sv-consistency - check and fix 2 frames` |
| 9 | `step 9: sv-edit - compose final video for episode 1` |
| 10 | `step 10: sv-review - review notes for episode 1` |

### Regeneration Commits
```bash
git commit -m "step 4: sv-assets - regenerate char_001 v3"
git commit -m "step 5: sv-storyboard - regenerate frame_005 v2"
git commit -m "step 6: sv-shots - regenerate shot_003 v2 with sora2"
```

---

## Skill-Specific Git Instructions

| Skill | Files to Stage | Notes |
|-------|---------------|-------|
| `sv-intake` | `project_brief.json`, `.gitattributes`, `.gitignore` | Init repo first |
| `sv-plan` | `project_settings.json` | |
| `sv-script` | `script_bible.json` | |
| `sv-assets` | `assets.json`, `assets/characters/*.png`, `assets/scenes/*.png`, `assets/props/*.png` | Images tracked by git |
| `sv-storyboard` | `storyboard.json`, `storyboard/episode_N/*.png` | Images tracked by git |
| `sv-shots` | `shots.json`, `shots/episode_N/*.mp4` | Videos tracked by LFS |
| `sv-voice` | `harmonized_shots.json`, `harmonized/episode_N/*.mp4` | Videos tracked by LFS |
| `sv-edit` | `edit_output.json`, `output/episode_N/*` | Videos/audio tracked by LFS |
| `sv-review` | `review_notes.json` | |
| `sv-consistency` | `storyboard.json`, `consistency_report.json`, fixed images | |
| `sv-judge` | `quality_feedback.json`, `quality_insights.json` | |
| `sv-pipeline` | `pipeline_state.json` | Also commits from each sub-step |

---

## LFS File Types

Files tracked by Git LFS (defined in `.gitattributes`):

| Extension | Category | Typical Size |
|-----------|----------|-------------|
| `.mp4` | Video | 1-50 MB per clip |
| `.webm` | Video | 1-30 MB per clip |
| `.mov` | Video | 5-100 MB per clip |
| `.wav` | Audio | 1-20 MB per track |
| `.mp3` | Audio | 0.5-5 MB per track |
| `.flac` | Audio | 5-30 MB per track |
| `.psd` | Image (high-res) | 10-100 MB |

PNG and JPG images are tracked by regular git (typically < 5 MB each).

---

## Directory Structure

```
my-project/
├── .git/
├── .gitattributes
├── .gitignore
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
├── assets/
│   ├── characters/
│   │   ├── char_001_v1.png
│   │   ├── char_001_v2.png
│   │   └── char_001_selected.png
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
├── shots/
│   └── episode_1/
│       ├── shot_001_v1.mp4
│       └── shot_001_selected.mp4
├── harmonized/
│   └── episode_1/
│       └── beat_001_selected.mp4
└── output/
    └── episode_1/
        ├── merged.mp4
        ├── subtitles.srt
        ├── bgm.wav
        ├── final_v1.mp4
        └── final_selected.mp4
```

---

## Best Practices

1. **Always check before init**: Run `git rev-parse --is-inside-work-tree` before `git init`
2. **Commit after each step**: Don't batch commits across multiple pipeline steps
3. **Use relative paths**: All file references in JSON should be relative to the project root
4. **Stage specific files**: Use explicit file paths, not `git add .`
5. **LFS for large binaries**: Video and audio files go through LFS automatically via `.gitattributes`
6. **Descriptive messages**: Include step number, skill name, and what was done
7. **Track regenerations**: Each regeneration gets its own commit with version info

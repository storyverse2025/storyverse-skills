You are the StoryVerse Voice Harmonization Assistant. Your job is to transform speaker voices in video clips to match character voice profiles.

## Your Task

Apply voice transformation to video shots so each character has a consistent, distinct voice. Save results as `harmonized_shots.json`.

## User Input (optional — episode number or voice preferences)

$ARGUMENTS

## Prerequisites

Read these files from the current directory:
- `shots.json` — Video clips with dialogue information
- `script_bible.json` — Full screenplays with character dialogue
- `assets.json` — Character personas for voice matching

If files are missing, tell the user which skill to run first (`/sv-shots`).

## Required Environment

- `ELEVENLABS_API_KEY` must be set
- The voice harmonization pipeline from the `storyverse` repo should be available at `~/repos/storyverse/voice_harmonization/`

## Procedure

### 1. Analyze Dialogue and Characters

From `script_bible.json` and `shots.json`:
- Identify all speaking characters across episodes
- Map each character to their dialogue lines per beat
- Note emotional states from dialogue annotations

### 2. Set Up Voice Mapping

Create a voice mapping YAML file (`voice_mapping.yaml`) for each episode:

```yaml
voice_mapping:
  "Character A":
    voice_id: "voice_id_here"
    description: "Young female, warm, confident"
  "Character B":
    voice_id: "voice_id_here"
    description: "Middle-aged male, deep, authoritative"
```

**Voice selection guidance:**
- Ask the user to choose voice profiles for each character
- If ElevenLabs voice library is accessible, list available voices
- Match voice characteristics to character descriptions from `assets.json` character `persona`

### 3. Run Voice Harmonization

For each episode's video clips, run the voice harmonization pipeline:

**Option A: CLI Pipeline** (if storyverse repo is available)

First, verify the pipeline exists:
```bash
VOICE_DIR="$HOME/repos/storyverse/voice_harmonization"
ls "$VOICE_DIR/pipeline.py"
```

If found, run:
```bash
cd "$HOME/repos/storyverse/voice_harmonization"
python -u pipeline.py \
    --input-dir <shots_directory> \
    --output-dir <harmonized_directory> \
    --prompt-file <voice_mapping.yaml> \
    --character <default_character>
```

TTS mode (for cleaner synthesized speech):
```bash
cd "$HOME/repos/storyverse/voice_harmonization"
python -u pipeline.py \
    --input-dir <shots_directory> \
    --output-dir <harmonized_directory> \
    --prompt-file <voice_mapping.yaml> \
    --use-tts
```

The pipeline performs:
1. Audio extraction from video
2. Speaker diarization (separating speakers)
3. Forced alignment (word-level timing)
4. Voice transformation using ElevenLabs Voice Changer API
5. Audio re-composition into video

**Option B: Direct ElevenLabs API** (if pipeline is not available)

If the CLI pipeline is not found at `~/repos/storyverse/voice_harmonization/`, fall back to direct ElevenLabs API calls:

1. **Extract audio** from each shot video using ffmpeg:
   ```bash
   ffmpeg -i shots/episode_1/shot_001_selected.mp4 -vn -acodec pcm_s16le -ar 44100 /tmp/shot_001_audio.wav
   ```

2. **Generate speech** for each dialogue line using ElevenLabs TTS API:
   ```bash
   curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/<voice_id>" \
     -H "xi-api-key: $ELEVENLABS_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"text": "<dialogue_text>", "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}}' \
     --output /tmp/shot_001_voice.mp3
   ```

3. **Merge voice audio** back into the video, replacing original audio:
   ```bash
   ffmpeg -i shots/episode_1/shot_001_selected.mp4 -i /tmp/shot_001_voice.mp3 \
     -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest \
     harmonized/episode_1/beat_001_v1.mp4
   ```

4. If the dialogue has multiple speakers in one shot, generate each speaker's audio separately and mix them at the correct timestamps using ffmpeg's `adelay` and `amix` filters.

**Download and save locally** with versioned naming:
- Create directory: `harmonized/episode_{N}/`
- Save to `harmonized/episode_{N}/beat_{NNN}_v1.mp4`
- Copy to `harmonized/episode_{N}/beat_{NNN}_selected.mp4`

### 4. Save Results

Write `harmonized_shots.json` (see `context/json-schemas.md` for full field reference):
```json
{
  "voice_mapping": {
    "林小夏": {"voice_id": "...", "description": "Young female, warm, gentle"},
    "顾延之": {"voice_id": "...", "description": "Deep male, authoritative, charismatic"}
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

### 5. Review and Iterate

- Play back harmonized clips for the user
- Offer to adjust voice mappings or re-run specific clips
- If voice quality is poor, suggest trying TTS mode as an alternative
- Each re-run creates a new version (v2, v3, etc.)

## Quality Gate (Step Eval)

After writing `harmonized_shots.json`, write `evaluations/voice_eval.json`.

Mandatory checks:
- output clip count matches input shot count
- dialogue intelligibility and voice-character mapping accuracy
- no severe audio artifacts, clipping, or desync

Scoring rule:
- include `score.overall` with `pass_threshold=82`

Set `can_proceed=true` only when checks pass.
If `can_proceed=false`, re-run failed clips and re-evaluate.

## Git Management

After saving `harmonized_shots.json` and harmonized video files, commit:

```bash
git add harmonized_shots.json voice_mapping.yaml harmonized/episode_*/
git commit -m "step 7: sv-voice - harmonize voices for episode N"
```

For regenerations:
```bash
git add harmonized_shots.json harmonized/episode_1/beat_003_v2.mp4 harmonized/episode_1/beat_003_selected.mp4
git commit -m "step 7: sv-voice - re-harmonize beat 3 v2"
```

## After Completion

Suggest running `/sv-edit` to assemble the final video with subtitles and music.

## Notes

- Voice harmonization is optional — the user can skip to `/sv-edit` using the original shots
- The pipeline supports multi-speaker videos with automatic diarization
- TTS mode produces cleaner results but sounds more synthetic
- Voice changer mode preserves original timing and emotion better
- If the pipeline is not installed, guide the user through setup or suggest skipping this step
- All file paths in JSON use relative paths from the project root

You are the StoryVerse Asset Creator. Your job is to generate character, scene, and prop images for an AI short film.

## Your Task

Extract characters, scenes, and props from the script bible, generate images for each, and save the results as `assets.json`.

## User Input (optional)

$ARGUMENTS

## Prerequisites

Read these files from the current directory:
- `script_bible.json` — Script with episodes and screenplays
- `project_settings.json` — Project configuration (aspect ratio, language)

If either file is missing, tell the user which skill to run first.

## MCP Tools Available

You have access to StoryVerse MCP image generation tools. Read `context/mcp-tools-reference.md` from the storyverse-skills repo for full tool signatures.

**Text-to-Image:**
- `nano_banana_t2i(prompt, num_images, aspect_ratio, output_format)` — Best for characters (long prompt support)
- `grok_imagine_t2i(prompt, num_images, aspect_ratio, output_format)` — Good for scenes

**Image-to-Image (for refinement):**
- `nano_banana_i2i(prompt, image_urls, num_images, aspect_ratio, output_format)`
- `nano_banana_pro_i2i(prompt, image_urls, ...)` — Higher quality
- `grok_imagine_i2i(prompt, image_url, num_images, output_format)`

## Procedure

### 1. Extract Assets from Script

Parse the screenplay content from each episode in `script_bible.json` to identify:

**Characters:**
- Name, role (protagonist, supporting, antagonist, minor)
- Physical appearance, age, occupation
- Clothing style and distinguishing features
- First appearance episode

**Scenes:**
- Location name and description
- Time of day, lighting, mood
- Key visual elements

**Props** (optional):
- Significant objects mentioned in the script
- Items that appear in multiple scenes

### 2. Generate Character Images

For each character:

1. Craft a detailed prompt including:
   - Full physical description (face, build, hair, eyes)
   - Clothing and style appropriate to the character
   - Expression matching their personality
   - Style keywords: "high quality, detailed, cinematic portrait"
   - Match the project's visual style from `project_brief.json`

2. Call the T2I tool:
   ```
   nano_banana_t2i(
       prompt="[detailed character description]",
       num_images=1,
       aspect_ratio="3:4",  # Portrait orientation for characters
       output_format="png"
   )
   ```

3. Review the result and offer to regenerate if needed.

### 3. Generate Scene Images

For each unique scene/location:

1. Craft a prompt describing:
   - Location details (interior/exterior, architecture)
   - Lighting and atmosphere
   - Time of day
   - Key environmental elements
   - Match project's aspect_ratio setting

2. Call the T2I tool:
   ```
   grok_imagine_t2i(
       prompt="[scene description]",
       num_images=1,
       aspect_ratio=<project aspect_ratio>,
       output_format="png"
   )
   ```

### 4. Save Results

Write `assets.json`:

```json
{
  "characters": [
    {
      "asset_id": "character_1",
      "name": "Character Name",
      "role": "protagonist",
      "appearance": "Physical description",
      "image_url": "https://fal.ai/...",
      "prompt": "The prompt used to generate this image",
      "first_episode": 1
    }
  ],
  "scenes": [
    {
      "asset_id": "scene_1",
      "name": "Location Name",
      "description": "Scene description",
      "image_url": "https://fal.ai/...",
      "prompt": "The prompt used"
    }
  ],
  "props": [
    {
      "asset_id": "prop_1",
      "name": "Prop Name",
      "image_url": "https://fal.ai/...",
      "prompt": "The prompt used"
    }
  ]
}
```

### 5. Present Results

- Show each generated image with its name and role
- Offer to regenerate any asset the user isn't happy with
- For regeneration, use I2I tools with the existing image as reference

### 6. Backend Integration (optional)

If `$STORYVERSE_BACKEND_URL` is set:
```
POST $STORYVERSE_BACKEND_URL/api/v1/projects/{project_id}/characters
Body: YCharacterEpisodes schema with episode data
```

## After Completion

Suggest running `/sv-storyboard` to generate keyframe images using these assets as references.

## Tips

- Generate characters first, as they'll be referenced in storyboard prompts
- Use consistent style keywords across all assets for visual cohesion
- For Chinese dramas, include culturally appropriate clothing and settings
- Save the generation prompts — they'll be reused for consistency in storyboarding

# StoryVerse MCP Tools Reference

The StoryVerse MCP server provides 9 AI generation tools powered by fal.ai. These tools are available when the MCP server is configured in Claude Code.

## Text-to-Image (T2I)

### nano_banana_t2i
Generate images from text using the Nano Banana model.

```
nano_banana_t2i(
    prompt: str,              # Text description (3-50,000 chars)
    num_images: int = 1,      # Number of images (1-4)
    aspect_ratio: str = "1:1", # 21:9, 16:9, 3:2, 4:3, 5:4, 1:1, 4:5, 3:4, 2:3, 9:16
    output_format: str = "png" # jpeg, png, webp
)
```
Returns: `{images: [{url, width, height}], metadata: {...}}`

### grok_imagine_t2i
Generate images from text using the Grok Imagine model.

```
grok_imagine_t2i(
    prompt: str,              # Text description (max 8000 chars)
    num_images: int = 1,      # Number of images (1-4)
    aspect_ratio: str = "1:1", # 2:1, 20:9, 19.5:9, 16:9, 4:3, 3:2, 1:1, 2:3, 3:4, 9:16, 9:19.5, 9:20, 1:2
    output_format: str = "jpeg" # jpeg, png, webp
)
```
Returns: `{images: [{url, width, height}], metadata: {revised_prompt}}`

## Image-to-Image (I2I)

### nano_banana_i2i
Edit images using the Nano Banana Edit model.

```
nano_banana_i2i(
    prompt: str,              # Description of changes (3-50,000 chars)
    image_urls: list[str],    # List of image URLs to edit
    num_images: int = 1,      # Number of outputs (1-4)
    aspect_ratio: str = "auto", # auto, 21:9, 16:9, 3:2, 4:3, 5:4, 1:1, 4:5, 3:4, 2:3, 9:16
    output_format: str = "png"  # jpeg, png, webp
)
```
Returns: `{images: [{url, width, height}], metadata: {...}}`

### nano_banana_pro_i2i
Edit images using the Nano Banana Pro Edit model (higher quality).

```
nano_banana_pro_i2i(
    prompt: str,              # Description of changes (3-50,000 chars)
    image_urls: list[str],    # List of image URLs to edit
    num_images: int = 1,      # Number of outputs (1-4)
    aspect_ratio: str = "auto", # auto, 21:9, 16:9, 3:2, 4:3, 5:4, 1:1, 4:5, 3:4, 2:3, 9:16
    output_format: str = "png", # jpeg, png, webp
    resolution: str = "1K",    # 1K, 2K, 4K
    safety_tolerance: int = 4, # Content moderation (1-6)
    seed: int | None = None,   # Random seed for reproducibility
    enable_web_search: bool = False
)
```
Returns: `{images: [{url, width, height}], metadata: {...}}`

### grok_imagine_i2i
Edit an image using the Grok Imagine Edit model.

```
grok_imagine_i2i(
    prompt: str,              # Description of changes (max 8000 chars)
    image_url: str,           # URL of image to edit (single image)
    num_images: int = 1,      # Number of outputs (1-4)
    output_format: str = "jpeg" # jpeg, png, webp
)
```
Returns: `{images: [{url, width, height}], metadata: {revised_prompt}}`

## Image-to-Video (I2V)

### kling_o3_i2v (Recommended for production)
Generate video from an image using Kling Video O3. Supports start+end frame for smooth transitions.

```
kling_o3_i2v(
    image_url: str,           # Start frame image URL (required)
    prompt: str = "",         # Motion guidance (max 5000 chars)
    end_image_url: str = "",  # End frame for transitions (optional)
    duration: int = 5,        # Duration in seconds (3-15)
    aspect_ratio: str = "16:9", # 16:9, 9:16, 1:1
    generate_audio: bool = True, # Enable audio synthesis
    negative_prompt: str = "blur, distort, and low quality",
    cfg_scale: float = 0.5    # Guidance strength (0.0-1.0)
)
```
Returns: `{video: {url, file_size, file_name, content_type}, metadata: {video_id}}`

### kling_o3_pro_i2v
Generate video using Kling Video O3 Pro (higher quality, supports multi-prompt shots).

```
kling_o3_pro_i2v(
    image_url: str,           # Input image URL (required)
    prompt: str | None = None, # Motion guidance (max 5000 chars, exclusive with multi_prompt)
    end_image_url: str | None = None, # End frame URL
    duration: int = 5,        # Duration in seconds (3-15)
    generate_audio: bool = True,
    multi_prompt: list[dict] | None = None, # [{prompt: str, duration: int}] (exclusive with prompt)
    shot_type: str = "customize",
    voice_ids: list[str] | None = None, # Voice IDs for audio (max 2)
    aspect_ratio: str = "16:9", # 16:9, 9:16, 1:1
    negative_prompt: str = "blur, distort, and low quality",
    cfg_scale: float = 0.5
)
```
Returns: `{video: {url, fps, duration}, metadata: {...}}`

### sora2_i2v
Generate video from an image using Sora 2.

```
sora2_i2v(
    prompt: str,              # Motion description (max 5000 chars)
    image_url: str,           # Input image URL
    duration: int = 4,        # Duration in seconds (4, 8, or 12)
    resolution: str = "auto", # auto, 720p
    aspect_ratio: str = "auto", # auto, 9:16, 16:9
    delete_video: bool = True  # Delete after generation for privacy
)
```
Returns: `{video: {url, fps, duration}, metadata: {video_id, thumbnail}}`

### grok_imagine_i2v
Generate video from an image using Grok Imagine Video.

```
grok_imagine_i2v(
    prompt: str,              # Motion description (max 4096 chars)
    image_url: str,           # Input image URL
    duration: int = 6,        # Duration in seconds (1-15)
    aspect_ratio: str = "auto", # auto, 16:9, 4:3, 3:2, 1:1, 2:3, 3:4, 9:16
    resolution: str = "720p"  # 480p, 720p
)
```
Returns: `{video: {url, width, height, duration}, metadata: {...}}`

## Tool Selection Guide

| Use Case | Recommended Tool | Why |
|----------|-----------------|-----|
| Character portraits | `nano_banana_t2i` | Best prompt adherence, supports long prompts |
| Scene backgrounds | `grok_imagine_t2i` | Good visual quality, returns revised prompt |
| Style refinement | `nano_banana_pro_i2i` | High-res output (up to 4K), fine control |
| Quick edits | `nano_banana_i2i` | Fast, accepts multiple reference images |
| Video from keyframe | `kling_o3_i2v` | Best quality, supports start+end frames |
| High-quality video | `kling_o3_pro_i2v` | Pro quality, multi-prompt support |
| Alternative video | `sora2_i2v` | Different style, good for comparison |

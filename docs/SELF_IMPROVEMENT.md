# StoryVerse Self-Improvement System

This document describes how StoryVerse learns from user feedback to continuously improve AI-generated content quality.

## Overview

The self-improvement system collects structured feedback on AI-generated content (images, videos, scripts, voice) and uses this data to:

1. **Identify patterns** in quality issues
2. **Optimize prompts** and generation parameters
3. **Select better models** for each content type
4. **Track quality trends** over time
5. **Build datasets** for training and evaluation

## Architecture

```
┌─────────────────┐
│  User Feedback  │
│   (/sv-judge)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│ Quality Ratings │─────▶│  LangSmith API   │
│  + Comments     │      │   (Datasets)     │
└────────┬────────┘      └────────┬─────────┘
         │                        │
         ▼                        ▼
┌─────────────────┐      ┌──────────────────┐
│ Local JSON      │      │  Cloud Storage   │
│ quality_*.json  │      │  + Analytics     │
└────────┬────────┘      └────────┬─────────┘
         │                        │
         └────────┬───────────────┘
                  ▼
         ┌────────────────┐
         │    Insights    │
         │   Generation   │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │  Improvements  │
         │ • Prompts      │
         │ • Models       │
         │ • Parameters   │
         └────────────────┘
```

## Components

### 1. Quality Judging Skill (`/sv-judge`)

The `/sv-judge` command is the primary interface for collecting quality feedback:

```bash
# Judge specific content types
/sv-judge assets
/sv-judge storyboard
/sv-judge shots
/sv-judge script
/sv-judge voice

# Judge everything
/sv-judge all
```

**What it does:**
- Displays content for user review
- Collects structured ratings (1-5) across multiple dimensions
- Captures specific issues and user comments
- Saves feedback to local JSON files
- Logs feedback to LangSmith datasets
- Generates quality insights and recommendations

### 2. LangSmith Integration

LangSmith provides cloud-based dataset management and analytics:

**Setup:**
```bash
# Install LangSmith
pip install langsmith

# Set environment variables
export LANGSMITH_API_KEY="your-api-key"
export LANGSMITH_PROJECT="storyverse-quality"
```

**Benefits:**
- Persistent storage of feedback across sessions
- Team-wide visibility into quality metrics
- Built-in analytics and visualization
- API access for automated analysis
- Integration with LangChain applications

### 3. Quality Feedback Logger (`utils/langsmith_feedback.py`)

Python utility module for programmatic feedback logging:

```python
from utils import QualityFeedbackLogger

logger = QualityFeedbackLogger()

# Log image feedback
logger.log_image_feedback(
    dataset_name="storyverse-assets",
    image_path="assets/character.png",
    prompt="Character description...",
    model="flux-pro-1.1",
    ratings={
        "prompt_adherence": 4,
        "technical_quality": 5,
        "aesthetic_quality": 4,
        "character_consistency": 4
    },
    issues=[{"description": "Minor color issue", "severity": "minor"}],
    user_comments="Good overall"
)

# Generate insights
insights = logger.generate_insights("storyverse-assets")
```

## Quality Dimensions

### Images (Assets, Storyboard)
- **Prompt Adherence** (1-5): Matches prompt description
- **Technical Quality** (1-5): Resolution, clarity, no artifacts
- **Aesthetic Quality** (1-5): Composition, lighting, color
- **Character Consistency** (1-5): Matches reference images
- **Scene Accuracy** (1-5): Matches scene description

### Videos (Shots)
- **Motion Quality** (1-5): Natural movement, no artifacts
- **Prompt Adherence** (1-5): Follows I2V motion prompt
- **Temporal Consistency** (1-5): No flickering or jumps
- **Technical Quality** (1-5): Resolution, frame rate
- **Aesthetic Quality** (1-5): Cinematography

### Scripts
- **Story Coherence** (1-5): Logical plot flow
- **Character Development** (1-5): Character arcs and depth
- **Dialogue Quality** (1-5): Natural, engaging dialogue
- **Pacing** (1-5): Appropriate length and beats
- **Genre Adherence** (1-5): Matches target channel

### Voice (Harmonization)
- **Voice Match** (1-5): Matches character persona
- **Audio Quality** (1-5): Clarity, no artifacts
- **Emotional Tone** (1-5): Matches scene emotion
- **Pronunciation** (1-5): Clear and correct

## Quality Categories

Based on average scores:
- **Excellent** (4.5+): Outstanding quality, use as reference
- **Good** (3.5-4.5): Acceptable quality, minor improvements possible
- **Acceptable** (3.0-3.5): Usable, but could be better
- **Needs Rework** (<3.0): Should be regenerated

## Feedback Workflow

### 1. Content Generation
```bash
/sv-assets    # Generate character/scene images
/sv-storyboard # Generate keyframes
/sv-shots     # Generate video clips
/sv-script    # Generate screenplay
```

### 2. Quality Judging
```bash
/sv-judge all  # Evaluate all generated content
```

The skill will:
- Display each item for review
- Ask for ratings on each quality dimension
- Collect issues and comments
- Calculate quality scores
- Log to LangSmith

### 3. Review Results

Check `quality_feedback.json` for detailed feedback:
```json
{
  "overall_summary": {
    "total_items_evaluated": 8,
    "excellent_count": 2,
    "good_count": 5,
    "acceptable_count": 1,
    "needs_rework_count": 0,
    "average_quality_score": 4.1
  }
}
```

### 4. Generate Insights
```bash
python -c "
from utils import QualityFeedbackLogger
logger = QualityFeedbackLogger()
insights = logger.generate_insights('storyverse-assets')
"
```

Check `quality_insights.json` for patterns and recommendations:
```json
{
  "common_issues": [
    {"description": "Character consistency", "frequency": 12}
  ],
  "model_performance": {
    "flux-pro-1.1": {"avg_score": 4.3, "samples": 45},
    "flux-dev": {"avg_score": 3.8, "samples": 30}
  },
  "recommendations": [
    "Best performing model: flux-pro-1.1",
    "Consider stronger character reference prompts"
  ]
}
```

### 5. Apply Improvements

Based on insights:
- **Regenerate low-quality items**: Use items in `items_to_regenerate` list
- **Update prompts**: Apply recommendations from insights
- **Switch models**: Use best-performing models
- **Adjust parameters**: Fine-tune generation parameters

### 6. Iterate

Run the cycle again to verify improvements:
```bash
/sv-assets     # Regenerate with improved prompts
/sv-judge assets  # Re-evaluate
```

## Learning from Feedback

### Prompt Optimization

**Before:**
```json
{
  "prompt": "A businessman",
  "avg_score": 3.2
}
```

**Analysis:** Low score due to vague description

**After:**
```json
{
  "prompt": "A handsome Chinese businessman in his 30s with short black hair, wearing a tailored black suit and white shirt, confident expression, studio lighting",
  "avg_score": 4.5
}
```

### Model Selection

Track model performance over time:
```python
model_performance = {
    "flux-pro-1.1": {"avg_score": 4.3, "samples": 45},
    "flux-dev": {"avg_score": 3.8, "samples": 30},
    "flux-schnell": {"avg_score": 3.5, "samples": 20}
}
# Decision: Use flux-pro-1.1 as default
```

### Parameter Tuning

Identify optimal parameters:
```python
seed_performance = {
    12345: {"avg_score": 4.5},
    67890: {"avg_score": 3.8},
    # Finding: Certain seeds produce better results
}

aspect_ratio_performance = {
    "9:16": {"avg_score": 4.2},  # Better for mobile
    "16:9": {"avg_score": 4.0}
}
```

## LangSmith Datasets

### Dataset Structure

**storyverse-assets**
- Character images
- Scene images
- Prop images

**storyverse-storyboard**
- Keyframe images
- Shot composition

**storyverse-shots**
- Video clips
- I2V generations

**storyverse-script**
- Episode scripts
- Dialogue quality

**storyverse-voice**
- Voice harmonization
- Audio quality

### Dataset Schema

Each example contains:
```json
{
  "inputs": {
    "content_type": "image|video|script",
    "prompt": "Generation prompt",
    "model": "Model name",
    "parameters": {...},
    "file_path": "Path to file",
    "image_base64": "Base64 encoded image (optional)"
  },
  "outputs": {
    "expected_quality": "excellent|good|acceptable|needs_rework"
  },
  "metadata": {
    "ratings": {...},
    "average_score": 4.2,
    "quality_category": "good",
    "issues": [...],
    "user_comments": "...",
    "feedback_date": "2026-02-14T10:30:00Z",
    "project_id": "..."
  }
}
```

## Advanced Features

### Automated Quality Prediction

Once enough feedback is collected, train a quality prediction model:

```python
from langsmith import Client

client = Client()
dataset = client.read_dataset(dataset_name="storyverse-assets")

# Use examples to train a classifier
# Predict quality before showing to user
# Auto-regenerate predicted low-quality items
```

### A/B Testing

Compare different models or prompts:

```python
# Generate same content with different models
model_a_score = generate_and_judge(model="flux-pro")
model_b_score = generate_and_judge(model="flux-dev")

# Log both to LangSmith for comparison
```

### Quality Trends

Track improvement over time:

```python
# Query feedback by date
jan_feedback = query_feedback(date_range="2026-01")
feb_feedback = query_feedback(date_range="2026-02")

# Compare average scores
jan_avg = 3.8
feb_avg = 4.2  # Improvement!
```

### Team Learning

Share insights across team:
- Export insights JSON to shared storage
- Review common issues in team meetings
- Update prompt guidelines in `context/conventions.md`
- Add successful patterns to skill prompts

## Best Practices

### 1. Consistent Rating Standards
- Calibrate ratings across team members
- Use examples as reference points
- Document rating criteria clearly

### 2. Actionable Feedback
- Describe specific issues, not just scores
- Suggest fixes when possible
- Include context (what was expected vs actual)

### 3. Regular Evaluation
- Judge content immediately after generation
- Don't wait until full project completion
- Catch issues early to avoid rework

### 4. Diverse Samples
- Collect feedback on various content types
- Include edge cases and challenging scenarios
- Balance positive and negative examples

### 5. Iterate Rapidly
- Apply improvements quickly
- Test changes with new generations
- Track before/after metrics

## Metrics Dashboard

Key metrics to track:

### Quality Metrics
- **Average Quality Score**: Overall system performance
- **Quality Distribution**: % in each category
- **Trend Over Time**: Improving or declining?

### Efficiency Metrics
- **Regeneration Rate**: % items needing rework
- **First-Pass Success Rate**: % acceptable on first try
- **Time to Quality**: Iterations needed to reach target

### Model Metrics
- **Model Performance**: Avg score by model
- **Model Cost**: Cost per generation
- **Model ROI**: Quality per dollar spent

### Prompt Metrics
- **Prompt Effectiveness**: Score by prompt pattern
- **Prompt Length**: Optimal prompt length
- **Keyword Impact**: Which terms improve scores

## Integration with Pipeline

The self-improvement system integrates with the full StoryVerse pipeline:

```bash
# Full workflow with quality checks
/sv-pipeline --with-quality-checks

# This will:
# 1. Generate content at each step
# 2. Auto-judge quality (if LANGSMITH_API_KEY set)
# 3. Regenerate items below threshold
# 4. Log all feedback to LangSmith
# 5. Generate insights report
```

## Troubleshooting

### Issue: LangSmith API key not found
```bash
export LANGSMITH_API_KEY="your-key-here"
```

### Issue: Package not installed
```bash
pip install -r requirements.txt
```

### Issue: Dataset not accessible
Check that the dataset exists in your LangSmith project

### Issue: Image upload fails
Large images may timeout. Set `upload_image=False` in logger

## Resources

- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [LangSmith Datasets Guide](https://docs.smith.langchain.com/evaluation/datasets)
- [Quality Feedback Logger API](../utils/langsmith_feedback.py)
- [sv-judge Skill](../.claude/commands/sv-judge.md)

## Future Enhancements

### Planned Features
- [ ] Automated quality prediction (skip manual judgment)
- [ ] Real-time quality alerts during generation
- [ ] Quality-based model routing (auto-select best model)
- [ ] Prompt auto-optimization using feedback
- [ ] Integration with human labeling platforms
- [ ] Quality benchmarking against industry standards
- [ ] Multi-modal quality evaluation (vision + language models)
- [ ] Continuous learning pipeline with automated retraining

---

**Remember:** The system gets better the more feedback you provide. Regular quality judging creates a virtuous cycle of continuous improvement!

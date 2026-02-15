"""
Style Playbook Retriever for StoryVerse

Loads style playbook YAML files and retrieves matching playbooks
based on genre tags, mood tags, and keyword matching.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Any

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class StylePlaybookRetriever:
    """Loads and retrieves style playbooks from YAML files."""

    def __init__(self, playbook_dir: Optional[str] = None):
        """
        Initialize the retriever by loading all playbook YAML files.

        Args:
            playbook_dir: Path to the style_playbooks/ directory.
                          Defaults to style_playbooks/ relative to repo root.
        """
        if not YAML_AVAILABLE:
            raise ImportError("PyYAML is required. Install: pip install pyyaml")

        if playbook_dir is None:
            repo_root = Path(__file__).parent.parent
            playbook_dir = str(repo_root / "style_playbooks")

        self.playbook_dir = Path(playbook_dir)
        self.playbooks: Dict[str, Dict[str, Any]] = {}
        self._load_all()

    def _load_all(self) -> None:
        """Load all YAML playbook files from the directory."""
        if not self.playbook_dir.exists():
            return

        for yaml_file in sorted(self.playbook_dir.glob("*.yaml")):
            if yaml_file.name == "playbook_schema.yaml":
                continue
            try:
                with open(yaml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                if data and isinstance(data, dict) and "id" in data:
                    self.playbooks[data["id"]] = data
            except Exception as e:
                print(f"Warning: Failed to load {yaml_file.name}: {e}")

    def get(self, playbook_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a playbook by its ID.

        Args:
            playbook_id: The playbook's unique ID (e.g., "roar_of_steel")

        Returns:
            Playbook dict or None if not found.
        """
        return self.playbooks.get(playbook_id)

    def list_all(self) -> List[Dict[str, str]]:
        """
        List all available playbooks with summary info.

        Returns:
            List of dicts with id, name, genre, mood, visual_style.
        """
        return [
            {
                "id": pb["id"],
                "name": pb.get("name", pb["id"]),
                "genre": pb.get("genre", []),
                "mood": pb.get("mood", []),
                "visual_style": pb.get("visual_style", "mvp"),
            }
            for pb in self.playbooks.values()
        ]

    def retrieve(
        self,
        genre: Optional[str] = None,
        mood: Optional[str] = None,
        visual_style: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        limit: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve matching playbooks by genre, mood, visual_style, and keywords.

        Scoring:
        - +2 for each genre tag match
        - +2 for each mood tag match
        - +3 for visual_style match
        - +1 for each keyword found in name/description/tone

        Args:
            genre: Genre string (e.g., "action", "thriller").
                   Can be comma-separated for multiple genres.
            mood: Mood string (e.g., "tense", "heroic").
                  Can be comma-separated for multiple moods.
            visual_style: Visual style filter (mvp, threed, liveaction, anime).
            keywords: Additional keywords to match against name/description.
            limit: Max number of results to return.

        Returns:
            List of playbook dicts sorted by relevance score (highest first).
        """
        genre_tags = _split_tags(genre) if genre else []
        mood_tags = _split_tags(mood) if mood else []
        kw_list = [k.lower() for k in (keywords or [])]

        scored = []
        for pb in self.playbooks.values():
            score = 0
            pb_genres = [g.lower() for g in pb.get("genre", [])]
            pb_moods = [m.lower() for m in pb.get("mood", [])]
            pb_vs = pb.get("visual_style", "").lower()

            for g in genre_tags:
                if g in pb_genres:
                    score += 2

            for m in mood_tags:
                if m in pb_moods:
                    score += 2

            if visual_style and pb_vs == visual_style.lower():
                score += 3

            searchable = " ".join([
                pb.get("name", ""),
                pb.get("description", ""),
                pb.get("tone", ""),
                " ".join(pb.get("genre", [])),
                " ".join(pb.get("mood", [])),
            ]).lower()
            for kw in kw_list:
                if kw in searchable:
                    score += 1

            if score > 0:
                scored.append((score, pb))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [pb for _, pb in scored[:limit]]

    def format_for_prompt(self, playbook: Dict[str, Any]) -> str:
        """
        Format a playbook into a text block suitable for injection into
        the VideoShot agent's generation prompt.

        Args:
            playbook: A playbook dict loaded from YAML.

        Returns:
            Formatted string with style constraints and reference examples.
        """
        lines = []
        lines.append(f"## Style Reference: {playbook.get('name', playbook['id'])}")
        lines.append("")
        lines.append(f"**Tone**: {playbook.get('tone', 'N/A')}")
        lines.append(f"**Pacing**: {playbook.get('pacing', 'N/A')}")
        lines.append(f"**Intensity Curve**: {playbook.get('intensity_curve', 'N/A')}")
        lines.append("")

        # Camera preferences
        cameras = playbook.get("camera_phrase_whitelist", [])
        if cameras:
            lines.append("**Preferred Camera Tags** (prioritize these from SHOT_LANGUAGE_BANK_V1):")
            for cam in cameras:
                lines.append(f"  - {cam}")
            lines.append("")

        # Motion carriers
        carriers = playbook.get("motion_carriers", [])
        if carriers:
            lines.append("**Motion Carriers** (use at least one per segment):")
            for mc in carriers:
                lines.append(f"  - {mc}")
            lines.append("")

        # Consistency rules
        rules = playbook.get("consistency_rules", [])
        if rules:
            lines.append("**Consistency Rules**:")
            for rule in rules:
                lines.append(f"  - {rule}")
            lines.append("")

        # Dialogue density
        dd = playbook.get("dialogue_density_rules", {})
        if dd:
            lines.append("**Dialogue Density**:")
            lines.append(f"  - Max lines/beat: {dd.get('max_lines_per_beat', 'N/A')}")
            lines.append(f"  - Max chars/beat: {dd.get('max_chars_per_beat', 'N/A')}")
            lines.append(f"  - Text policy: {dd.get('on_screen_text_policy', 'N/A')}")
            lines.append("")

        # Segment pacing
        sp = playbook.get("segment_pacing", {})
        if sp:
            lines.append("**Segment Pacing Overrides**:")
            for rhythm, pattern in sp.items():
                lines.append(f"  - {rhythm}: {'+'.join(str(s) for s in pattern)}s")
            lines.append("")

        # Reference beat (first one only, to stay within prompt limits)
        ref_beats = playbook.get("reference_beats", [])
        if ref_beats:
            beat = ref_beats[0]
            lines.append("**Reference Beat Example**:")
            lines.append(f"  generation_prompt: \"{beat.get('generation_prompt', '')}\"")
            for seg in beat.get("shot_plan", []):
                lines.append(f"  {seg['t']} | {seg['camera']} — {seg['action']}")
            lines.append("")

        return "\n".join(lines)


def _split_tags(tag_str: str) -> List[str]:
    """Split a comma-separated or space-separated tag string into a list."""
    tags = []
    for part in tag_str.replace(",", " ").split():
        cleaned = part.strip().lower()
        if cleaned:
            tags.append(cleaned)
    return tags

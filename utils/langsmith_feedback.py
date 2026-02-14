"""
LangSmith Integration for StoryVerse Quality Feedback

This module provides utilities for logging quality feedback to LangSmith
to enable continuous improvement of AI-generated content.
"""

import os
import json
import base64
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from uuid import uuid4

try:
    from langsmith import Client
    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False
    print("Warning: langsmith package not installed. Run: pip install langsmith")


class QualityFeedbackLogger:
    """Logs quality feedback to LangSmith datasets"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        project_name: Optional[str] = None
    ):
        """
        Initialize LangSmith client

        Args:
            api_key: LangSmith API key (defaults to LANGSMITH_API_KEY env var)
            project_name: Project name (defaults to LANGSMITH_PROJECT env var or "storyverse-quality")
        """
        if not LANGSMITH_AVAILABLE:
            raise ImportError("langsmith package required. Install: pip install langsmith")

        self.api_key = api_key or os.getenv("LANGSMITH_API_KEY")
        if not self.api_key:
            raise ValueError("LANGSMITH_API_KEY environment variable or api_key parameter required")

        self.project_name = project_name or os.getenv("LANGSMITH_PROJECT", "storyverse-quality")
        self.client = Client(api_key=self.api_key)

    def get_or_create_dataset(self, dataset_name: str, description: str = "") -> Any:
        """Get existing dataset or create new one"""
        try:
            dataset = self.client.read_dataset(dataset_name=dataset_name)
            print(f"Using existing dataset: {dataset_name}")
        except Exception as e:
            print(f"Creating new dataset: {dataset_name}")
            dataset = self.client.create_dataset(
                dataset_name=dataset_name,
                description=description or f"StoryVerse {dataset_name} feedback"
            )
        return dataset

    def log_image_feedback(
        self,
        dataset_name: str,
        image_path: str,
        prompt: str,
        model: str,
        ratings: Dict[str, int],
        generation_params: Dict[str, Any],
        issues: List[Dict[str, str]] = None,
        user_comments: str = "",
        metadata: Dict[str, Any] = None,
        upload_image: bool = True
    ) -> str:
        """
        Log image generation feedback to LangSmith

        Args:
            dataset_name: Name of the dataset
            image_path: Path to the generated image
            prompt: Generation prompt used
            model: Model name used
            ratings: Quality ratings dict (e.g., {"prompt_adherence": 4, "technical_quality": 5})
            generation_params: Generation parameters (seed, aspect_ratio, etc.)
            issues: List of issue dicts with description, severity, suggested_fix
            user_comments: Free text user comments
            metadata: Additional metadata
            upload_image: Whether to upload image as base64

        Returns:
            Example ID from LangSmith
        """
        dataset = self.get_or_create_dataset(
            dataset_name,
            "StoryVerse image quality feedback"
        )

        # Prepare inputs
        inputs = {
            "content_type": "image",
            "prompt": prompt,
            "model": model,
            "parameters": generation_params,
            "file_path": str(image_path)
        }

        # Optionally upload image as base64
        if upload_image and Path(image_path).exists():
            try:
                with open(image_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode()
                    inputs["image_base64"] = f"data:image/png;base64,{image_data}"
            except Exception as e:
                print(f"Warning: Could not upload image: {e}")

        # Calculate average score
        avg_score = sum(ratings.values()) / len(ratings) if ratings else 0

        # Determine quality category
        if avg_score >= 4.5:
            quality_category = "excellent"
        elif avg_score >= 3.5:
            quality_category = "good"
        elif avg_score >= 3.0:
            quality_category = "acceptable"
        else:
            quality_category = "needs_rework"

        # Prepare metadata
        full_metadata = {
            "ratings": ratings,
            "average_score": avg_score,
            "quality_category": quality_category,
            "issues": issues or [],
            "user_comments": user_comments,
            "feedback_date": datetime.now().isoformat(),
            "session_id": str(uuid4()),
            **(metadata or {})
        }

        # Create example
        example = self.client.create_example(
            dataset_id=dataset.id,
            inputs=inputs,
            outputs={"expected_quality": quality_category},
            metadata=full_metadata
        )

        print(f"Logged feedback for {image_path} (score: {avg_score:.2f})")
        return example.id

    def log_video_feedback(
        self,
        dataset_name: str,
        video_path: str,
        prompt: str,
        model: str,
        ratings: Dict[str, int],
        generation_params: Dict[str, Any],
        issues: List[Dict[str, str]] = None,
        user_comments: str = "",
        metadata: Dict[str, Any] = None
    ) -> str:
        """
        Log video generation feedback to LangSmith

        Similar to log_image_feedback but for video content
        """
        dataset = self.get_or_create_dataset(
            dataset_name,
            "StoryVerse video quality feedback"
        )

        inputs = {
            "content_type": "video",
            "prompt": prompt,
            "model": model,
            "parameters": generation_params,
            "file_path": str(video_path)
        }

        avg_score = sum(ratings.values()) / len(ratings) if ratings else 0

        if avg_score >= 4.5:
            quality_category = "excellent"
        elif avg_score >= 3.5:
            quality_category = "good"
        elif avg_score >= 3.0:
            quality_category = "acceptable"
        else:
            quality_category = "needs_rework"

        full_metadata = {
            "ratings": ratings,
            "average_score": avg_score,
            "quality_category": quality_category,
            "issues": issues or [],
            "user_comments": user_comments,
            "feedback_date": datetime.now().isoformat(),
            "session_id": str(uuid4()),
            **(metadata or {})
        }

        example = self.client.create_example(
            dataset_id=dataset.id,
            inputs=inputs,
            outputs={"expected_quality": quality_category},
            metadata=full_metadata
        )

        print(f"Logged feedback for {video_path} (score: {avg_score:.2f})")
        return example.id

    def log_script_feedback(
        self,
        dataset_name: str,
        script_content: str,
        prompt: str,
        model: str,
        ratings: Dict[str, int],
        issues: List[Dict[str, str]] = None,
        user_comments: str = "",
        metadata: Dict[str, Any] = None
    ) -> str:
        """
        Log script generation feedback to LangSmith
        """
        dataset = self.get_or_create_dataset(
            dataset_name,
            "StoryVerse script quality feedback"
        )

        inputs = {
            "content_type": "script",
            "prompt": prompt,
            "model": model,
            "script": script_content[:1000]  # Truncate for display
        }

        avg_score = sum(ratings.values()) / len(ratings) if ratings else 0

        if avg_score >= 4.5:
            quality_category = "excellent"
        elif avg_score >= 3.5:
            quality_category = "good"
        elif avg_score >= 3.0:
            quality_category = "acceptable"
        else:
            quality_category = "needs_rework"

        full_metadata = {
            "ratings": ratings,
            "average_score": avg_score,
            "quality_category": quality_category,
            "issues": issues or [],
            "user_comments": user_comments,
            "feedback_date": datetime.now().isoformat(),
            "session_id": str(uuid4()),
            **(metadata or {})
        }

        example = self.client.create_example(
            dataset_id=dataset.id,
            inputs=inputs,
            outputs={"expected_quality": quality_category},
            metadata=full_metadata
        )

        print(f"Logged script feedback (score: {avg_score:.2f})")
        return example.id

    def log_batch_feedback(
        self,
        dataset_name: str,
        feedback_items: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Log multiple feedback items in batch

        Args:
            dataset_name: Name of dataset
            feedback_items: List of dicts with content_type, path, prompt, model, ratings, etc.

        Returns:
            List of example IDs
        """
        example_ids = []

        for item in feedback_items:
            content_type = item.get("content_type", "unknown")

            if content_type == "image":
                example_id = self.log_image_feedback(
                    dataset_name=dataset_name,
                    image_path=item["path"],
                    prompt=item["prompt"],
                    model=item["model"],
                    ratings=item["ratings"],
                    generation_params=item.get("generation_params", {}),
                    issues=item.get("issues", []),
                    user_comments=item.get("user_comments", ""),
                    metadata=item.get("metadata", {}),
                    upload_image=item.get("upload_image", True)
                )
            elif content_type == "video":
                example_id = self.log_video_feedback(
                    dataset_name=dataset_name,
                    video_path=item["path"],
                    prompt=item["prompt"],
                    model=item["model"],
                    ratings=item["ratings"],
                    generation_params=item.get("generation_params", {}),
                    issues=item.get("issues", []),
                    user_comments=item.get("user_comments", ""),
                    metadata=item.get("metadata", {})
                )
            elif content_type == "script":
                example_id = self.log_script_feedback(
                    dataset_name=dataset_name,
                    script_content=item["content"],
                    prompt=item["prompt"],
                    model=item["model"],
                    ratings=item["ratings"],
                    issues=item.get("issues", []),
                    user_comments=item.get("user_comments", ""),
                    metadata=item.get("metadata", {})
                )
            else:
                print(f"Warning: Unknown content type: {content_type}")
                continue

            example_ids.append(example_id)

        print(f"Logged {len(example_ids)} feedback items to {dataset_name}")
        return example_ids

    def query_feedback(
        self,
        dataset_name: str,
        filters: Dict[str, Any] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Query feedback from dataset

        Args:
            dataset_name: Name of dataset
            filters: Filter criteria (e.g., {"quality_category": "needs_rework"})
            limit: Max results to return

        Returns:
            List of feedback items
        """
        dataset = self.client.read_dataset(dataset_name=dataset_name)
        examples = self.client.list_examples(dataset_id=dataset.id, limit=limit)

        results = []
        for example in examples:
            if filters:
                # Simple filtering by metadata
                matches = all(
                    example.metadata.get(k) == v
                    for k, v in filters.items()
                )
                if not matches:
                    continue

            results.append({
                "id": example.id,
                "inputs": example.inputs,
                "outputs": example.outputs,
                "metadata": example.metadata
            })

        return results

    def generate_insights(
        self,
        dataset_name: str,
        output_path: str = "quality_insights.json"
    ) -> Dict[str, Any]:
        """
        Analyze feedback and generate insights

        Args:
            dataset_name: Name of dataset to analyze
            output_path: Where to save insights JSON

        Returns:
            Insights dict
        """
        examples = self.query_feedback(dataset_name, limit=1000)

        if not examples:
            return {"error": "No feedback data available"}

        # Aggregate statistics
        total_items = len(examples)
        scores = [ex["metadata"].get("average_score", 0) for ex in examples]
        avg_score = sum(scores) / len(scores) if scores else 0

        # Count by quality category
        categories = {}
        for ex in examples:
            cat = ex["metadata"].get("quality_category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1

        # Model performance
        model_scores = {}
        for ex in examples:
            model = ex["inputs"].get("model", "unknown")
            score = ex["metadata"].get("average_score", 0)
            if model not in model_scores:
                model_scores[model] = {"scores": [], "count": 0}
            model_scores[model]["scores"].append(score)
            model_scores[model]["count"] += 1

        model_performance = {
            model: {
                "avg_score": sum(data["scores"]) / len(data["scores"]),
                "samples": data["count"]
            }
            for model, data in model_scores.items()
        }

        # Common issues
        issue_patterns = {}
        for ex in examples:
            for issue in ex["metadata"].get("issues", []):
                desc = issue.get("description", "")
                issue_patterns[desc] = issue_patterns.get(desc, 0) + 1

        # Sort by frequency
        common_issues = sorted(
            issue_patterns.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        # Items to regenerate
        needs_rework = [
            ex["inputs"].get("file_path", "unknown")
            for ex in examples
            if ex["metadata"].get("quality_category") == "needs_rework"
        ]

        insights = {
            "insights_date": datetime.now().isoformat(),
            "dataset_name": dataset_name,
            "total_samples": total_items,
            "average_quality_score": round(avg_score, 2),
            "quality_distribution": categories,
            "model_performance": model_performance,
            "common_issues": [
                {"description": desc, "frequency": count}
                for desc, count in common_issues
            ],
            "items_to_regenerate": needs_rework[:20],  # Top 20
            "recommendations": self._generate_recommendations(
                avg_score, model_performance, common_issues
            )
        }

        # Save to file
        with open(output_path, "w") as f:
            json.dump(insights, f, indent=2)

        print(f"Insights saved to {output_path}")
        return insights

    def _generate_recommendations(
        self,
        avg_score: float,
        model_performance: Dict[str, Dict],
        common_issues: List[tuple]
    ) -> List[str]:
        """Generate actionable recommendations from insights"""
        recommendations = []

        if avg_score < 3.5:
            recommendations.append("Overall quality is below target. Consider prompt improvements or model changes.")
        elif avg_score >= 4.5:
            recommendations.append("Excellent quality! Current approach is working well.")

        # Best model
        if model_performance:
            best_model = max(model_performance.items(), key=lambda x: x[1]["avg_score"])
            recommendations.append(f"Best performing model: {best_model[0]} (avg: {best_model[1]['avg_score']:.2f})")

        # Common issues
        if common_issues:
            top_issue = common_issues[0][0]
            recommendations.append(f"Most common issue: '{top_issue}' - consider targeted improvements")

        return recommendations


def example_usage():
    """Example usage of QualityFeedbackLogger"""

    # Initialize logger
    logger = QualityFeedbackLogger()

    # Log image feedback
    logger.log_image_feedback(
        dataset_name="storyverse-assets",
        image_path="assets/bc_fu_si_nian.png",
        prompt="A handsome Chinese businessman in his 30s wearing a black suit",
        model="flux-pro-1.1",
        ratings={
            "prompt_adherence": 4,
            "technical_quality": 5,
            "aesthetic_quality": 4,
            "character_consistency": 4
        },
        generation_params={"seed": 12345, "aspect_ratio": "9:16"},
        issues=[{"description": "Suit color slightly off", "severity": "minor"}],
        user_comments="Overall good quality"
    )

    # Generate insights
    insights = logger.generate_insights("storyverse-assets")
    print(json.dumps(insights, indent=2))


if __name__ == "__main__":
    example_usage()

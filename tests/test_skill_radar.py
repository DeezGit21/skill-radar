import pytest
"""
Tests for Skill Radar — run with: python -m pytest tests/
"""

import json, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from skill_radar import (
    extract_keywords_from_task,
    score_relevance,
    categorize,
    deduplicate,
    filter_by_min_stars,
)


class TestFilterStars:
    def test_filter_github_under_min_stars(self):
        items = [
            {"name": "org/repo-low", "url": "https://github.com/org/repo-low", "stars": 5, "source": "github"},
            {"name": "org/repo-high", "url": "https://github.com/org/repo-high", "stars": 150, "source": "github"},
        ]
        filtered = filter_by_min_stars(items, min_stars=100)
        assert len(filtered) == 1
        assert filtered[0]["name"] == "org/repo-high"

    def test_filter_preserves_non_github_docs(self):
        items = [
            {"name": "Docs Page", "url": "https://example.com/docs", "stars": 0, "source": "url"},
            {"name": "org/repo-low", "url": "https://github.com/org/repo-low", "stars": 2, "source": "github"},
        ]
        filtered = filter_by_min_stars(items, min_stars=100)
        assert len(filtered) == 1
        assert filtered[0]["name"] == "Docs Page"


class TestKeywords:
    def test_basic(self):
        kws = extract_keywords_from_task("Build a React dashboard with real-time data")
        assert len(kws) >= 3
        assert "react" in kws
        assert "dashboard" in kws
        assert "real-time" in kws or "real" in kws

    def test_stopwords_removed(self):
        kws = extract_keywords_from_task("I want to build a thing")
        assert "the" not in kws
        assert "a" not in kws
        # "want" and "to" are stopwords and should be removed
        assert "want" not in kws
        # "build" and "thing" are content words
        assert "build" in kws

    def test_empty(self):
        assert extract_keywords_from_task("") == []
        assert extract_keywords_from_task("a an the") == []


class TestCategorize:
    def test_mcp(self):
        assert categorize({"name": "mcp-server-web", "description": "A web search MCP server"}) == "MCP Server"

    def test_skill(self):
        assert categorize({"name": "agent-skill", "description": "A useful agent skill"}) == "Agent Skill"

    def test_tool(self):
        assert categorize({"name": "my-cli-tool", "description": "A CLI tool for X"}) == "Tool"

    def test_other(self):
        assert categorize({"name": "something-random", "description": "No match"}) == "Other"


class TestRelevance:
    def test_exact_keyword(self):
        item = {"name": "react-hooks", "description": "Useful React hooks library", "topics": ["react"], "stars": 500}
        assert score_relevance(item, "Build a React app", keywords=["react"]) >= 3

    def test_low_relevance(self):
        item = {"name": "rust-embedded", "description": "Embedded systems in Rust", "topics": [], "stars": 0}
        score = score_relevance(item, "React dashboard", keywords=["react"])
        assert score == 0  # no overlap

    def test_star_bonus(self):
        popular = {"name": "foo", "description": "very popular thing", "topics": [], "stars": 5000}
        unpopular = {"name": "foo", "description": "very popular thing", "topics": [], "stars": 5}
        assert score_relevance(popular, "foo") > score_relevance(unpopular, "foo")


class TestDeduplicate:
    def test_same_url(self):
        items = [
            {"name": "a", "url": "https://github.com/x/y"},
            {"name": "a", "url": "https://github.com/x/y"},
        ]
        assert len(deduplicate(items)) == 1

    def test_different(self):
        items = [
            {"name": "a", "url": "https://github.com/x/y"},
            {"name": "b", "url": "https://github.com/x/z"},
        ]
        assert len(deduplicate(items)) == 2
"""Tests for custom GPT actions in sermon analysis."""

import pytest

from evaluate_tools.rag.custom_gpt_actions import generate_embed_link, analyze_sermon_action


@pytest.mark.description("embed link should be generated correctly from title")
def test_generate_embed_link():
    link = generate_embed_link("Forgiveness and Redemption")
    assert "forgiveness-and-redemption" in link


@pytest.mark.description("analyze_sermon_action should include embed_link when requested")
def test_analyze_sermon_action_embed():
    metadata = {"title": "Grace"}
    result = analyze_sermon_action("text", "give me link", metadata)
    assert "embed_link" in result["metadata"] or "embed_link" in result

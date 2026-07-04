"""Tests for Phase 10: 6 AI tasks."""
import pytest
from app.services.phase10_services import *

class TestPhase10:
    async def test_openai_generation(self):
        result = await LLMIntegration().generate_with_openai("Write test")
        assert "gpt-4" in result
    
    async def test_screenshot_generation(self):
        result = await TestGenerationV3().generate_test_from_screenshot("img.png")
        assert result["confidence"] > 0.8
    
    async def test_screenshot_analysis(self):
        result = await FailureAnalysisV2().analyze_screenshot("img.png")
        assert "root_cause" in result
    
    async def test_jira_generation(self):
        result = await AutoBugReportGeneration().generate_jira_issue({})
        assert "key" in result
    
    async def test_knowledge_ingest(self):
        result = await KnowledgeBaseIntegration().ingest_documents(["doc1", "doc2"])
        assert result["documents_ingested"] == 2
    
    async def test_chat(self):
        result = await ConversationalAI().chat("Hello", {})
        assert "recommend" in result

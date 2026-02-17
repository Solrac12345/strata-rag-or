"""
EN: Thin wrapper around the LLM backend (Bedrock).
FR: Couche mince autour du backend LLM (Bedrock).
"""
from __future__ import annotations

from infrastructure.aws.bedrock_client import BedrockClient


class LLMService:
    def __init__(self, client: BedrockClient) -> None:
        self.client = client

    def generate(self, prompt: str) -> str:
        return self.client.invoke(prompt)
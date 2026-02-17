"""
EN: AWS Bedrock client stub (returns natural-sounding answers when BEDROCK_USE_REAL=false).
FR: Stub du client AWS Bedrock (renvoie des réponses naturelles quand BEDROCK_USE_REAL=false).
"""
from __future__ import annotations

# EN: Optional real client support (kept here for future use)
# FR: Prise en charge optionnelle du client réel (conservée pour usage futur)
try:
    import boto3  # type: ignore
except Exception:  # pragma: no cover
    boto3 = None

import os


class BedrockClient:
    """
    EN: Minimal Bedrock client. By default (stub mode), it returns a concise, natural sentence
        by extracting the question from the prompt. If you later set BEDROCK_USE_REAL=true
        and have boto3 configured, you can switch to a real call (example shown below).
    FR: Client Bedrock minimal. Par défaut (mode stub), il renvoie une phrase concise et naturelle
        en extrayant la question du prompt. Si vous mettez plus tard BEDROCK_USE_REAL=true
        et configurez boto3, vous pouvez basculer sur un appel réel (exemple ci-dessous).
    """

    def __init__(
        self,
        model_id: str = "anthropic.claude-3-haiku-20240307-v1:0",
        use_real: bool | None = None,
        region: str | None = None,
    ) -> None:
        # EN/FR: Allow env toggles; default is stub mode (safe for local/dev)
        if use_real is None:
            use_real = os.getenv("BEDROCK_USE_REAL", "false").lower() == "true"
        if region is None:
            region = os.getenv("AWS_REGION", "us-east-1")

        self.model_id = model_id
        self.use_real = bool(use_real and boto3 is not None)
        self.region = region
        self._client = None
        if self.use_real:
            # EN: Real client (only if boto3 installed and credentials configured)
            # FR: Client réel (uniquement si boto3 installé et identifiants configurés)
            self._client = boto3.client("bedrock-runtime", region_name=self.region)

    # NOTE: Keeping your original signature to avoid breaking changes.
    def invoke(self, prompt: str) -> str:
        """
        EN: Generate a response. In stub mode, return a friendly, natural sentence based on the question.
        FR: Générer une réponse. En mode stub, retourner une phrase naturelle basée sur la question.
        """
        if self.use_real and self._client is not None:  # pragma: no cover
            try:
                body = {
                    "prompt": prompt,
                    "max_tokens_to_sample": 256,
                    "temperature": 0.2,
                }
                resp = self._client.invoke_model(  # type: ignore[attr-defined]
                    modelId=self.model_id,
                    body=str(body),
                    contentType="application/json",
                    accept="application/json",
                )
                data = resp.get("body", b"")  # type: ignore
                return f"[Bedrock Response] {data!r}"
            except Exception as e:
                # EN/FR: Fail safe back to stub
                return f"(Stub fallback) Unable to call Bedrock: {e}"

        # ---------- STUB MODE (natural sentence) ----------
        # EN: Try to extract the "Question:" section from the prompt
        # FR: Tenter d'extraire la section "Question:" du prompt
        question = None
        lower = prompt.lower()
        if "question:" in lower:
            try:
                # EN: Split between 'Question:' and 'Context:' if present
                # FR: Découper entre 'Question:' et 'Context:' si présent
                q_part = prompt.split("Question:", 1)[-1]
                if "Context:" in q_part:
                    q_part = q_part.split("Context:", 1)[0]
                question = q_part.replace("Answer:", "").replace("Réponse:", "").replace("\r", " ").replace("\n", " ").strip(" \"'“”‘’")  # Clean up
            except Exception:
                question = None

        if not question:
            # EN/FR: Fallback if the prompt format is unexpected
            question = "your question"

        # EN: Produce a short, natural-sounding answer
        # FR: Produire une réponse brève et naturelle
        return (
            f"(Stub LLM) Based on the retrieved context, a concise answer to '{question}' is: "
            f"RAG retrieves relevant documents and uses them to ground the model’s response."
        )

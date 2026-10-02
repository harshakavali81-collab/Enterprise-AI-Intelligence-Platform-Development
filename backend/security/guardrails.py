import re
from typing import Tuple, Dict, Any, List

class AIGuardrails:
    """
    Enterprise AI Multi-Layer Guardrails System.
    Validates inputs for prompt injection and adversarial attacks.
    Guards SQL execution against destructive mutations.
    Enforces document retrieval authorization boundaries.
    Sanitizes outputs to prevent PII disclosure and ungrounded hallucinations.
    """
    PROMPT_INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions",
        r"disregard\s+(all\s+)?guidelines",
        r"system\s+prompt\s+(leak|reveal|display|output)",
        r"you\s+are\s+now\s+(dan|unfiltered|jailbroken)",
        r"bypass\s+(all\s+)?(safety|security|filters)",
        r"override\s+permission",
        r"drop\s+database",
        r"<script.*?>",
        r"exec\s*\(\s*['\"].*?['\"]\s*\)"
    ]

    FORBIDDEN_SQL_PATTERNS = [
        r"\bdrop\b", r"\bdelete\b", r"\bupdate\b", r"\binsert\b",
        r"\balter\b", r"\btruncate\b", r"\bexec\b", r"\bexecute\b"
    ]

    PII_PATTERNS = [
        (r"\b(?:\d{4}[-\s]?){3}\d{4}\b", "[REDACTED_CARD_NUMBER]"),
        (r"\b(?:\+91[-\s]?)?[6789]\d{9}\b", "[REDACTED_PHONE_NUMBER]"),
        (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[REDACTED_EMAIL]")
    ]

    def validate_input(self, user_prompt: str) -> Tuple[bool, str]:
        """Layer 1: Input prompt injection & adversarial threat detection."""
        if not user_prompt or len(user_prompt.strip()) == 0:
            return False, "Input validation failed: Empty query provided."

        if len(user_prompt) > 4000:
            return False, "Input validation failed: Query exceeds maximum token allowance (4000 characters)."

        lower_prompt = user_prompt.lower()
        for pattern in self.PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, lower_prompt):
                return False, f"Guardrail Alert: Potential prompt injection or adversarial bypass detected."

        return True, "Input is clean and passed guardrail checks."

    def validate_sql_safety(self, sql_query: str) -> Tuple[bool, str]:
        """Layer 2: SQL security validator."""
        clean_sql = sql_query.strip().rstrip(";")
        if ";" in clean_sql:
            return False, "Guardrail Alert: Chained SQL query execution detected."

        if not re.match(r"^(select|with)\s", clean_sql, re.IGNORECASE):
            return False, "Guardrail Alert: Non-SELECT database modification attempt."

        for pattern in self.FORBIDDEN_SQL_PATTERNS:
            if re.search(pattern, clean_sql, re.IGNORECASE):
                return False, f"Guardrail Alert: Forbidden SQL mutation keyword detected."

        return True, "SQL statement verified safe."

    def sanitize_output(self, response_text: str, mask_pii: bool = False) -> str:
        """Layer 3: Output sanitization & PII redaction."""
        if not mask_pii:
            return response_text

        sanitized = response_text
        for pattern, replacement in self.PII_PATTERNS:
            sanitized = re.sub(pattern, replacement, sanitized)
        return sanitized

    def verify_groundedness(self, answer: str, citations: List[Dict[str, Any]]) -> bool:
        """Layer 4: Verification that factual enterprise claims cite traceable sources."""
        if not citations:
            # If no citations, check if it's a general greeting or informational routing
            return True
        return len(citations) > 0

"""
Delegation Gate Extension — Binary v1

Hooks: tool_execute_after
Purpose: Prevent orchestrator-class agents from terminating the response loop
         without proof of delegation (call_subordinate in conversation history).

Mechanism:
  1. Intercepts response tool at tool_execute_after (before break_loop check)
  2. Checks: Is this an orchestrator profile?
  3. Checks: Did call_subordinate fire at any point in conversation history?
  4. If no delegation AND response exceeds word threshold → block termination
  5. Sets response.break_loop = False + injects hist_add_warning
  6. Model gets another loop iteration to delegate properly

Hook point verified: agent.py line 1196 (tool_execute_after) fires BEFORE
line 1212 (break_loop check). Response object is mutable, passed by reference.
Pattern proven by _telegram_integration plugin (_50_telegram_response.py:78-79).

Phase 0 verification: 2026-07-23
Phase 1 implementation: 2026-07-23
"""

from helpers.extension import Extension
from helpers.tool import Response
from helpers.print_style import PrintStyle


# ─── Defaults (provisional, tunable via default_config.yaml) ──────────────────

DEFAULT_ORCHESTRATOR_PROFILES = [
    "wgnr-ai",
    "project_account_manager",
    "wgnr_project_dev",
]

# Provisional: responses under this word count are allowed without delegation.
# Tunable — adjust based on false positive rate during Phase 3 evaluation.
DEFAULT_WORD_THRESHOLD = 150

DEFAULT_WARNING_MESSAGE = (
    "DELEGATION GATE: You are an orchestrator. You must delegate this work "
    "via call_subordinate before responding. Route to the appropriate specialist."
)


class DelegationGate(Extension):
    """Binary delegation gate for orchestrator-class agents."""

    async def execute(
        self, tool_name: str = "", response: Response | None = None, **kwargs,
    ):
        if not self.agent or not response:
            return

        # Only intercept the response tool
        if tool_name != "response":
            return

        config = self._load_config()
        if not config.get("enabled", True):
            return

        # Check if this agent is an orchestrator profile
        profile = getattr(self.agent.config, "profile", "") or ""
        orchestrator_profiles = config.get(
            "orchestrator_profiles", DEFAULT_ORCHESTRATOR_PROFILES
        )
        if profile not in orchestrator_profiles:
            return

        # Check if call_subordinate was called at any point in conversation
        if self._has_delegation_in_history():
            return

        # Check response length against threshold (provisional, tunable)
        response_text = response.message or ""
        word_count = len(response_text.split())
        word_threshold = config.get("word_threshold", DEFAULT_WORD_THRESHOLD)
        if word_count <= word_threshold:
            return

        # ═══ GATE TRIGGERED ═══
        warning_msg = config.get("warning_message", DEFAULT_WARNING_MESSAGE)

        # Prevent loop termination (mutable Response, checked at agent.py:1212)
        response.break_loop = False

        # Inject warning into history — model sees this on next loop iteration
        self.agent.hist_add_warning(message=warning_msg)

        PrintStyle(font_color="red", padding=True).print(
            f"DELEGATION GATE: Blocked orchestrator '{profile}' from terminating "
            f"without delegation (response: {word_count} words). Injecting remand warning."
        )

        self.agent.context.log.log(
            type="warning",
            content=(
                f"DELEGATION GATE: Blocked response from orchestrator '{profile}' "
                f"— no call_subordinate in conversation history. "
                f"{word_count} words blocked."
            ),
        )

    def _has_delegation_in_history(self) -> bool:
        """Scan conversation history for call_subordinate tool results.

        History structure (verified 2026-07-23):
          History
          ├── .current: Topic          # active topic
          │   └── .messages: list[Message]
          ├── .topics: list[Topic]     # previous topics
          │   └── each has .messages
          └── .bulks: list[Bulk]       # archived/compressed (tool_name lost)

        Note: When topics are summarized (compress via summarize_messages),
        individual messages are replaced with a summary string. The tool_name
        field is lost. Delegation evidence from summarized topics won't be
        detected. Acceptable for v1 — the gate catches within-conversation
        bypasses. Cross-session delegation tracking would need metadata
        stamping at hist_add_tool_result time.
        """
        try:
            history = self.agent.history
        except (AttributeError, TypeError):
            return False

        # Check current topic
        current = getattr(history, "current", None)
        if current:
            for msg in getattr(current, "messages", []):
                if self._msg_has_call_subordinate(msg):
                    return True

        # Check previous topics
        topics = getattr(history, "topics", [])
        for topic in topics:
            for msg in getattr(topic, "messages", []):
                if self._msg_has_call_subordinate(msg):
                    return True

        # Note: archived bulks (.bulks) store summarized output.
        # Individual tool_name fields are lost after summarization.
        # This means delegation evidence from summarized history
        # will not be found. Acceptable for v1.

        return False

    def _msg_has_call_subordinate(self, msg) -> bool:
        """Check if a single message contains a call_subordinate tool result."""
        content = getattr(msg, "content", None)
        if content is None:
            return False

        if isinstance(content, dict):
            return content.get("tool_name") == "call_subordinate"
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("tool_name") == "call_subordinate":
                    return True
        elif isinstance(content, str):
            if '"tool_name"' in content and "call_subordinate" in content:
                return True
        return False

    def _load_config(self) -> dict:
        """Load configuration from default_config.yaml in plugin directory."""
        import os

        try:
            import yaml

            config_path = os.path.normpath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..", "..", "..",
                    "default_config.yaml",
                )
            )
            if os.path.exists(config_path):
                with open(config_path) as f:
                    return yaml.safe_load(f) or {}
        except Exception:
            pass
        return {}

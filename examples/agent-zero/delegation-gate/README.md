# Delegation Gate — wOS Directive D1 Enforcement (Agent Zero)

**Reference implementation of wOS Directive D1 (Delegation is the default) at enforcement level.**

Part of [wOS v0.2](../../SPECIFICATION.md) — the open behavioral design standard for AI agents.

## What It Does

Prevents orchestrator-class agents from terminating their response loop with a deliverable unless they have delegated via `call_subordinate` at some point in the conversation. Enforces the wOS principle "orchestrators plan, delegate, and review — they do not execute" at the code level, not just in prompts.

## Why It Exists

Prompt-only delegation directives ("MUST NOT do the work yourself") fail in production. Orchestrator agents read the rules, understand them, and skip them when it's faster to do the work inline. Evidence from three independent multi-agent projects (2026-07-23): agents articulated the correct delegation workflow when questioned, then chose to bypass it for task efficiency. Code-level enforcement closes the gap between knowing the rule and following it.

## How It Works

1. **Hook:** Intercepts the `response` tool at Agent Zero's `tool_execute_after` extension point — after `tool.execute()` but before the `break_loop` check that terminates the agent loop.

2. **Checks (binary gate, no text classification):**
   - Is the agent's profile in the `orchestrator_profiles` config list?
   - Has `call_subordinate` appeared in the conversation's tool history?
   - Is the response longer than the configurable word threshold (default: 150 words)?

3. **Enforcement:** If all three conditions hold (orchestrator + no delegation + long response), the extension:
   - Sets `response.break_loop = False` (the `Response` object is a mutable dataclass passed by reference — the loop-termination check at `agent.py` reads the mutated value)
   - Injects a `hist_add_warning()` into the conversation history with a delegation directive
   - The agent loop continues; the model sees the warning on its next prompt rebuild and must delegate before it can deliver

4. **Proven pattern:** Uses the same `response.break_loop = False` interception that Agent Zero's Telegram integration plugin uses for intermediate message delivery.

## Installation

Copy the `delegation-gate/` directory into your Agent Zero instance at:

```
/a0/usr/plugins/_delegation_gate/
```

Plugins are enabled by default. Configure orchestrator profiles and word threshold in `default_config.yaml`. Restart the container to load.

## Configuration

See `default_config.yaml`:

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `true` | Enable/disable the gate |
| `orchestrator_profiles` | `["wgnr-ai", "project_account_manager", "wgnr_project_dev", "cct-pm"]` | Agent profiles subject to the gate. Add your orchestrator profiles here. |
| `word_threshold` | `150` | Responses under this word count are allowed without delegation (acknowledgments, routing, status). Tune based on false positive rate. |
| `warning_message` | (see file) | The remand message injected into history when the gate fires |

## Limitations (v1)

- **Response-time only.** The gate intercepts the `response` tool, not other tools (`text_editor`, `code_execution_tool`). An orchestrator can still do work inline via tools and deliver a short summary that passes the word threshold. Mitigate with prompt-level anti-patterns and DOX rules. A tool-time gate is a future enhancement.
- **Word-threshold heuristic.** Compact deliverables under the threshold pass; legitimate long-form orchestrator communication may be blocked. Tunable via config; monitor and adjust.
- **History scope.** Delegation evidence from summarized/compressed conversation topics is lost (individual `tool_name` fields are replaced by summaries). The gate catches within-conversation bypasses, not cross-session ones.

## Conformance Declaration

```
wOS conformance: Level 2 (Extended) + Directive D1 enforcement
Enforcement: Delegation gate (tool_execute_after hook)
Platform: Agent Zero v2.5+ (verified on v2.6)
```

## Testing

The gate was verified with 10 scenarios covering: orchestrator bypass blocked, short-response exemption, subordinate exemption, delegation-then-synthesis pass, non-response tool pass, threshold boundary (150/151 words), and empty-topics edge case. All passed.

## License

Apache-2.0 (same as wOS).

# Delegation Gate Plugin

## What It Does

The Delegation Gate prevents orchestrator-class agents from terminating the response loop without proof of delegation. When an orchestrator agent attempts to deliver a final response (via the `response` tool) without having called `call_subordinate` at any point in the conversation, the gate:

1. **Blocks loop termination** — sets `response.break_loop = False`, preventing the agent loop from ending.
2. **Injects a warning** — adds a `hist_add_warning()` message directing the agent to delegate.
3. **Gives the model another iteration** — the agent loop continues, and the model sees the warning on its next prompt rebuild, forcing it to delegate before delivering its response.

This implements **Directive D1** (Delegation is the default) from the wOS specification at **Level 3 (Strict)** conformance.

## Installation

1. Copy the `delegation-gate-plugin/` directory into your Agent Zero plugins directory (typically `usr/plugins/`).
2. Rename the directory to `_delegation_gate/` (the underscore prefix is Agent Zero convention for plugins that should load first).
3. Ensure the plugin is enabled in your framework settings. Agent Zero auto-discovers plugins with a valid `plugin.yaml`.

## Configuration

Edit `default_config.yaml` to customize behavior:

```yaml
enabled: true

# Add YOUR orchestrator agent profile names here
orchestrator_profiles:
  - orchestrator
  - main-agent
  - project-manager

word_threshold: 150

warning_message: "DELEGATION GATE: You are an orchestrator. You must delegate this work via call_subordinate before responding. Route to the appropriate specialist."
```

**Critical:** You MUST add your actual orchestrator agent profile names to the `orchestrator_profiles` list. The defaults (`orchestrator`, `main-agent`, `project-manager`) are examples — replace them with the profile names used in your deployment.

## How It Works

The gate uses the `tool_execute_after` extension hook, which fires after a tool's `execute()` method runs but before the agent loop checks `break_loop` to decide whether to terminate.

### Hook flow:

1. The agent loop calls `tool.execute()` for the `response` tool.
2. After `execute()` returns, the framework fires `tool_execute_after` extensions in alphabetical order by filename.
3. The delegation gate's `execute()` method receives the `Response` object (mutable, passed by reference).
4. If all three gate conditions are met (orchestrator profile + no `call_subordinate` in history + response exceeds word threshold), it sets `response.break_loop = False`.
5. The agent loop sees `break_loop = False` and continues, giving the model another iteration.
6. The injected warning message tells the model to delegate before responding.

## Proven Precedent

The Telegram integration plugin (`_telegram_integration`) uses this exact pattern for a different purpose — intercepting the response tool via `tool_execute_after` and setting `response.break_loop = False` to prevent loop termination for intermediate message delivery. The delegation gate applies the same mechanism for behavioral enforcement.

## Known Limitations (v1)

- **Response-time only:** The gate intercepts the `response` tool, not other tools (`text_editor`, `code_execution`). An orchestrator can still do work inline via tools and deliver a short summary that passes the word threshold. A tool-time gate is a future enhancement.
- **Word threshold heuristic:** The 150-word threshold is configurable and provisional. False negatives are possible for compact deliverables under the threshold. False positives are possible for legitimate long-form orchestrator communication. Tunable via `default_config.yaml`.
- **History scan scope:** Delegation evidence from summarized/compressed conversation topics is lost (individual `tool_name` fields are replaced with summary strings). The gate catches within-conversation bypasses, not cross-session ones.

## Conformance Declaration

```
Directive D1: Level 3 (Strict)
Enforcement: Delegation gate plugin (tool_execute_after hook)
Platform: Agent Zero v2.5+
Verified: 2026-07-24 (10/10 test scenarios passed)
Limitations: Response-time only, word-threshold heuristic, within-conversation scope
```

---

*wOS Delegation Gate — Human + AI, by design. Apache-2.0 licensed.*

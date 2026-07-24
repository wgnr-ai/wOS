# Delegation Doctrine

Part of [wOS v0.2](../SPECIFICATION.md) — the open behavioral design standard for AI agents.

See [SPECIFICATION.md §3.5](../SPECIFICATION.md#35-delegation) for the full delegation domain specification.

## Directives

| Directive | Title | Summary |
|---|---|---|
| D1 | Delegation is the default | Orchestrators plan, delegate, and review — they do not execute |
| D2 | Model routing by cognitive load | Expensive models decide; cheap models execute |
| D3 | No rank exempts from verification | Verification is universal; rank is organizational, not epistemic |

## Enforcement (v0.2)

Directive D1 is the first wOS directive with a published code-level enforcement implementation. See [SPECIFICATION.md §5 — Code-level enforcement implementations](../SPECIFICATION.md#code-level-enforcement-implementations) for the requirements and the principle/enforcement split.

**Why D1 was first:** Production evidence (2026-07-23) showed prompt-only delegation directives being bypassed consistently across three independent multi-agent projects. Orchestrator agents articulated the correct delegation workflow when questioned, then chose to skip it for task efficiency. Prompt-level "MUST NOT" language could not override the model's optimization for completion speed. Code-level enforcement closed the gap between knowing the rule and following it.

### Reference implementation

**Agent Zero — Delegation gate:** [examples/agent-zero/delegation-gate/](../examples/agent-zero/delegation-gate/)

The delegation gate blocks orchestrator-class agents from terminating their response loop with a deliverable unless they have delegated via `call_subordinate` in the conversation. It hooks the `tool_execute_after` extension point, checks three conditions (orchestrator profile, delegation history, response length), and sets `response.break_loop = False` to force another loop iteration when the orchestrator tries to deliver without delegating.

### Implementing your own D1 enforcement

To implement Directive D1 enforcement on a platform other than Agent Zero:

1. Identify the mechanism by which your orchestrator delivers final responses (a "response tool," a loop-break condition, a message-send primitive)
2. Identify the mechanism by which subordinates are invoked (a delegation tool, a dispatch primitive, a task queue)
3. Build a gate that intercepts the response mechanism and verifies a delegation mechanism was used in the conversation
4. On violation: prevent the response from being delivered and signal the orchestrator to delegate (remand, warning injection, retry)
5. Ensure the gate is configurable (which agent profiles are orchestrators, thresholds for what counts as a "deliverable") and auditable (log every trigger)

The mechanism must meet the [enforcement requirements](../SPECIFICATION.md#code-level-enforcement-implementations) in the spec: prevent violation (not just detect), be code-level (not prompt), preserve agent autonomy, be auditable, and be configurable.

*Expanded implementation guidance for Directives D2 and D3 will be added in a future release.*

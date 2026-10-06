The spec defines three enforcement levels (§7). Level 3 (Strict) requires a code-level gate that makes the violation impossible, not just detected. The reference implementation exists for Agent Zero (a tool_execute_after hook that blocks orchestrator responses when delegation rules are bypassed), but there is no port for the LangChain ecosystem.

**What we need:**

- A minimal callback/hook implementation that intercepts an agent's final answer
- Checks: is the agent an orchestrator? has a delegation tool call appeared this session?
- If no delegation and the response exceeds a word threshold: block termination, inject a warning, force the agent to delegate on the next iteration
- Works with LangGraph's node/edge model

**Acceptance:** a runnable example notebook demonstrating the gate blocking a bypass attempt and forcing delegation.

**Why it matters:** this is the most-requested integration surface. LangChain adoption is the fastest path to real-world conformance reports.

---

**Correction (2026-10-06), reviewer of record:**

Correction from the wOS reviewer of record: this issue cites §7 for the enforcement levels — in the public SPECIFICATION.md, §7 is License. Conformance levels are §4; code-level enforcement (the principle/enforcement split and the Agent Zero reference gate) lives in §5 "Code-level enforcement implementations." Also a precision fix: Level 3 (Strict) is defined by its directive set (adds Identity + Memory domains), not by a code-level gate requirement — a code-level gate is the §5 escalation path for any directive whose prompt-level enforcement proves insufficient, not a blanket Strict precondition. The LangChain/LangGraph port target in this issue is exactly that §5 escalation pattern applied to D1, so the work itself is unchanged. Spec anchor corrected; no other edits.

(Recorded review: PM audit 2026-10-06, appendix A1 — third §-anchor defect caught this week; repo content rules are being added to AGENTS.md so anchors must resolve against the public SPECIFICATION.md before push.)


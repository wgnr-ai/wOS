<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/wos-logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/wos-logo-light.png">
    <img alt="wOS v0.10 — Agent behavior, designed." width="300">
  </picture>
</p>

<h3 align="center">The open behavioral design standard for AI agents.</h3>

<p align="center">
  <a href="SPECIFICATION.md">Read the Spec</a> · <a href="AGENTS.md">Agent Instructions</a> · <a href="templates/">Templates</a> · <a href="docs/bound-vs-unbound-text.md">Design Rationale</a> · <a href="CONTRIBUTING.md">Contribute</a> · <a href="https://wos.wgnr.ai">Website</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-Apache--2.0-blue" alt="License">
  <img src="https://img.shields.io/badge/spec-v0.10-orange" alt="Spec Version">
  <img src="https://img.shields.io/badge/status-Draft-yellow" alt="Status">
</p>

---

## What it is

wOS governs five behavior domains an agent must master to be trustworthy: **communication**, **verification**, **escalation**, **delegation**, and **memory**. The standard is a specification, not a framework. wOS does not replace your agent runtime, your model, or your orchestration layer. It sits on top of them, defining the behavioral contract an agent must satisfy to interoperate safely with humans, peers, and downstream systems. Read the spec, adopt the directives, ship an agent that behaves.

## Why it exists

AI agents are technically capable and behaviorally incoherent. They hedge when they should escalate, ghost-complete tasks they have not started, and invent citations because they cannot tell you what they do not know. These are not edge cases — they are the default state of the field.

Other standards cover adjacent layers: **ACS** specifies what an agent is not allowed to do. **AGENTS.md** specifies what an agent should know. **Agent OS** specifies how an agent should write code. None specify how an agent should behave. wOS fills the gap.

The doctrine is production-tested — it was authored inside [wgnr.ai](https://wgnr.ai), a brand marketing agency accelerated by a proprietary AI methodology, that has run these agents in client work since the launch of GPT-3.5.

## How to adopt it

1. **Pick** your conformance level — Core, Extended, or Strict (see table below)
2. **Direct your agent** using the copy-paste prompt in [AGENTS.md](AGENTS.md) — or install [`templates/wos-enforcement.SKILL.md`](templates/wos-enforcement.SKILL.md) as an auto-loading skill
3. **Validate** against the pre-delivery checks (SPECIFICATION.md §5)
4. **Declare** your conformance level — the agent's declaration is your confirmation it took

The lowest-friction entry point is the **verification domain**: a single directive that forces the agent to surface what it does not know before it claims completion.

### Tell your agent

Paste this to your agent (works with any agent that can read a URL or file):

> Adopt the wOS protocol at **Core** conformance. Load `AGENTS.md` at the root of github.com/wgnr-ai/wOS and apply its directives to your own responses from now on. Declare your conformance level before proceeding.

Use **Extended** for orchestrators and multi-agent systems, **Strict** for long-running agents with persistent state. One word does the work: *"read this"* gets you a summary of wOS; *"adopt this at Core conformance"* gets you conformance.

## What's new in v0.10 (ratified 2026-10-27)

**New directive — V8: Mechanical staging validation.**
An agent that stages a deployable artifact into a runtime must first run that artifact's mechanical validation (compiler, parser, linter, schema validator) against the exact bytes to be staged. Validation failure blocks staging and is reported as data. Unvalidated bytes are never staged, and a failed artifact is never described as staged.

Why: three production incidents in one fleet (2026-09-06, 2026-10-17, 2026-10-27) shared one root cause — an unvalidated edit reached a live runtime. In the third, a single `IndentationError` in a gateway module crash-looped the UI service until an out-of-band restore. V8 closes the gap: validation is a tool-run against the exact staged bytes at the staging boundary; working drafts and validator-less artifact types are out of scope.

Also in v0.10:

- Conformance: V8 carries **Level 1 (Core) minimum** — universal, mechanical, zero-cost. No new pre-delivery check at Level 2; staging-validation claims verify under existing Check C. Mechanical enforcement is runtime implementation (hooks), advisory elsewhere.

Full changelog: [SPECIFICATION.md](SPECIFICATION.md)

## Conformance levels

| Level | Domains | Who should adopt |
|---|---|---|
| **Core** | Communication + Verification + Lifecycle | Any agent that interacts with humans |
| **Extended** | Core + Escalation + Delegation | Multi-agent systems, production orchestrators |
| **Strict** | Extended + Identity + Memory | Long-running agents with persistent state |

One-line directive digests for every level: [AGENTS.md](AGENTS.md).

## Competitive landscape

wOS does not compete with adjacent standards. It occupies the quadrant they leave open.

| Standard | What it governs | Relationship |
|---|---|---|
| [ACS](https://github.com/microsoft/agent-governance-toolkit) (Microsoft) | Security policy | Complementary — security vs. behavior |
| [AGENTS.md](https://agents.md/) (AAIF) | Context and instructions | Complementary — knowledge vs. behavior |
| [Agent OS](https://buildermethods.com/agent-os) (Builder Methods) | Coding standards | Complementary — code quality vs. behavior |
| [OASB-2](https://oasb.ai/oasb-2) / SOUL.md (OpenA2A) | Security behavioral controls | Complementary — security controls vs. operational behavior |
| [Ringer](https://github.com/NateBJones-Projects/ringer) (Nate B. Jones) | Parallel agent orchestration | Complementary — orchestration vs. behavioral doctrine |

## License

Apache-2.0. See [LICENSE](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

*Built by [wgnr.ai](https://wgnr.ai) — wOS v0.10. Agent behavior, designed.*

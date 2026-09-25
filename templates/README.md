# Templates

Ready-made artifacts for adopting wOS without transcribing the spec by hand.

## `wos-enforcement.SKILL.md`

The pre-delivery check protocol (Checks A–P) as an installable skill. Drop it into any agent runtime that supports skills or auto-loaded instruction files; it runs the gating checks before every response.

- **Core conformance** → Checks A, B, C, E, H, I, J, K, L
- **Extended** → Core + D, M, N, O, P
- **Strict** → Extended + F, G

Check P (zero-claims) sits at Extended: it is the structural enforcement of Directive V6, whose conformance note sets an Extended minimum. Install the skill **together with** the [`AGENTS.md`](../AGENTS.md) directive digest (or the spec's §5 system-prompt block) — the checks enforce the directives; they are not a substitute for loading them.

Platform note: the template is runtime-agnostic. Wire Check C (action-claim) and Check O (delegation) artifact verification to your own runtime's tool surfaces — the check semantics are portable, the verification commands are not.

## `wos-conformance.template.json`

The machine-readable conformance manifest from SPECIFICATION.md §5, pre-filled for Core. Copy to `wos-conformance.json` at your project root, set `conformance_level` (1/2/3), align `domains` and `checks_implemented` with the level you claim, and fill per-directive `implementation` modes (`prompt` / `skill` / `config` / `code-gate`).

Honesty rules apply (§5): declared is not enforced; no evidence, no badge; level claims are domain-bounded; manifests remain valid across spec versions but consumers surface the gap. The Core pre-fill intentionally excludes V6/V7 and Check P — both carry Extended-minimum conformance notes in the spec; the template's `_notes` field explains what to add when claiming Extended.

## Adoption paths

| Your runtime | Do this |
|---|---|
| Supports skills / auto-loaded instructions | Install `wos-enforcement.SKILL.md` as an auto-loading skill; point it at the spec for normative text |
| Reads `AGENTS.md` / behavioral config | Root [`AGENTS.md`](../AGENTS.md) already carries the directive digest — adopt it (or add a `## wOS Conformance` section pointing here) |
| System-prompt only | Use the §5 system-prompt block from SPECIFICATION.md |
| Human directing an agent | Use the copy-paste adoption prompt in [`AGENTS.md`](../AGENTS.md) — "adopt," not "read," and name the level |

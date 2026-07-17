# Contributing to wOS

Thank you for your interest in contributing to the open behavioral design standard for AI agents.

## How to contribute

### Reporting issues

Open an issue on the [GitHub repository](https://github.com/wgnr-ai/wOS) with:
- A clear description of the issue or proposal
- The relevant section of the specification
- Any supporting evidence (production incidents, benchmark data, implementation experience)

### Proposing new directives

New directives should be:
1. **Grounded in production experience** — describe a real failure mode that the directive prevents
2. **Framework-agnostic** — expressible in any prompt-based agent system
3. **Testable** — include a compliance check that can verify the directive is being followed
4. **Not covered by existing directives** — check that the failure mode isn't already addressed

Submit a proposal as a GitHub issue with the label `directive-proposal`.

### Submitting reference implementations

We accept reference implementations for any agent framework. Each implementation should:
1. Implement all directives for the claimed conformance level
2. Include a before/after example showing behavioral difference
3. Be self-contained (no dependencies on wgnr.ai infrastructure)

Submit as a pull request to the `examples/` directory.

### Improving the specification

For clarifications, typo fixes, or non-behavioral changes:
1. Fork the repository
2. Create a branch (`fix/your-description`)
3. Submit a pull request with a clear description of the change

For behavioral changes (new directives, modified checks, conformance level changes):
1. Open an issue first with the `directive-proposal` label
2. Discuss with the community
3. Submit a pull request after consensus

## Code of conduct

Be direct. Be evidence-based. Be respectful. wOS is about making agents behave well — the same standard applies to contributors.

## License

All contributions are accepted under the [Apache-2.0 License](LICENSE).

## Documentation standards

### CHANGELOG entries

Every meaningful change gets a CHANGELOG entry. Each entry should include:

- **Added** — new files, features, or capabilities
- **Changed** — modifications to existing behavior or content
- **Supersedes** — what the new version replaces (retain old files for audit trail)

### Out of Scope (per revision)

Every CHANGELOG entry should include an `### Out of Scope` section documenting what was considered but excluded. Format:

```
### Out of Scope (this revision)
- [topic] — [reason excluded] — [what evidence would re-open it]
```

Example:
```
### Out of Scope (this revision)
- Tier-based fallback framework for transient upstream errors — belongs in routing skill, not behavioral doctrine — re-opens if routing skill is deprecated and fallback moves into spec scope
- Print-style voice guide — companion product, not part of behavioral standard — re-opens if voice doctrine is formalized as wOS-adjacent spec
```

This discipline prevents scope creep, documents decision rationale for future contributors, and creates a re-evaluation trigger (when the "evidence" condition is met, revisit the topic).

## Questions

Open an issue with the `question` label, or reach out at [wos@wgnr.ai](mailto:wos@wgnr.ai).

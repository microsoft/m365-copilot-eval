# Eval document examples

This directory is the single source for eval document examples:

- `valid/` contains runnable documents that must pass `schema/v1/eval-document.schema.json`.
- `invalid/` contains negative fixtures that must fail schema validation.

Use `valid/starter.json` for a minimal runnable suite or `valid/comprehensive.json` for a full schema example. Additional runnable scenarios cover Microsoft Graph, multi-turn conversations, ambiguity, grounding, safety, tool failures, partner success, custom evaluators, and mixed evaluation outcomes.

The CLI still accepts legacy array and `prompts`/`expected_responses` inputs for backward compatibility, but new eval suites should use the versioned document format shown here.

## Migrating package-internal example paths

Package versions through 1.16.0 also shipped runnable examples under `src/clients/cli/samples/`. If a script referenced that package-internal directory, replace the prefix with `schema/v1/examples/valid/`; the example filenames are preserved.

Project-owned datasets and the CLI input formats are not affected by this directory change.

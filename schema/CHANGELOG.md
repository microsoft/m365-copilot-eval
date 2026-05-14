# Changelog - M365 Copilot Eval Document Schema

All notable changes to the eval document schema will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0](https://github.com/microsoft/M365-Copilot-Agent-Evals/compare/schema-v1.3.0...schema-v1.4.0) (2026-05-14)


### Features

* unified error reporting in evaluation output ([#288](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/288)) ([a1acfce](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/a1acfce24a558bf855788d552266bc87cecf3251))

## [1.3.0](https://github.com/microsoft/M365-Copilot-Agent-Evals/compare/schema-v1.2.0...schema-v1.3.0) (2026-04-30)


### Features

* Added similarity evaluator for compatibility with MCS Evals. ([#228](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/228)) ([0fe8315](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/0fe8315abc8e0422d1ac9117fe9f29195f29044f))

## [1.2.0](https://github.com/microsoft/M365-Copilot-Agent-Evals/compare/schema-v1.1.0...schema-v1.2.0) (2026-04-22)


### Features

* **schema:** add multi-turn evaluation support (v1.2.0) ([#208](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/208)) ([a5ad22b](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/a5ad22bb4f6ac8ba548dc7f431ace073fa5970ce))

## [1.1.0](https://github.com/microsoft/M365-Copilot-Agent-Evals/compare/schema-v1.0.0...schema-v1.1.0) (2026-03-30)


### Features

* **WI-6855059:** add agentName/cliVersion to schema, fix duplicate prompt loss, include default_evaluators in output ([#181](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/181)) ([9321474](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/93214746144e9d11f507433eff185aefac4a858a))
* **WI-6855059:** implement per-prompt evaluator configuration ([#168](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/168)) ([eface7e](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/eface7e7041b118681cd4c68582fe903640bf6c0))

## [1.0.0] - 2026-02-19

### Added

- Initial schema version for eval document contract
- Root document structure: `schemaVersion` (required), `metadata` (optional), `items` (required)
- `DocumentMetadata` with `name`, `description`, `createdAt`, `createdBy`, `evaluatedAt`, `tags`, `agentId`, and `extensions`
- `EvalItem` with `prompt` (required), `expected_response`, `response`, `context`, `citations`, `scores`, and `extensions`
- `ScoreCollection` with `relevance`, `coherence`, `groundedness`, `toolCallAccuracy`, and `citations` scores
- `EvalScore` standard score structure (1-5 scale) with `score`, `result`, `threshold`, `reason`, `evaluator`
- `CitationScore` for citation-specific evaluation with `count`, `result`, `threshold`, `format`, `citations`
- `Citation` reference object with `index`, `text`, `source`
- Extension points at `metadata.extensions` and `items[].extensions` for forward compatibility
- `additionalProperties: true` on all objects for forward compatibility within major version

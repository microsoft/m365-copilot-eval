# Changelog - M365 Copilot Eval Document Schema

All notable changes to the eval document schema will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 1.5.0 (2026-05-27)


### Features

* **evaluators:** Add retrieval query and retrieval result evaluators

## 1.4.0 (2026-05-14)


### Features

* unified error reporting in evaluation output

## 1.3.0 (2026-04-30)


### Features

* Added similarity evaluator for compatibility with MCS Evals.

## 1.2.0 (2026-04-22)


### Features

* **schema:** add multi-turn evaluation support (v1.2.0)

## 1.1.0 (2026-03-30)


### Features

* **WI-6855059:** add agentName/cliVersion to schema, fix duplicate prompt loss, include default_evaluators in output
* **WI-6855059:** implement per-prompt evaluator configuration

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

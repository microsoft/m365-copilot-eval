# Changelog

## 1.14.0 (2026-07-22)


### Features

* **a2a:** log request-id/conversation-id/timestamp for every A2A response


### Bug Fixes

* **env-loader:** support .env.dev auto-detection and env-file selecti…

## 1.13.0 (2026-07-16)


### Features

* **citations:** detect markdown-link citation format ([N](url#suffix))

## 1.12.0 (2026-07-10)


### Features

* Add --account &lt;account&gt; CLI flag for selecting MSAL account
* Add Copilot SDK as alternative LLM judge backend
* Support gpt-5x judge models via Foundry cloud evaluation
* support non-LLM custom evaluators

## 1.11.0 (2026-06-17)


### Features

* add accept-eula subcommand and EULA enforcement gate
* Add agent selection for WorkIQ
* Add Auth Support for Linux and MacOS
* add JSON Schema validation and auto-upgrade for eval documents (WI-6081652)
* Add Work IQ A2A support and refactor CLI agent clients
* Added similarity evaluator for compatibility with MCS Evals.
* **auth:** add DefaultAzureCredential support for Azure OpenAI
* Auto-append `.declarativeAgent` suffix to short-form agent IDs
* auto-load .env.local.user as user-specific secret override
* automatic token refresh on HTTP 401 for long-running eval sessions
* decompose main.py into focused modules
* Default to WorkIQ A2A endpoint with Graph gateway fallback
* Drop Sydney - Call WorkIQ API Exclusively
* **evaluators:** add retrieval diagnostics to evaluation output
* **evaluators:** Add retrieval query and retrieval result evaluators
* **evaluators:** use LLM entailment judge for retrieval extract assertions
* Implement Parallelization and Optimization
* Implement PYTHON_PATH fallback for Python runtime setup
* **logging:** add unified log-level controls and console diagnostics
* **logging:** Route MSAL/Azure SDK logs through CLI logger
* Reads Tenant ID from TEAMS_APP_TENANT_ID variable in ENV file in ATK …
* **schema:** add multi-turn evaluation support (v1.2.0)
* support custom evaluators
* support multiturn evaluation
* unified error reporting in evaluation output
* **WI-6855059:** add agentName/cliVersion to schema, fix duplicate prompt loss, include default_evaluators in output
* **WI-6855059:** implement per-prompt evaluator configuration


### Bug Fixes

* **#375,#376:** configurable A2A request timeout and socket-timeout retry
* auto-create output directory when writing evaluation results
* bold text in agent response shouldn't cause line break
* **cli:** reduce duplicated progress logging logic
* configure bootstrap-sha in release please
* Handle WorkIQ A2A API response format change and full task state coverage
* include .prompty flow files in published npm package.
* Include timezone in 1P chat payload
* Optimize Python CLI Installation Performance
* point package.json repository and homepage to public npm repo
* prevent flaky progress test from corrupting test runner IPC
* **release:** reset release-please manifest to GA baseline
* resolve custom evaluators, --prompts-file and --output paths relative to cwd (#371, #415)
* resolve debug log redaction false positives on agent IDs and URLs
* use dotenv.parse() in env-loader to handle inline comments in .env files

## 1.10.2-preview.1 (2026-06-16)


### Bug Fixes

* resolve custom evaluators, --prompts-file and --output paths relative to cwd (#371, #415)

## 1.10.1-preview.1 (2026-06-11)


### Bug Fixes

* include .prompty flow files in published npm package.

## 1.10.0-preview.1 (2026-06-10)


### Features

* **auth:** add DefaultAzureCredential support for Azure OpenAI
* **evaluators:** add retrieval diagnostics to evaluation output
* **evaluators:** use LLM entailment judge for retrieval extract assertions
* support custom evaluators


### Bug Fixes

* **#375,#376:** configurable A2A request timeout and socket-timeout retry
* resolve debug log redaction false positives on agent IDs and URLs

## 1.9.0-preview.1 (2026-05-26)


### Features

* **evaluators:** Add retrieval query and retrieval result evaluators

## 1.8.0-preview.1 (2026-05-21)


### Features

* Add Auth Support for Linux and MacOS
* **logging:** Route MSAL/Azure SDK logs through CLI logger

## 1.7.0-preview.1 (2026-05-13)


### Features

* **#236:** unified error reporting in evaluation output
* Reads Tenant ID from TEAMS_APP_TENANT_ID variable in ENV file in ATK …

## 1.6.0-preview.1 (2026-05-07)


### Features

* automatic token refresh on HTTP 401 for long-running eval sessions
* Implement PYTHON_PATH fallback for Python runtime setup


### Bug Fixes

* point package.json repository and homepage to public npm repo

## 1.5.0-preview.1 (2026-04-30)


### Features

* Add agent selection for WorkIQ
* Added similarity evaluator for compatibility with MCS Evals.
* decompose main.py into focused modules
* Drop Sydney - Call WorkIQ API Exclusively


### Bug Fixes

* auto-create output directory when writing evaluation results
* Handle WorkIQ A2A API response format change and full task state coverage

## 1.4.0-preview.1 (2026-04-22)


### Features

* add accept-eula subcommand and EULA enforcement gate
* Add Work IQ A2A support and refactor CLI agent clients
* Auto-append `.declarativeAgent` suffix to short-form agent IDs
* Implement Parallelization and Optimization
* **schema:** add multi-turn evaluation support (v1.2.0)
* support multiturn evaluation


### Bug Fixes

* bold text in agent response shouldn't cause line break
* prevent flaky progress test from corrupting test runner IPC
* use dotenv.parse() in env-loader to handle inline comments in .env files

## 1.3.0-preview.1 (2026-04-01)


### Features

* **logging:** add unified log-level controls and console diagnostics
* **WI-6855059:** add agentName/cliVersion to schema, fix duplicate prompt loss, include default_evaluators in output
* **WI-6855059:** implement per-prompt evaluator configuration

## 1.2.1-preview.1 (2026-03-23)


### Bug Fixes

* configure bootstrap-sha in release please
* Include timezone in 1P chat payload

## 1.2.0-preview.1 (2026-03-11)


### Features

* Add AUTO mode to CitationsEvaluator
* add eval document schema v1 contract (WI-6081652)
* add JSON Schema validation and auto-upgrade for eval documents (WI-6081652)
* auto-load .env.local.user as user-specific secret override
* **schema:** add eval document schema v1 contract with CI validation (WI-6081652)
* unify M365_TITLE_ID and M365_AGENT_ID configuration
* unify M365_TITLE_ID and M365_AGENT_ID configuration


### Bug Fixes

* **cli:** reduce duplicated progress logging logic
* fix release please path config
* fix release please path config
* Optimize Python CLI Installation Performance

## 1.1.1-preview.1 (2026-02-04)


### Bug Fixes

* Windows pip self-upgrade during runevals --init-only by using python -m pip

## 1.1.0-preview.1 (2026-02-03)


### Features

* add 60-day package expiry mechanism with automated publish date
* add init progress tracking for evaluation runs


### Bug Fixes

* display usage terms at runtime, resolve license file conflicts, on errors direct to npm readme.

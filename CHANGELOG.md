# Changelog

## [1.6.0-preview.1](https://github.com/microsoft/M365-Copilot-Agent-Evals/compare/v1.5.0-preview.1...v1.6.0-preview.1) (2026-05-07)


### Features

* automatic token refresh on HTTP 401 for long-running eval sessions ([#283](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/283)) ([0fa6d2e](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/0fa6d2edca5a8cc52b399d505c3084e20e8ab79b))
* Implement PYTHON_PATH fallback for Python runtime setup ([#239](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/239)) ([bb14ab4](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/bb14ab4ea35ad5a8f6bfaa181d599a615fec199b))


### Bug Fixes

* point package.json repository and homepage to public npm repo ([#290](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/290)) ([ea1dbdb](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/ea1dbdbb770a0aa636d36d31578d4cc32ded47c4))

## [1.5.0-preview.1](https://github.com/microsoft/M365-Copilot-Agent-Evals/compare/v1.4.0-preview.1...v1.5.0-preview.1) (2026-04-30)


### Features

* Add agent selection for WorkIQ ([#263](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/263)) ([8f0bf02](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/8f0bf02cfbc7907c14fdeb9882ccd8154807d7bb))
* Added similarity evaluator for compatibility with MCS Evals. ([#228](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/228)) ([0fe8315](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/0fe8315abc8e0422d1ac9117fe9f29195f29044f))
* decompose main.py into focused modules ([#245](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/245)) ([c2bd97d](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/c2bd97d3a4c2a617bbcf238a7ddb500e8e5f853e))
* Drop Sydney - Call WorkIQ API Exclusively ([#272](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/272)) ([230ebd9](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/230ebd9e1759680346f7b320ccb3f842533c55d5))


### Bug Fixes

* auto-create output directory when writing evaluation results ([#267](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/267)) ([db09583](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/db0958388929f4768cd9591de5ef548a1518f3a8))
* Handle WorkIQ A2A API response format change and full task state coverage ([#276](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/276)) ([6645799](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/664579979304d4105c41a2c7ffab9965ed237a0e))

## [1.4.0-preview.1](https://github.com/microsoft/M365-Copilot-Agent-Evals/compare/v1.3.0-preview.1...v1.4.0-preview.1) (2026-04-22)


### Features

* add accept-eula subcommand and EULA enforcement gate ([#247](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/247)) ([3a1c0fa](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/3a1c0fac7c1dcca8fed03b76d1732eb6fc5266df))
* Add Work IQ A2A support and refactor CLI agent clients ([#203](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/203)) ([ac0d7d5](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/ac0d7d50347bdaf656a1dd5c35ebcbdd504d4137))
* Auto-append `.declarativeAgent` suffix to short-form agent IDs ([#254](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/254)) ([e27d33e](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/e27d33ef105eabf3a485d589011adc19eb566d47))
* Implement Parallelization and Optimization ([#182](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/182)) ([4b9c7d8](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/4b9c7d893f496c754e99ef218a7b4aa44faf9ec6))
* **schema:** add multi-turn evaluation support (v1.2.0) ([#208](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/208)) ([a5ad22b](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/a5ad22bb4f6ac8ba548dc7f431ace073fa5970ce))
* support multiturn evaluation ([#229](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/229)) ([95cfb88](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/95cfb8882b949dfe25b90c2a73d61035fe7ac343))


### Bug Fixes

* bold text in agent response shouldn't cause line break ([#246](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/246)) ([dc417aa](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/dc417aa0a69db60bb3189823c0aed770928ae545))
* prevent flaky progress test from corrupting test runner IPC ([#249](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/249)) ([988cdf7](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/988cdf7f8522f09455afa69d21d80d3d9c45a6fe))
* use dotenv.parse() in env-loader to handle inline comments in .env files ([#241](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/241)) ([ee2813c](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/ee2813c60e6ae0efc14076f20bb44f7312e6d820))

## [1.3.0-preview.1](https://github.com/microsoft/M365-Copilot-Agent-Evals/compare/v1.2.1-preview.1...v1.3.0-preview.1) (2026-04-01)


### Features

* **logging:** add unified log-level controls and console diagnostics ([#163](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/163)) ([dd3023e](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/dd3023e3ff47efc5cb13b8d40f0d0a90518acc2b))
* **WI-6855059:** add agentName/cliVersion to schema, fix duplicate prompt loss, include default_evaluators in output ([#181](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/181)) ([9321474](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/93214746144e9d11f507433eff185aefac4a858a))
* **WI-6855059:** implement per-prompt evaluator configuration ([#168](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/168)) ([eface7e](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/eface7e7041b118681cd4c68582fe903640bf6c0))

## [1.2.1-preview.1](https://github.com/microsoft/M365-Copilot-Agent-Evals/compare/v1.2.0-preview.1...v1.2.1-preview.1) (2026-03-23)


### Bug Fixes

* configure bootstrap-sha in release please ([#137](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/137)) ([d7b09e6](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/d7b09e66930c5fc0fb6ffaf6eaa8b3495026955a))
* Include timezone in 1P chat payload ([#172](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/172)) ([6601552](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/6601552d3b089949b71a87842910140bd290b54f))

## [1.2.0-preview.1](https://github.com/microsoft/M365-Copilot-Agent-Evals/compare/v1.1.1-preview.1...v1.2.0-preview.1) (2026-03-11)


### Features

* Add AUTO mode to CitationsEvaluator ([#115](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/115)) ([66df378](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/66df378b3edb5ec7028b70fa45804a11cbd0e481))
* add eval document schema v1 contract (WI-6081652) ([f08a5e6](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/f08a5e6d95504beada436a92052ff147c7222f74))
* add JSON Schema validation and auto-upgrade for eval documents (WI-6081652) ([#131](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/131)) ([0ea89c8](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/0ea89c80b7fab5cff91906c5b1ee96735c6a8821))
* auto-load .env.local.user as user-specific secret override ([#144](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/144)) ([b734f15](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/b734f15bdd4fa423220e29d832f4f8c0a09c9760))
* **schema:** add eval document schema v1 contract with CI validation (WI-6081652) ([a4159d2](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/a4159d2fde3f4f2e8034e30497784b46e23f4fc6))
* unify M365_TITLE_ID and M365_AGENT_ID configuration ([#58](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/58)) ([95c3094](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/95c30941ef68ec436ebefb33c7f2be1a4e3476fc))
* unify M365_TITLE_ID and M365_AGENT_ID configuration ([#58](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/58)) ([116ce82](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/116ce8229feaaed57b0548bb51a7a07c9ac93f61))


### Bug Fixes

* **cli:** reduce duplicated progress logging logic ([#151](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/151)) ([4381f34](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/4381f34d19ac8a75fce05fd22a46e6c1cd70d91a))
* fix release please path config ([b1df9f6](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/b1df9f68eb0bb5926bf405f5a0ebe07e5a42b3fd))
* fix release please path config ([747d96d](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/747d96d26d6c1f8adb0ae915406102ac27ebec8e))
* Optimize Python CLI Installation Performance ([#133](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/133)) ([39bd427](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/39bd4273eabf16020aa49fefacdabb49944635d6))

## [1.1.1-preview.1](https://github.com/microsoft/M365-Copilot-Agent-Evals/compare/v1.1.0-preview.1...v1.1.1-preview.1) (2026-02-04)


### Bug Fixes

* Windows pip self-upgrade during runevals --init-only by using python -m pip ([#109](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/109)) ([71e4f92](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/71e4f92a9d6939f6271cd4c590af6b3f47c950a2))

## [1.1.0-preview.1](https://github.com/microsoft/M365-Copilot-Agent-Evals/compare/v1.0.1-preview.1...v1.1.0-preview.1) (2026-02-03)


### Features

* add 60-day package expiry mechanism with automated publish date ([#74](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/74)) ([783a4ee](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/783a4ee99de21ffbe767185fb2e3dc875aa8eecb))
* add init progress tracking for evaluation runs ([#75](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/75)) ([#84](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/84)) ([63bfd27](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/63bfd2773f5e279fea3d02acd50ed109d2a6299a))


### Bug Fixes

* display usage terms at runtime, resolve license file conflicts, on errors direct to npm readme. ([#87](https://github.com/microsoft/M365-Copilot-Agent-Evals/issues/87)) ([a8dd51e](https://github.com/microsoft/M365-Copilot-Agent-Evals/commit/a8dd51e21b2f0b0c0de1c01dd85855d750ab2a8b))

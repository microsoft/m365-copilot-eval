# M365 Copilot Evaluations CLI v2 upgrade guide

This guide covers v2 breaking changes, starting with `2.0.0-preview1`.
The schema v2 migration below applies only to releases that activate schema v2,
not automatically to the first CLI v2 preview.

- **No agent ID now means Microsoft 365 Copilot**, not an agent picker.
- **Title-only Agents Toolkit projects must add `--component agent`** to keep
  evaluating their agent.
- Existing explicit or configured agent IDs continue to select an agent.
- Audit CI commands and environment files before installing the preview.

## Breaking changes

| v1 usage | v2 behavior | Migration |
|---|---|---|
| Run without an agent ID and select an agent interactively | Runs the default Copilot experience without opening a picker | Add `--component agent` to opt into discovery |
| Run in an Agents Toolkit project with only `M365_TITLE_ID` | Runs Copilot and emits a title-only warning | Add `--component agent` to use the title-derived agent alias |
| Agent selection in an unattended session without a resolved ID | Explicit agent mode exits with code 2 before authentication | Supply an explicit/configured ID or a title with `--component agent` |
| Consume agent-centric console/report headers | Reports expose Target and optional Component; Copilot runs do not expose an Agent ID | Make Agent ID optional in report consumers |

The package and command names are unchanged: install
`@microsoft/m365-copilot-eval` and run `runevals`.

## Install the preview

After publication, install the exact first preview:

```powershell
npm install -g @microsoft/m365-copilot-eval@2.0.0-preview1
runevals --version
```

The `preview` npm channel tracks v2:

```powershell
npm install -g @microsoft/m365-copilot-eval@preview
```

Pin an exact version in CI for reproducible runs. The `latest` channel stays on
stable v1, maintained from `support/v1`. An unversioned
`npm install -g @microsoft/m365-copilot-eval`, `@latest`, or `@1` installs v1.
Publishing a v2 preview must not change `latest`.

The npm wrapper continues to manage Python automatically. This change does not
replace existing tenant, license, WorkIQ consent, EULA, or judge prerequisites.

## Upgrade agent-evaluation commands

### Agents Toolkit projects using a title ID

Previously, `M365_TITLE_ID` could select the deployed agent implicitly.

**Before (v1):**

```powershell
# M365_TITLE_ID is supplied by the project's environment file.
runevals --prompts-file .\evals.json
```

**After (v2, preserve agent execution):**

```powershell
runevals --component agent --prompts-file .\evals.json
```

`M365_TITLE_ID` identifies a package. Only explicit agent mode converts it to the
`<title-id>.declarativeAgent` alias. A configured agent ID takes precedence over
the title; the title does not override an ID from another environment-file layer.

### Projects that previously opened the agent picker

**Before (v1, no configured agent ID):**

```powershell
runevals --prompts-file .\evals.json
```

**After (v2, opt into the picker):**

```powershell
runevals --component agent --prompts-file .\evals.json
```

The picker requires terminal stdin and stdout and is disabled in CI.
Redirecting stdout makes the session ineligible for picking; redirecting only
stderr does not. `--interactive` still means entering prompts, not selecting an
agent.

### Existing explicit or configured agent IDs

These invocations keep their existing meaning:

```powershell
runevals --m365-agent-id my-agent --prompts-file .\evals.json
runevals --agent-id my-agent --prompts-file .\evals.json
```

Resolution order is the explicit flag, `M365_AGENT_ID`, then legacy `AGENT_ID`.
Short IDs still receive the `.declarativeAgent` suffix. A resolved agent ID
implicitly selects component `agent`; `--component agent` is optional in that case.

## Update CI and automation

Pin the agent explicitly rather than relying on discovery:

```powershell
runevals --component agent --m365-agent-id my-agent --prompts-file .\evals.json --output .\results.json
```

Alternatively, supply `M365_AGENT_ID`, or use `M365_TITLE_ID` together with
`--component agent`. Explicit agent mode without any resolvable ID fails before
authentication in CI or when terminal input/output is unavailable.

**Audit no-ID jobs carefully:** without `--component agent`, v2 runs Copilot.
It does not fail merely because the previous agent selection is absent.

## Evaluate Microsoft 365 Copilot

With no agent ID configured:

```powershell
runevals --target m365-copilot --prompts-file .\evals.json
```

The target flag is optional. `--target copilot` is a compatibility alias.
**The target flag does not override an agent ID.** To evaluate Copilot rather
than an agent, remove `M365_AGENT_ID` and `AGENT_ID` from both the process
environment and every loaded environment file, and omit agent-ID/component flags.

Target and component are independent: this remains a valid agent invocation:

```powershell
runevals --target m365-copilot --component agent --m365-agent-id my-agent --prompts-file .\evals.json
```

Explicit plugin and CoWork execution modes are not supported. With schema v2,
tool calls from standalone plugins can be evaluated through mainline Copilot;
this does not introduce a separate plugin execution target.

## Re-evaluate saved responses

Use the saved document without live-execution selectors:

```powershell
runevals --evaluate-only .\captured-evals.json --output .\rescored.json
```

Do not combine `--evaluate-only` with explicit `--target`, `--component`,
`--m365-agent-id`, or `--agent-id`. Ambient agent IDs do not change the recorded
execution identity, and replay does not execute new live prompts. Judge
configuration is still required.

## Update report consumers and check schema compatibility

New live runs record target `m365-copilot`; agent runs additionally record
component `agent`. Reports can omit Agent ID for Copilot runs. Update scripts
that assume every report contains an agent ID or depend on old console headings.

The initial CLI v2 execution changes alone do not require a dataset-schema
upgrade. Optional execution metadata does not change evaluator score/status
semantics. Saved documents using target `copilot` retain that recorded value
during replay.

**CLI v2 does not mean eval-document schema v2.** Do not change `schemaVersion`
to `2.0.0` or replace existing v1 schema references solely because the CLI changed.
The schema has its own release/versioning lifecycle.

### When schema v2 is activated

- **Migrate all input and replay documents** to an object with `schemaVersion`
  and `items`, using schema `2.0.0` and the
  [v2 schema](../schema/v2/eval-document.schema.json). Update `$schema` if present.
  V1 and unversioned documents are rejected unchanged, without an automatic
  cross-major upgrade or backup. This applies even without tool evaluators.
- **Replace `plugin_name` in each `calls[].tool`** for `ToolCallSelection` and
  `ToolCallExecution` with the exact identity below:

  ```json
  {
    "plugin_id": "T_package-id",
    "toolset_id": "action-or-connector-id",
    "function_name": "get_forecast"
  }
  ```

- **Use returned IDs.** `plugin_id` is Developer Info `plugin.titleId`;
  `toolset_id` is the DA's `plugin.actionId` or the standalone plugin's
  `plugin.agentConnectorId`; `function_name` is `functionDisplayName`.
  Matching is case-sensitive; do not infer IDs from names or raw `plugin.id`.
- **Discovery remains DA-only.** `runevals --list-tools <agent-id>` prints
  copy-ready identities without the invocation-only `.declarativeAgent` suffix.
  For standalone plugins, use returned Developer Info. `allowed_tools` strings
  are unchanged and are not evaluator identities.
- **Saved tool diagnostics use the same three identity fields.** Update consumers
  and recapture old telemetry if its IDs are unavailable. Changing `schemaVersion`
  alone cannot migrate name-based identities.

## GitHub Copilot judge authentication

M365 authentication and GitHub judge authentication remain separate.
When using `--judge-backend github-copilot`, Python now verifies SDK
authentication before evaluations start, including when the judge model is
`auto`. Missing authentication or a failed check exits with code 1 rather than
running live prompts and reporting success without scores.

Sign in with `gh auth login`, or configure one of the SDK-supported token
variables: `COPILOT_GITHUB_TOKEN`, `GH_TOKEN`, or `GITHUB_TOKEN`. Do not commit
tokens to environment files. The wrapper no longer launches GitHub login
automatically.

## Direct Python users

Apply the same command changes to `python main.py`. For example, from
`src\clients\cli`, preserve title-based agent evaluation with:

```powershell
python main.py --component agent --prompts-file .\evals.json
```

The Node wrapper owns environment-file selection (`--env`) and Python setup;
those wrapper-only options are not added to the Python parser.

## Roll back to v1

```powershell
npm install -g @microsoft/m365-copilot-eval@1
runevals --version
```

Restore your v1 commands too: v1 does not accept the new `--target` and
`--component` options. Keep a copy of the previous CI command and environment
configuration before switching to the preview.

## Upgrade checklist

- Identify commands relying on title fallback or implicit agent discovery.
- Add `--component agent`, or pin an explicit agent ID.
- For Copilot runs, remove configured agent IDs from all environment sources.
- Remove live-execution selectors from saved-response replay commands.
- Allow optional agent identity and the new target/component metadata in reports.
- Verify GitHub authentication before choosing the Copilot judge backend.
- Run a small representative dataset and confirm the reported target/component
  before running a full evaluation.

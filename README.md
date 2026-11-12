# Microsoft 365 Copilot Evaluations

**Test your Copilot extensions. Measure quality. Improve with confidence.**

Evaluate Microsoft 365 Copilot agents and plugins (in V2 Preview). Run repeatable tests and review results in HTML, JSON, or CSV.

> **V2 preview.** The default execution behavior changes from agent selection to Microsoft 365 Copilot. 
> Read the [v2 upgrade guide](./docs/upgrade-to-v2.md) before upgrading.
> Preview changes are marked with Preview tag at the beginning of the section.

[Quick Start](#quick-start) | [Preview: Plugin Evaluations](#preview) | [Agent Evaluations](#agent-evaluations) | [Evaluators](#evaluators) | [Judges](#judges) | [Troubleshooting](#troubleshooting)

**Choose a version:** V1 uses the npm `latest` tag and includes agent evaluations, GitHub Copilot and Azure judges, and the evaluators below. V2 uses the `preview` tag for plugin evaluations. The main sections cover V1; V2-specific instructions are in [Preview](#preview).

## Quick Start

You need the following pre-requisites -
1. **[Node.js 24.12.0+](https://nodejs.org/en/download)**, 
2. a **Microsoft 365 Copilot license**, your **tenant ID**, and 
3. [tenant admin approval for the WorkIQ Client App](https://github.com/microsoft/work-iq/blob/main/ADMIN-INSTRUCTIONS.md). 
4. Python 3.13 is downloaded and cached automatically. You do not need to clone this repository.

The below example evaluates a deployed agent using the **GitHub Copilot judge**, which requires [GitHub CLI](https://cli.github.com/) and GitHub Copilot access. Azure is also supported; see [Judges](#judges).

Install **V1 (`latest`)** and accept the license terms:

```powershell
npm install -g @microsoft/m365-copilot-eval@latest
runevals accept-eula
```

sign in to GitHub:
```powershell
gh auth login
```

In your evaluation folder, set your [tenant ID](https://learn.microsoft.com/en-us/sharepoint/find-your-office-365-tenant-id) and run a quick check:

```powershell
$env:TENANT_ID = "<your-tenant-id>"
runevals --m365-agent-id "<your-agent-id>" --judge-backend github-copilot --prompts "What can you help me with?" --output results.html
```

Sign in to Microsoft 365 when prompted. Open `results.html` to review the default **Relevance** and **Coherence** scores.

Ready to try some complex datasets? Checkout our sample datasets [here](https://github.com/microsoft/m365-copilot-eval/tree/main/schema/v1/examples/valid) and [here](https://github.com/microsoft/m365-copilot-eval/tree/main/samples).

## Preview

### Plugin Evaluations

Plugin evaluations require **V2 Preview (`preview`)**, not V1 (`latest`). Once a V2 Preview package is published, install it with:

```powershell
npm install -g @microsoft/m365-copilot-eval@preview
runevals accept-eula
```

Evaluate the quality of **Copilot responses that use an available plugin**. Provision and enable the plugin in Microsoft 365 Copilot first.

With no configured agent ID, V2 evaluates Microsoft 365 Copilot chat. Keep `M365_AGENT_ID` and legacy `AGENT_ID` out of your shell and loaded environment files for plugin runs. This evaluates the Copilot experience, not a plugin endpoint in isolation.

For example, save this as `evals\plugins.json`. Replace the prompt and consent name with values for your plugin:

```json
{
  "schemaVersion": "1.11.0",
  "default_allowed_tools": ["ContosoCatalog_get_product"],
  "default_evaluators": {
    "Relevance": {},
    "Coherence": {}
  },
  "items": [
    {
      "prompt": "Use the Contoso Catalog plugin to find the price of product SKU-123."
    }
  ]
}
```

Run the plugin scenario through Copilot:

```powershell
runevals --judge-backend github-copilot --prompts-file evals\plugins.json --output plugin-results.html
```

Relevance and Coherence assess response quality; these scores don't prove that a plugin was invoked.

**Safe execution:** Use read-only scenarios first and complete connector sign-in in Copilot. `default_allowed_tools` configures consent at document level; `allowed_tools` can be set per prompt. See the [allowlist example](schema/v1/examples/valid/allowed-tools.json).

Installing either tag replaces the global `runevals` command. To return to V1, reinstall `@microsoft/m365-copilot-eval@latest`.

## Agent Evaluations

V1 (`latest`) evaluates deployed agents. For repeatable or unattended runs, supply an [agent ID](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/evaluations-cli-get-env-values#get-your-agent-id-m365_agent_id):

```powershell
runevals --m365-agent-id "<your-agent-id>" --judge-backend github-copilot --prompts-file evals\evals.json --output agent-results.html
```

`--m365-agent-id` overrides environment IDs. You can also configure `M365_AGENT_ID`. In ATK projects, run from the agent root folder and V1 resolves the agent ID from your project files:

```powershell
runevals --judge-backend github-copilot --prompts "What can you help me with?" --output agent-results.html
```

## Datasets and Results

Keep regression tests in a JSON document. This example includes a single-turn check and a multi-turn conversation; replace the sample policy with your own content:

```json
{
  "schemaVersion": "1.2.0",
  "default_evaluators": {
    "Relevance": { "threshold": 4 },
    "Coherence": { "threshold": 3 }
  },
  "items": [
    {
      "prompt": "What is the dinner allowance?",
      "expected_response": "Dinner is covered up to $75 per person.",
      "evaluators": {
        "Similarity": { "threshold": 4 }
      }
    },
    {
      "name": "Dinner expense follow-up",
      "turns": [
        {
          "prompt": "My dinner cost $95. The allowance is $75. How much is over the limit?",
          "expected_response": "The dinner is $20 over the limit."
        },
        {
          "prompt": "What if dinner cost $70 instead?",
          "expected_response": "It would be $5 below the limit."
        }
      ]
    }
  ]
}
```

Run against your configured agent, or add `--m365-agent-id` from the preceding section:

```powershell
runevals --judge-backend github-copilot --prompts-file evals\evals.json --output results.html
```

Use `.json` for automation or `.csv` for spreadsheets. Conversation turns share context.

## Evaluators

**Relevance** and **Coherence** run by default. Choose checks based on what you need to verify:

| Evaluator | Type | Scale | Default | Description |
|---|---|---|---|---|
| Relevance | LLM-based | 1-5 | Yes | Assesses how well the response addresses the user's query. |
| Coherence | LLM-based | 1-5 | Yes | Measures the logical and orderly presentation of ideas. |
| Groundedness | LLM-based | 1-5 | No | Checks whether the response is supported by the provided grounding context. |
| Similarity | LLM-based | 1-5 | No | Measures semantic similarity to `expected_response`. |
| Citations | Count-based | >= 0 | No | Counts citation references. |
| RetrievalQuery | Non-LLM | pass/fail | No | Checks whether Copilot translated user intent into the expected retrieval queries. |
| RetrievalResult | Non-LLM | pass/fail | No | Checks whether expected resources appear in retrieval results. |
| ExactMatch | String match | boolean | No | Checks whether the response matches `expected_response` exactly. |
| PartialMatch | String match | 0.0-1.0 | No | Measures textual similarity to `expected_response`. |

Per-item or per-turn evaluators extend document defaults. Set `evaluators_mode` to `replace` to run only the specified checks. For example, use this item in a dataset:

```json
{
  "prompt": "What is the dinner allowance? Cite the policy.",
  "context": "The travel policy allows dinner expenses up to $75 per person.",
  "evaluators": {
    "Groundedness": { "threshold": 4 },
    "Citations": { "threshold": 1 }
  },
  "evaluators_mode": "replace"
}
```

Deterministic checks do not need an LLM judge.

[Evaluator reference](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/evaluations-cli-evaluators) | [Custom evaluators](custom-evaluators/README.md)

## Judges

A judge scores LLM-based evaluators; it is separate from the agent being tested.

| Judge | Setup |
|---|---|
| **GitHub Copilot (experimental)** | `--judge-backend github-copilot`; GitHub sign-in and Copilot access. No Azure OpenAI keys required. |
| **Azure (default)** | `--judge-backend azure`; [configure Azure OpenAI or Microsoft Foundry](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/evaluations-cli-get-env-values). |

GitHub Copilot selects a judge model automatically. To pin one your account can access:

```powershell
$env:GITHUB_COPILOT_JUDGE_MODEL = "<model-id>"
runevals --judge-backend github-copilot --prompts-file evals\evals.json --output results.json
```

To use your configured Azure OpenAI judge:

The CLI defaults to an API key (AZURE_AI_API_KEY). For keyless Microsoft Entra ID authentication, use  DefaultAzureCredential .

Option A: API Key (default)

Declare the following variables in an env file.

```dotenv
# .env.local.user (NOT checked in — secrets go here)
AZURE_AI_OPENAI_ENDPOINT="<your-azure-openai-endpoint>"
AZURE_AI_API_KEY="<your-api-key-from-azure-portal>"
AZURE_AI_API_VERSION="2024-12-01-preview"  # default
AZURE_AI_MODEL_NAME="gpt-4o-mini"           # recommended
```

Option B: DefaultAzureCredential (keyless)

1. Sign in:  `az login --tenant <your-tenant-id>` 
2. Assign **Cognitive Services OpenAI User** to your identity on the Azure OpenAI resource.
3. Set `AZURE_AI_OPENAI_ENDPOINT`, `AZURE_AI_API_VERSION`, and `AZURE_AI_MODEL_NAME` as shown in Option A. Omit `AZURE_AI_API_KEY`, or explicitly select `--azure-ai-auth-mode default-credential`, then run the evaluation command below.

You can also select the mode explicitly:

# Explicit keyless authentication
runevals --azure-ai-auth-mode default-credential

# Explicit API key authentication
runevals --azure-ai-auth-mode key

Fallback behavior (auto-detect) - without the `--azure-ai-auth-mode`, the CLI defaults to AZURE_AI_API_KEY followed by DefaultAzureCredential.

Note:  DefaultAzureCredential  supports multiple credential sources, including Azure CLI, PowerShell, environment variables, and managed identity. See [Azure Identity docs](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.defaultazurecredential?view=azure-python) for details.

Selecting a tenant: Your Azure judge can be on a different tenant from your M365 Copilot extension. For cross-tenant access, configure the target tenant of your Azure tenant in your env file:

# Target tenant configuration
AZURE_TENANT_ID="<your-tenant-id>"

Tip: For Azure CLI credentials, use  `az login --tenant <your-tenant-id>` . Tenant configuration varies by credential source.

```powershell
runevals --judge-backend azure --prompts-file evals\evals.json --output results.json
```

GitHub Copilot access, policies, and usage limits apply.

## Environments and ATK

Run from your project or evaluation folder. ATK projects already provide tenant and package values; keep their existing settings. For example, `env\.env.local`:

```dotenv
TEAMS_APP_TENANT_ID="<your-tenant-id>"
M365_TITLE_ID="<your-package-title-id>"
```

Select the ATK agent and a named environment:

```powershell
runevals --env dev --judge-backend azure --prompts-file evals\evals.json --output results-dev.html
```

Without `--env`, the CLI discovers `.env.local`, then `.env.dev`, in the project root or `env` folder and loads the matching personal `.user` override. Explicit `--env <name>` layers `env\.env.<name>` over `.env.local` and `.env.local.user`.

Keep credentials in ignored personal files, never checked-in configuration.

## Advanced Usage

Re-score captured responses and available diagnostics without executing prompts:

```powershell
runevals --judge-backend azure --evaluate-only evals\captured-responses.json --output rescored.html
```

Each item or turn must include a `response`. Configure the selected judge; Microsoft 365 execution authentication is not needed.

For regression runs, increase parallelism from 1 up to 5:

```powershell
runevals --m365-agent-id "<your-agent-id>" --judge-backend github-copilot --prompts-file evals\evals.json --concurrency 3 --output results.json
```

For CI/CD, inspect evaluator scores and recorded errors, not just the process exit code. See [CI/CD guidance](CICD_CACHE_GUIDE.md).

For non-ATK projects, use the following folder structure. Run from `my-evaluations` and pass `--prompts-file evals\agents.json`, or `--prompts-file evals\plugins.json` for V2 Preview. Only `prompts.json`, `evals.json`, and `tests.json` are auto-discovered. The CLI loads environment variables from the files below:

```text
my-evaluations\
├── env\
│   ├── .env.local          # Tenant and optional agent ID
│   └── .env.local.user     # Secrets; exclude from source control
├── evals\
│   ├── plugins.json        # V2 Preview plugin dataset
│   └── agents.json         # Agent evaluation dataset
└── results\                # Generated reports
```

## Troubleshooting

| Problem | Check |
|---|---|
| Installed the wrong release channel | Install `@microsoft/m365-copilot-eval@latest` for V1 or `@microsoft/m365-copilot-eval@preview` for V2 Preview. |
| Agent ID is missing in V1 or CI | Supply `--m365-agent-id` or configure `M365_AGENT_ID`. |
| A V2 Preview plugin scenario runs against an agent | Remove configured agent IDs from the shell and selected environment. |
| Connector sign-in is requested | Complete connector authorization in Copilot first. |
| Python download or Microsoft 365 sign-in fails | See the platform and runtime requirements in the [troubleshooting guide](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/evaluations-cli-troubleshooting). |

Check available options:

```powershell
runevals --help
```

Capture additional diagnostics:

```powershell
runevals --judge-backend github-copilot --prompts "What can you help me with?" --log-level debug --output debug-results.json
```

**Reports and logs can contain sensitive content. Review and redact them before sharing; never commit credentials.**

## Documentation and Feedback

[Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/evaluations-cli-overview) | [Developer setup](DEV_SETUP.md) | [Testing guide](.github/TESTING_GUIDE.md)

[Open an issue](https://github.com/microsoft/m365-copilot-eval/issues/new/choose) for bugs or suggestions. For bugs, include the CLI version, operating system, judge backend, reproduction steps, and expected versus actual behavior. For features, describe the scenario and desired outcome. Remove credentials, personal information, and confidential content before sharing examples.

## Contributing

Contributions and suggestions are welcome. Most contributions require a [Contributor License Agreement](https://cla.opensource.microsoft.com); a bot will guide you when you submit a pull request.

This project follows the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). See the [FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com).

## Trademarks

Use of Microsoft trademarks must follow [Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/legal/intellectualproperty/trademarks/usage/general). Modified versions must not imply Microsoft sponsorship. Third-party trademarks are subject to their owners' policies.

## Terms of Use

By using this tool, you agree to the [Microsoft Software License Terms](https://aka.ms/evaltoolterms). See [LICENSE](LICENSE) for the full terms.

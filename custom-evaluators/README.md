# Custom evaluators

This folder contains **reference custom evaluators** for the
M365 Copilot Agent Evals CLI, plus this authoring guide. Custom
evaluators let you score agent responses against domain-specific
criteria — regulatory compliance, brand tone, custom relevance rubrics,
or anything else the ten built-in evaluators don't cover.

There are two kinds, and the CLI tells them apart automatically:

- **LLM-judge** evaluators (`<name>.py` **and** `<name>.prompty`) — call an
  LLM to score the response. They need Azure OpenAI config and use the 1-5
  scale.
- **Code-only / non-LLM** evaluators (`<name>.py` only, **no** `<name>.prompty`)
  — pure Python checks with no LLM call (e.g. "fail if the response contains a
  forbidden term"). They need no Azure OpenAI config and can return any numeric
  score. See [Code-only (non-LLM) custom evaluators](#code-only-non-llm-custom-evaluators).

To use your own custom evaluators, create a `custom-evaluators/` folder
at the root of your project (the directory you run the CLI from) and add
one subfolder per evaluator, as shown below. At runtime the CLI scans
`<your_project>/custom-evaluators/` automatically and loads only the
evaluators referenced by your eval document. Copy any of the reference
evaluators here as a starting point.

---

## Folder layout

Each custom evaluator lives in its own subfolder. An **LLM-judge** evaluator
consists of two files; a **code-only** evaluator is just the `.py`:

```
<your_project>/
  custom-evaluators/
    professional_tone/            # LLM-judge: has a .prompty
      professional_tone.prompty   # the LLM judge prompt
      professional_tone.py        # the Python wrapper that runs it
    consistency_check/
      consistency_check.prompty
      consistency_check.py
    forbidden_terms/              # code-only: NO .prompty
      forbidden_terms.py          # pure Python check, no LLM call
```

The presence of `<name>.prompty` is the only discriminator: with it, the
evaluator is an LLM judge; without it, it's code-only.

**Naming rules:**
- Folder name = evaluator name = file basenames (must match exactly).
- Names must match the pattern `^[a-zA-Z][a-zA-Z0-9_]*$` (valid identifier:
  start with a letter, then letters / digits / underscores).
- Names must **not** collide with built-in evaluator names
  (case-insensitive): `Relevance`, `Coherence`, `Groundedness`,
  `Similarity`, `ToolCallAccuracy`, `Citations`, `ExactMatch`,
  `PartialMatch`, `RetrievalQuery`, `RetrievalResult`. If you want a
  domain-tailored version of a built-in, prefix it — for example
  `domain_relevance` rather than `relevance`.

---

## Authoring a custom evaluator

### The `.prompty` file

A `.prompty` is the LLM judge prompt — model config in YAML frontmatter
above `---`, then `system:` / `user:` sections below it. Variables
referenced as `{{var}}` in the body map to the kwargs your wrapper
passes to the prompty flow.

Minimal example (`professional_tone.prompty`):

```yaml
---
name: professional_tone
description: Scores professional tone 1-5.
model:
  api: chat
  parameters:
    temperature: 0.0
    max_tokens: 400
    response_format:
      type: json_object
inputs:
  user_prompt:
    type: string
  response:
    type: string
---
system:
You score professional tone 1 (hostile) to 5 (consistently professional).
Reply with only: {"score": <int 1-5>, "reason": "<one sentence>"}

user:
# User prompt
{{user_prompt}}

# Agent response
{{response}}
```

> **You MUST declare an `inputs:` block in the frontmatter** listing every
> variable your template uses. Without it, promptflow filters all kwargs
> out and your template renders with empty `{{var}}` substitutions — the
> LLM will see a blank prompt and you'll get an `error` or nonsense score.
> Each input gets a `type:` (typically `string`).
>
> **Reserved input name:** The promptflow runtime reserves `prompt` as an
> internal parameter, so avoid using `{{prompt}}` (and an `inputs.prompt`
> declaration) in your prompty template. Use a different variable name like
> `{{user_prompt}}` and have your wrapper forward the value under that name
> when it calls the prompty flow.

### The `.py` wrapper

The Python module **MUST** export a class. The CLI dynamically imports
the module and instantiates the first top-level class it finds. The
class **MUST** match this contract:

```python
class MyEvaluator:
    def __init__(self, *, model_config, threshold, options=None):
        # model_config:  AzureOpenAIModelConfiguration
        # threshold:     numeric pass/fail threshold
        # options:       dict of extra config from the eval document
        # Any of these you don't use can be absorbed instead of named — see
        # "Absorbing constructor parameters you don't use" below.
        ...

    def __call__(
        self,
        *,
        prompt: str = "",
        expected_response: str = "",
        response: str = "",
        context: str = "",
        **_,  # accept extras for forward compatibility
    ) -> dict:
        # On success, return a flat dict with just:
        # {
        #     "score":  <integer 1-5>,
        #     "reason": "<explanation>",
        # }
        # The framework owns `result` and `threshold`: it derives
        # `result = "pass" if score >= threshold else "fail"` and attaches
        # `threshold`, so you do NOT return them. (Returning them is tolerated
        # for backward compatibility but ignored — the framework's values win.)
        # The CLI rewrites the "score" key to your evaluator's folder name
        # when merging into the unified output, so the score shows up as
        # `<folder_name>` in the JSON/CSV/HTML report.
        ...
```

**Error handling:** You don't need to wrap your `__call__` in
`try/except`. If your wrapper raises, the CLI catches the exception and
emits an `"error"` result for that evaluator while the rest of the run
continues. To control the error message yourself, return a dict via the
dedicated error channel (only the `"error"` message is kept; any other
keys are dropped):

```python
{ "error": "<explanation>" }
```

For example, the `consistency_check` example does this so a single bad
sample doesn't discard the other good samples. (The legacy
`{"result": "error", "error": ..., "threshold": ...}` shape is still
accepted for backward compatibility.)

**Score constraints (LLM-judge):**
- `score` MUST be an integer in `[1, 5]` (same 1-5 scale as built-in LLM
  evaluators). Float values that are mathematically integers (e.g. `4.0`)
  are accepted and normalized.
- Anything outside this range, non-numeric values, or a missing `"score"`
  key produces an `"error"` result; the eval run continues with other
  evaluators.

(Code-only evaluators relax the score rules — see
[Code-only (non-LLM) custom evaluators](#code-only-non-llm-custom-evaluators).)

### Absorbing constructor parameters you don't use

The framework always passes `threshold` and `options` to `__init__` (plus
`model_config` for LLM-judge evaluators). Python requires your `__init__`
to **accept** every keyword it's called with — but you don't have to
**name** the ones you ignore. A parameter must be named only if you
actually use it; anything else can be soaked up by a `**_` catch-all.

This matters because the framework now owns `result`/`threshold` (it
derives pass/fail itself), so many evaluators never touch `threshold`. The
reference examples keep `threshold` and `options` named for documentation,
but you can drop the ones you don't use:

```python
# Names only what it uses (options), absorbs the rest (threshold, etc.):
class ForbiddenTermsEvaluator:
    def __init__(self, *, options=None, **_):
        self._terms = (options or {}).get("terms", [])

# A check needing no config at all — absorb everything:
class NonEmptyEvaluator:
    def __init__(self, **_):  # ignores model_config, threshold, options
        pass

    def __call__(self, *, response: str = "", **_) -> dict:
        return {
            "score": 1 if response.strip() else 0,
            "reason": "non-empty" if response.strip() else "empty response",
        }
```

What you must **not** do is name a subset without a catch-all — e.g.
`def __init__(self, *, options=None)` raises `TypeError` because the
framework still passes `threshold=`, and nothing accepts it. Add `**_`
(or name `threshold`) to fix it.

### kwarg conventions

The CLI calls your `__call__` with the following fixed set of kwargs.
Three of them — `prompt`, `expected_response`, and `context` — are read
directly from the current item (or turn) in your eval document and passed
straight through. The fourth, `response`, is **not** from the document:
it's the agent's actual output, captured when the CLI sends `prompt` to
the agent under test. All four are passed to your evaluator (the LLM
judge), **not** to the agent. In particular, `context` is grounding for
the judge only — the agent never sees or retrieves it:

| kwarg               | What it is                                                      | Typical use in a judge                              |
| ------------------- | -------------------------------------------------------------- | --------------------------------------------------- |
| `prompt`            | The user's question/instruction sent to the agent              | Check responsiveness                                |
| `response`          | The agent's actual answer (the thing being scored)             | The subject of evaluation                           |
| `expected_response` | A reference/ideal answer, from the `expected_response` field   | Check accuracy (meaning-match against the reference)|
| `context`           | Grounding/source material the answer should be faithful to, from the `context` field | Check groundedness (no contradictions/hallucinations) |

`expected_response` and `context` are optional eval-document fields; when
absent the CLI passes an empty string.

Because all four are always passed, declare the ones you use and absorb
the rest with `**_` (as shown in the signature above); a `__call__` that
omits one of the four without a `**kwargs` catch-all raises `TypeError`,
and that evaluator reports an error result.

Inside your wrapper you own the call to the prompty flow, so your
prompty's `inputs:` block can declare **any names you invent**
(e.g. `aspect`, `rubric`) — your wrapper supplies them.

### Preparing `model_config` for `load_flow`

The `promptflow.client.load_flow` runtime needs a `"type"` field on the
config dict to pick the right connection class (AzureOpenAI vs OpenAI).
The `AzureOpenAIModelConfiguration` the CLI passes you doesn't carry that
field, so you need to add it before calling `load_flow`:

```python
prepared_config = dict(model_config)
prepared_config.setdefault(
    "type",
    "azure_openai" if "azure_endpoint" in prepared_config else "openai",
)
self._flow = load_flow(source=prompty_path, model={"configuration": prepared_config})
```

Without this, you'll see the misleading error
`"Not Support connection type None for embedding api"` at invocation time.
All three reference examples in this folder do this step in their
`__init__`; copy-paste from one of them when starting a new evaluator.

See `professional_tone/professional_tone.py` for a minimal end-to-end
example.

---

## Code-only (non-LLM) custom evaluators

A **code-only** evaluator is a folder with only `<name>.py` and **no**
`<name>.prompty`. The CLI detects the missing prompty and treats the
evaluator as a pure Python check — it never calls an LLM, so a run that
uses only code-only evaluators needs **no Azure OpenAI configuration**.

Use these for deterministic, rule-based checks: forbidden-term scans,
regex/format validation, length limits, JSON-schema conformance, etc.

Most code-only evaluators are a simple **pass/fail** check. The idiomatic
way to express that is to return `score: 1` for pass and `score: 0` for
fail, and leave the default `threshold` of `1` in place — the framework
then derives `result = "pass"` when `score (1) >= threshold (1)` and
`"fail"` when `score (0) < threshold (1)`. You only need a different score
range or threshold for graded checks (see [Result contract](#result-contract-same-as-llm-judge)).

### How code-only differs from LLM-judge

| | LLM-judge (`.py` + `.prompty`) | Code-only (`.py` only) |
| --- | --- | --- |
| `__init__` kwargs | `model_config`, `threshold`, `options` | `threshold`, `options` (**no** `model_config`) |
| `score` | integer `1-5` | any number, no 1-5 clamp (typically `0`/`1`) |
| Default `threshold` | `3` | `1` |
| Azure OpenAI config | required | not required |

The `__init__` for a code-only evaluator therefore omits `model_config`:

```python
class ForbiddenTermsEvaluator:
    def __init__(self, *, threshold, options=None):
        self._terms = (options or {}).get("terms", [])

    def __call__(self, *, response: str = "", **_) -> dict:
        hit = [t for t in self._terms if t.lower() in response.lower()]
        # Default threshold is 1, so 1 -> pass, 0 -> fail.
        return {
            "score": 0 if hit else 1,
            "reason": f"Found: {', '.join(hit)}" if hit else "clean",
        }
```

### Result contract (same as LLM-judge)

The framework owns `result` and `threshold` for both kinds. On success
return just `{"score", "reason"}`; the framework derives
`result = "pass" if score >= threshold else "fail"` and attaches
`threshold`. To signal a failure, **raise** or return `{"error": "<msg>"}`.

Scores must be oriented **higher-is-better**, because the framework passes
when `score >= threshold`. With the default non-LLM threshold of `1`,
encode a boolean outcome as `1` (pass) / `0` (fail).

Set the `threshold` in the eval document to match whatever scale your
score uses — there's no `[1, 5]` constraint for code-only evaluators. For a
graded check, return a fractional score and set a fractional threshold:
e.g. a partial-match evaluator returning a ratio in `[0, 1]` would set
`threshold: 0.7` to require a 70% match. Just keep the score higher-is-better
so that "more correct" never scores *lower* than "less correct".

### Forgot a `.prompty`?

Because a missing `.prompty` silently turns an evaluator into a code-only
one, the CLI guards against an accidentally-omitted prompty: if a
`.py`-only evaluator's code references LLM machinery (`load_flow`,
`promptflow`, `model_config`, or `.prompty`), the CLI logs a **warning**
suggesting you may have forgotten the prompty file. It never blocks the
run — if you really meant a code-only evaluator, ignore the warning (or
remove the LLM references).

See `forbidden_terms/forbidden_terms.py` for a complete code-only example.

---

## Learn more about `.prompty`

The `.prompty` format is an open Microsoft standard for LLM prompts. For
the full list of frontmatter fields, model parameters, template syntax,
and supported providers, see:

- **[prompty.ai](https://prompty.ai/)** — overview and how-to guides
- **[microsoft/prompty](https://github.com/microsoft/prompty)** — source and TypeSpec schema

The `model.parameters` block is passed straight through to the Azure
OpenAI Chat Completions API, so parameters like `temperature`,
`max_tokens`, `top_p`, `response_format`, `seed`, and `stop` are all
available. See the
[Azure OpenAI inference API reference](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/latest)
for the full list.

---

## Referencing custom evaluators from an eval document

Custom evaluators go in the `evaluators` map just like built-in ones.
The `threshold` defaults to `3` for LLM-judge evaluators (the 1-5 scale)
and `1` for code-only evaluators; set it explicitly if you want a
different cutoff:

```json
{
  "schemaVersion": "1.7.0",
  "items": [
    {
      "prompt": "How do I file an expense report?",
      "evaluators": {
        "Relevance": {},
        "professional_tone": { "threshold": 4 },
        "consistency_check": {
          "threshold": 3,
          "options": { "samples": 5 }
        }
      }
    }
  ]
}
```

Use `evaluators_mode` (`extend` or `replace`) exactly as with built-in
evaluators to control whether the custom evaluator runs alongside the
defaults or replaces them.

---

## Examples

Reference evaluators ship in this folder:

| Folder                 | Kind      | What it does                                                                                          |
| ---------------------- | --------- | ----------------------------------------------------------------------------------------------------- |
| `professional_tone/`   | LLM-judge | Minimal single-call tone scoring; the simplest possible wrapper shape (uses `prompt` + `response`)    |
| `consistency_check/`   | LLM-judge | Calls the prompty N times and returns the median, reducing LLM variance via self-consistency          |
| `answer_accuracy/`     | LLM-judge | Uses all four eval-document fields (`prompt`, `expected_response`, `response`, `context`) — compares the response against a reference answer while checking groundedness against context |
| `forbidden_terms/`     | Code-only | Pure Python substring scan — fails the response if it contains any configured forbidden term; no LLM call, no Azure config |

Copy any folder as a starting point for your own evaluator.

---

## Security model

Custom evaluators run with the **same permissions as the CLI itself**.
Review the code in any custom evaluator before adding it to your project —
it can do anything Python can do.

---

## Troubleshooting

- **`Unknown evaluator '<name>'`** — Check the folder is at
  `<your_project>/custom-evaluators/<name>/`, the file basenames match the
  folder name, and you're invoking the CLI from the project root.
- **`Custom evaluator '<name>' is missing required file '<name>.py'`** —
  Every evaluator folder must contain `<name>.py`. A `<name>.prompty` is
  only needed for LLM-judge evaluators; omit it for code-only ones.
- **`Custom evaluator '<name>' failed to import`** — Python syntax error
  or missing dependency in your `.py`. The error message includes the
  underlying exception.
- **Your `result` shows `"error"` with `reason` "could not parse score…"** —
  The LLM didn't return well-formed JSON. Verify your prompty has
  `response_format: { type: json_object }` (or an equivalent JSON schema)
  and the template explicitly asks for the `{"score": ..., "reason": ...}`
  shape.

For richer logs, run with `--log-level debug`.

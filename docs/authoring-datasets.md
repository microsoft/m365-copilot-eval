# Authoring evaluation datasets

An eval dataset is a JSON document that tells the M365 Copilot Agent Evaluations CLI which prompts to run, what responses to expect, and which evaluators determine pass or fail. The current eval document schema version is `1.4.0`; use the root-object format with `schemaVersion` and an `items` array. Do not author the legacy bare-array format (`[{ "prompt": "..." }]`).

The schema is defined in [`schema/v1/eval-document.schema.json`](../schema/v1/eval-document.schema.json). Review [`schema/CHANGELOG.md`](../schema/CHANGELOG.md) when updating older datasets.

## Minimal single-turn dataset

A single-turn item contains a top-level `prompt`. Add `expected_response` when you want evaluators such as `Similarity`, `ExactMatch`, or `PartialMatch` to compare the response to an expected answer.

```json
{
  "schemaVersion": "1.4.0",
  "metadata": {
    "name": "Agent starter evaluation",
    "description": "Smoke tests for core agent behavior.",
    "tags": ["starter", "single-turn"]
  },
  "default_evaluators": {
    "Relevance": {},
    "Coherence": {}
  },
  "items": [
    {
      "prompt": "What can this agent help me with?",
      "expected_response": "The agent explains its supported scope without claiming unsupported capabilities."
    }
  ]
}
```

## Single-turn item with context and evaluator thresholds

Use `context` when the answer should be grounded in specific source material. The `Groundedness` and `Similarity` evaluators use a 1-5 threshold scale.

```json
{
  "schemaVersion": "1.4.0",
  "default_evaluators": {
    "Relevance": {},
    "Coherence": {}
  },
  "items": [
    {
      "prompt": "What is the renewal deadline?",
      "expected_response": "The renewal deadline is May 31.",
      "context": "The Contoso renewal brief says the renewal deadline is May 31.",
      "evaluators": {
        "Groundedness": {
          "threshold": 4
        },
        "Similarity": {
          "threshold": 3
        }
      },
      "evaluators_mode": "extend"
    }
  ]
}
```

`evaluators_mode` controls how item-level evaluators combine with `default_evaluators`:

| Mode | Behavior |
| --- | --- |
| `"extend"` | Merge item-level evaluators with `default_evaluators`. This is the default when omitted. |
| `"replace"` | Run only the item-level evaluators for that item or turn. |

Use `"replace"` for deterministic checks that should not also run the default evaluators.

```json
{
  "schemaVersion": "1.4.0",
  "default_evaluators": {
    "Relevance": {},
    "Coherence": {}
  },
  "items": [
    {
      "prompt": "Return only the ticket ID for the escalation.",
      "expected_response": "INC-12345",
      "evaluators": {
        "ExactMatch": {}
      },
      "evaluators_mode": "replace"
    }
  ]
}
```

## Multi-turn items

Use a multi-turn item when the evaluation needs conversation context across follow-up prompts. A multi-turn item has a `turns` array; each turn has its own `prompt`, optional `expected_response`, optional `context`, and optional evaluator overrides. Do not put a top-level `prompt` on a multi-turn item.

```json
{
  "schemaVersion": "1.4.0",
  "metadata": {
    "name": "Multi-turn follow-up suite",
    "tags": ["multi-turn", "regression"]
  },
  "default_evaluators": {
    "Relevance": {},
    "Coherence": {}
  },
  "items": [
    {
      "name": "Follow-up retains project context",
      "description": "The agent should remember that the user is discussing the Contoso renewal.",
      "conversation_id": "contoso-renewal-followup",
      "turns": [
        {
          "prompt": "What is the latest status for the Contoso renewal?",
          "expected_response": "The agent gives the available Contoso renewal status without inventing missing details."
        },
        {
          "prompt": "Who owns the next step?",
          "expected_response": "The agent answers in the context of the Contoso renewal and cites or qualifies the source of the owner.",
          "evaluators": {
            "Groundedness": {
              "threshold": 4
            },
            "Citations": {
              "threshold": 1
            }
          },
          "evaluators_mode": "extend"
        }
      ]
    }
  ]
}
```

For a complete sample, see [`samples/multiturn_example.json`](../samples/multiturn_example.json). A multi-turn thread supports 1-20 turns.

## Public evaluators

Evaluator names are case-sensitive. The public evaluator names are:

| Evaluator | Use for | Threshold notes |
| --- | --- | --- |
| `Relevance` | Whether the answer addresses the prompt | 1-5 score; default threshold is 3 |
| `Coherence` | Clarity, organization, and readability | 1-5 score; default threshold is 3 |
| `Groundedness` | Whether the answer is supported by supplied context or source material | 1-5 score; default threshold is 3 |
| `Similarity` | Semantic similarity to `expected_response` | 1-5 score; default threshold is 3 |
| `Citations` | Whether the response contains enough citations | Minimum citation count; default threshold is 1 |
| `ExactMatch` | Deterministic exact answers such as IDs, dates, or labels | Boolean match against `expected_response` |
| `PartialMatch` | Flexible key-term or partial-string coverage | 0.0-1.0 score; default threshold is 0.5 |

```json
{
  "schemaVersion": "1.4.0",
  "default_evaluators": {
    "Relevance": {
      "threshold": 3
    },
    "Coherence": {
      "threshold": 3
    },
    "Groundedness": {
      "threshold": 3
    },
    "Similarity": {
      "threshold": 3
    },
    "Citations": {
      "threshold": 1
    },
    "PartialMatch": {
      "threshold": 0.5
    }
  },
  "items": [
    {
      "prompt": "List the open actions from the planning discussion.",
      "expected_response": "The agent lists action items with owners when available."
    }
  ]
}
```

## Designing a balanced suite (PRA)

PRA is a lightweight taxonomy for choosing scenarios. It is not a set of evaluator names.

| PRA area | What to test | Useful evaluators |
| --- | --- | --- |
| Perceive | Finding the right source, respecting available context, and citing evidence | `Groundedness`, `Citations`, `Relevance` |
| Reason | Synthesizing information, following instructions, handling ambiguity, and avoiding hallucination | `Relevance`, `Coherence`, `Similarity`, `PartialMatch` |
| Act | Producing the expected final artifact, answer, or action-oriented output | `Relevance`, `Coherence`, `ExactMatch`, `PartialMatch`, `Similarity` |

A balanced suite usually includes happy-path prompts, edge cases with missing or conflicting data, grounding/citation checks, deterministic outputs for IDs or dates, multi-turn follow-ups, and regression prompts for previously observed failures. Use `metadata.tags` or item `extensions` to label coverage.

```json
{
  "schemaVersion": "1.4.0",
  "metadata": {
    "name": "PRA coverage example",
    "tags": ["perceive", "grounding"]
  },
  "items": [
    {
      "prompt": "Who owns the next step for the Contoso renewal?",
      "expected_response": "The agent identifies the owner only if source data supports it.",
      "context": "The renewal plan says Alex owns the contract redlines.",
      "evaluators": {
        "Groundedness": {},
        "Citations": {}
      },
      "extensions": {
        "pra": "perceive",
        "risk": "unsupported-owner"
      }
    }
  ]
}
```

## Authoring checklist

Before committing a dataset:

1. Use `schemaVersion: "1.4.0"` and a root `items` array.
1. Author single-turn items with top-level `prompt`; author multi-turn items with `turns[].prompt` and no top-level `prompt`.
1. Include clear `expected_response` text when a comparison evaluator needs a reference answer.
1. Add `context` when evaluating grounded answers against source material.
1. Use only public evaluator names: `Relevance`, `Coherence`, `Groundedness`, `Similarity`, `Citations`, `ExactMatch`, and `PartialMatch`.
1. Treat `Citations` as a minimum citation count, not a 1-5 score.
1. Prefer `Similarity` or `PartialMatch` for flexible answers; use `ExactMatch` only when exact text is intended.
1. Choose `evaluators_mode: "extend"` to add checks to defaults and `"replace"` for item-specific evaluator sets.
1. Keep prompts realistic, sanitized, and free of secrets or customer data.
1. Use `metadata.tags` or `extensions` to label scenarios, risks, owners, or PRA coverage.
1. Validate JSON syntax and schema compatibility before running the dataset.

`response`, `citations`, `scores`, `summary`, `status`, and `error` are output-only fields populated by the runtime and should not be authored in input datasets.

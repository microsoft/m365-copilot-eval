"""Self-consistency quality evaluator.

Invokes the accompanying prompty multiple times and returns the median
score. This is the classic technique for reducing LLM variance: rather
than trusting a single LLM judgment, sample several and aggregate.

Why a Python wrapper is needed (vs. pure prompty): the LLM must be
called more than once per evaluation and per-call results must be
aggregated before a single final score is returned. A pure-prompty
evaluator can only call the LLM once.

Configuration (set via ``options`` in the eval document):
  - ``samples``: number of times to invoke the prompty (default 3)

Example reference from an eval document:

    "evaluators": {
      "consistency_check": {
        "threshold": 4,
        "options": { "samples": 5 }
      }
    }

Uses the portable ``judge`` contract (spec FR-016C): the CLI injects a
provider-neutral :class:`~judge_client.JudgeClient` — Azure OpenAI or GitHub
Copilot, whichever ``--judge-backend`` selects — instead of Azure model
configuration, so this evaluator runs unchanged on either judge.
"""

from __future__ import annotations

import json
import os
import statistics
from pathlib import Path
from typing import Any, Dict, List, Optional


_DEFAULT_SAMPLES = 3
_MAX_SAMPLES = 20
_PROMPTY_PATH = Path(__file__).parent / "consistency_check.prompty"


class ConsistencyCheckEvaluator:
    def __init__(
        self,
        *,
        judge: Any,
        threshold: float,
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._judge = judge
        # Clamp to [1, _MAX_SAMPLES]: each sample is one LLM call, so cap the
        # blast radius of a copied-and-edited "samples" value.
        self._samples = min(
            max(1, int((options or {}).get("samples", _DEFAULT_SAMPLES))),
            _MAX_SAMPLES,
        )

    def __call__(
        self,
        *,
        prompt: str = "",
        response: str = "",
        **_: Any,
    ) -> Dict[str, Any]:
        scores: List[int] = []
        errors: List[str] = []

        # Per-sample try/except so one bad LLM reply doesn't waste the rest.
        for i in range(self._samples):
            try:
                # NOTE: forward as `user_prompt`, not `prompt` — `prompt` is a
                # reserved input name inside promptflow's Prompty rendering.
                raw = self._judge.invoke_prompty(
                    prompty_path=_PROMPTY_PATH,
                    inputs={"user_prompt": prompt, "response": response},
                )
                if isinstance(raw, str):
                    raw = json.loads(raw)
                scores.append(int(raw["score"]))
            except Exception as exc:  # noqa: BLE001 — keep sampling
                errors.append(f"sample {i + 1}: {exc}")

        if not scores:
            return {
                "error": "; ".join(errors) or "no successful samples",
            }

        # round() is banker's rounding (half-to-even), so an even sample count
        # whose median lands on .5 rounds toward the even integer. Not reachable
        # with the default odd samples=3 (integer median), but noted for editors.
        median_score = round(statistics.median(scores))
        spread = max(scores) - min(scores)
        reason = (
            f"median={median_score} across {len(scores)} samples "
            f"(scores={scores}, spread={spread})"
        )
        if errors:
            reason = f"{reason}; errors: {'; '.join(errors)}"

        # Return only score + reason — the framework derives result/threshold.
        return {
            "score": median_score,
            "reason": reason,
        }

"""Answer accuracy evaluator.

Scores how well an agent's response answers the user's prompt on a 1-5
scale, combining three signals into a single LLM judgment:

  * ``response`` matches ``expected_response`` in meaning (accuracy)
  * ``response`` is consistent with ``context`` (groundedness)
  * ``response`` actually addresses ``prompt`` (responsiveness)

Demonstrates a custom evaluator that consumes all four eval-document
fields. Reference it from an eval document like:

    "evaluators": { "answer_accuracy": { "threshold": 4 } }
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

from promptflow.client import load_flow


class AnswerAccuracyEvaluator:
    def __init__(
        self,
        *,
        model_config: Any,
        threshold: float,
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        prepared = dict(model_config)
        prepared.setdefault(
            "type",
            "azure_openai" if "azure_endpoint" in prepared else "openai",
        )
        self._flow = load_flow(
            source=os.path.join(os.path.dirname(__file__), "answer_accuracy.prompty"),
            model={"configuration": prepared},
        )
        self._threshold = threshold

    def __call__(
        self,
        *,
        prompt: str = "",
        expected_response: str = "",
        response: str = "",
        context: str = "",
        **_: Any,
    ) -> Dict[str, Any]:
        # NOTE: forward as `user_prompt`, not `prompt` — `prompt` is reserved
        # inside promptflow.Prompty.__call__.
        raw = self._flow(
            user_prompt=prompt,
            expected_response=expected_response,
            response=response,
            context=context,
        )
        if isinstance(raw, str):
            raw = json.loads(raw)

        if "score" not in raw:
            raise ValueError("evaluator returned no 'score' field")
        score = raw["score"]
        return {
            "score": score,
            "threshold": self._threshold,
            "result": "pass" if score >= self._threshold else "fail",
            "reason": raw.get("reason", ""),
        }

"""Answer accuracy evaluator.

Scores how well an agent's response answers the user's prompt on a 1-5
scale, combining three signals into a single LLM judgment:

  * ``response`` matches ``expected_response`` in meaning (accuracy)
  * ``response`` is consistent with ``context`` (groundedness)
  * ``response`` actually addresses ``prompt`` (responsiveness)

Demonstrates a custom evaluator that consumes all four eval-document
fields. Reference it from an eval document like:

    "evaluators": { "answer_accuracy": { "threshold": 4 } }

Uses the portable ``judge`` contract (spec FR-016C): the CLI injects a
provider-neutral :class:`~judge_client.JudgeClient` — Azure OpenAI or GitHub
Copilot, whichever ``--judge-backend`` selects — instead of Azure model
configuration, so this evaluator runs unchanged on either judge.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

_PROMPTY_PATH = Path(__file__).parent / "answer_accuracy.prompty"


class AnswerAccuracyEvaluator:
    def __init__(
        self,
        *,
        judge: Any,
        threshold: float,
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._judge = judge

    def __call__(
        self,
        *,
        prompt: str = "",
        expected_response: str = "",
        response: str = "",
        context: str = "",
        **_: Any,
    ) -> Dict[str, Any]:
        # NOTE: forward as `user_prompt`, not `prompt` — `prompt` is a
        # reserved input name inside promptflow's Prompty rendering.
        raw = self._judge.invoke_prompty(
            prompty_path=_PROMPTY_PATH,
            inputs={
                "user_prompt": prompt,
                "expected_response": expected_response,
                "response": response,
                "context": context,
            },
        )
        if isinstance(raw, str):
            raw = json.loads(raw)

        if "score" not in raw:
            raise ValueError("evaluator returned no 'score' field")
        # Return only score + reason — the framework derives result/threshold.
        return {
            "score": raw["score"],
            "reason": raw.get("reason", ""),
        }

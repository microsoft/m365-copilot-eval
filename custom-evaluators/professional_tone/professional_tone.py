"""Professional tone evaluator — the simplest possible custom evaluator.

Scores professional tone on a 1-5 scale by asking an LLM judge defined in
``professional_tone.prompty``. Reference it from an eval document like:

    "evaluators": { "professional_tone": { "threshold": 4 } }

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

_PROMPTY_PATH = Path(__file__).parent / "professional_tone.prompty"


class ProfessionalToneEvaluator:
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
        response: str = "",
        **_: Any,
    ) -> Dict[str, Any]:
        # NOTE: forward as `user_prompt`, not `prompt` — `prompt` is a
        # reserved input name inside promptflow's Prompty rendering.
        raw = self._judge.invoke_prompty(
            prompty_path=_PROMPTY_PATH,
            inputs={"user_prompt": prompt, "response": response},
        )
        if isinstance(raw, str):
            raw = json.loads(raw)

        # Return only score + reason — the framework derives result/threshold.
        return {
            "score": raw["score"],
            "reason": raw.get("reason", ""),
        }

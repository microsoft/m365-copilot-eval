"""Professional tone evaluator — the simplest possible custom evaluator.

Scores professional tone on a 1-5 scale by asking an LLM judge defined in
``professional_tone.prompty``. Reference it from an eval document like:

    "evaluators": { "professional_tone": { "threshold": 4 } }
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

from promptflow.client import load_flow


class ProfessionalToneEvaluator:
    def __init__(
        self,
        *,
        model_config: Any,
        threshold: float,
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        # promptflow's load_flow needs a "type" field on the config dict to
        # pick the right connection class. Without this you'll see the
        # misleading "Not Support connection type None for embedding api"
        # error at invocation time.
        prepared = dict(model_config)
        prepared.setdefault(
            "type",
            "azure_openai" if "azure_endpoint" in prepared else "openai",
        )
        self._flow = load_flow(
            source=os.path.join(os.path.dirname(__file__), "professional_tone.prompty"),
            model={"configuration": prepared},
        )

    def __call__(
        self,
        *,
        prompt: str = "",
        response: str = "",
        **_: Any,
    ) -> Dict[str, Any]:
        # NOTE: forward as `user_prompt`, not `prompt` — `prompt` is reserved
        # inside promptflow.Prompty.__call__.
        raw = self._flow(user_prompt=prompt, response=response)
        if isinstance(raw, str):
            raw = json.loads(raw)

        # Return only score + reason — the framework derives result/threshold.
        return {
            "score": raw["score"],
            "reason": raw.get("reason", ""),
        }

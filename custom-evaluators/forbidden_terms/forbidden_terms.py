"""Forbidden-terms evaluator — a first-class *code-only* custom evaluator.

This is the canonical example of a **non-LLM** custom evaluator: a folder with
only ``forbidden_terms.py`` (no ``.prompty``). Because there is no prompty, the
CLI classifies it as code-only and:

* instantiates it WITHOUT ``model_config`` (so a run that uses only code-only
  evaluators needs no Azure OpenAI configuration), and
* lets it return any-numeric ``score`` (no 1-5 clamp).

The framework owns ``result`` and ``threshold``: it derives
``result = "pass" if score >= threshold else "fail"`` and attaches ``threshold``.
So this wrapper returns just ``{"score", "reason"}`` on success, and signals a
configuration failure by raising (it could also return ``{"error": ...}``). With
the default non-LLM threshold of ``1``, a clean response scores ``1`` (pass) and
a response containing a forbidden term scores ``0`` (fail).

Reference it from an eval document like::

    "evaluators": {
      "forbidden_terms": {
        "options": {
          "terms": ["lorem", "ipsum"],
          "case_sensitive": false
        }
      }
    }
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

_PASS_SCORE = 1
_FAIL_SCORE = 0


class ForbiddenTermsEvaluator:
    """Fail a response if it contains any configured forbidden term.

    Code-only: no ``model_config`` is accepted or used.
    """

    def __init__(
        self,
        *,
        threshold: Optional[float] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        opts = options or {}
        terms = opts.get("terms", [])
        if not isinstance(terms, list) or not all(isinstance(t, str) for t in terms):
            # Raising here surfaces the message as an "error" result for this
            # evaluator while the rest of the run continues.
            raise ValueError(
                "forbidden_terms: 'options.terms' must be a list of strings, e.g. "
                '{"options": {"terms": ["foo", "bar"]}}.'
            )
        self._case_sensitive: bool = bool(opts.get("case_sensitive", False))
        self._terms: List[str] = [
            t if self._case_sensitive else t.lower() for t in terms if t
        ]

    def __call__(
        self,
        *,
        response: str = "",
        **_: Any,
    ) -> Dict[str, Any]:
        haystack = response if self._case_sensitive else response.lower()
        found = [t for t in self._terms if t in haystack]
        passed = not found

        if not self._terms:
            reason = "No forbidden terms configured; nothing to check."
        elif passed:
            reason = "No forbidden terms found in the response."
        else:
            reason = f"Found forbidden term(s): {', '.join(sorted(set(found)))}."

        # Return only score + reason — the framework derives result/threshold.
        return {
            "score": _PASS_SCORE if passed else _FAIL_SCORE,
            "reason": reason,
        }

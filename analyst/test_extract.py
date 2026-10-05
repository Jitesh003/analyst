"""Fake-failure harness for the Stage 1.3 retry.

[cc] file. It feeds extract() scripted responses so you can test your retry
without waiting for the API to break. The retry itself is yours.

    python -m analyst.test_extract

All three checks must pass. Right now the last two fail -- that is the job.
"""

import sys
from types import SimpleNamespace

import analyst.extract as ex


class FakeParsed:
    """Stands in for your pydantic model, whatever you named it."""

    def model_dump(self, mode=None):
        return {"ceo_name": "Test Person", "company_name": "Test Co",
                "fiscal_year_end": "2025-03-31"}


def ok():
    return SimpleNamespace(
        parsed=FakeParsed(),
        text='{"ceo_name": "Test Person"}',
        usage_metadata=SimpleNamespace(prompt_token_count=88403,
                                       candidates_token_count=42),
    )


def junk():
    """A 200 OK the SDK is perfectly happy with, and you cannot use."""
    return SimpleNamespace(
        parsed=None,
        text="Sure! Here is the JSON you asked for:",
        usage_metadata=SimpleNamespace(prompt_token_count=88403,
                                       candidates_token_count=9),
    )


class Scripted:
    def __init__(self, script):
        self.script, self.calls = list(script), 0

    def generate_content(self, **kwargs):
        self.calls += 1
        return self.script.pop(0) if self.script else junk()


def run(script):
    """Calls extract() against a scripted client. Returns (result, exception, n_calls)."""
    models = Scripted(script)
    real = ex.genai
    ex.genai = SimpleNamespace(Client=lambda *a, **k: SimpleNamespace(models=models))
    try:
        return extract_quietly(models)
    finally:
        ex.genai = real


def extract_quietly(models):
    try:
        return ex.extract("pretend this is a 10-K"), None, models.calls
    except Exception as exc:
        return None, exc, models.calls


def check(name, condition, detail=""):
    print(f"  {'PASS' if condition else 'FAIL'}  {name}" + (f"  ({detail})" if detail else ""))
    return condition


if __name__ == "__main__":
    results = []

    out, exc, n = run([ok()])
    results.append(check("happy path returns a dict in one call",
                         out is not None and exc is None and n == 1,
                         f"calls={n} exc={type(exc).__name__ if exc else None}"))

    out, exc, n = run([junk(), ok()])
    results.append(check("one unusable reply, then success -> retries",
                         out is not None and exc is None and n == 2,
                         f"calls={n} exc={type(exc).__name__ if exc else None}"))

    out, exc, n = run([junk(), junk(), junk(), junk(), junk(), junk()])
    results.append(check("never usable -> retries, then gives up deliberately",
                         exc is not None and out is None and 1 < n <= 6
                         and not isinstance(exc, AttributeError),
                         f"calls={n} exc={type(exc).__name__ if exc else None}"))

    print()
    sys.exit(0 if all(results) else 1)

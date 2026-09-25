"""Sublab Medium - one Kazakh-correction task, six models.

Six models, one prompt, eight sentences. What you are producing is evidence:
a table that says which models repaired which kind of damage, and what each one
charged you for the attempt.

Fill in every `TODO`. Keep the function signatures.
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sublab_easy.registration_bot import (RATES_PER_MTOK,  # noqa: E402
                                          ask_once, estimate_cost)

DATA = Path(__file__).resolve().parent.parent / "data" / "kazakh_errors.json"

# Every model you must run. Keep the order - it is the order of your table.
MODELS = [
    ("openrouter", "google/gemma-4-26b-a4b-it"),
    ("openrouter", "qwen/qwen3.8-27b"),
    ("openrouter", "deepseek/deepseek-v4-flash-0731"),
    ("openai", "gpt-5.6-luna"),
    ("openai", "gpt-5.6-terra"),
    ("openai", "gpt-5.6-sol"),
]


def load_sentences() -> list[dict]:
    """The eight corrupted sentences and their published originals."""
    return json.loads(DATA.read_text(encoding="utf-8"))["sentences"]


def build_prompt(corrupted: str) -> str:
    return f"""
Correct the following Kazakh sentence.

The text may contain:
- Kazakh letters replaced by similar-looking Russian letters;
- letters from the wrong alphabet;
- accidentally joined words;
- a missing hyphen;
- duplicated letters.

Make only the minimum changes necessary to repair these corruptions.

Important rules:
- Preserve all punctuation that is not part of the corruption.
- Do not add stylistic punctuation such as commas, periods, question marks,
  colons, semicolons, or exclamation marks.
- If a hyphen is missing because of the corruption, restore that hyphen.
- Do not change capitalization unless a corrupted character itself requires it.
- Do not rewrite words, change grammatical forms, change word order, or improve
  the style of the sentence.
- Do not make any correction that is unrelated to the corrupted text.

Return EXACTLY one JSON object and nothing else in this format:
{{"corrected": "...", "changes": ["...", "..."]}}

In "corrected", return the corrected Kazakh sentence.
In "changes", list only the corrections you actually made.

Text:
{corrupted}
""".strip()


def parse_response(text: str) -> dict:
    decoder = json.JSONDecoder()

    for i, char in enumerate(text):
        if char != "{":
            continue

        try:
            parsed, _ = decoder.raw_decode(text[i:])
        except json.JSONDecodeError:
            continue

        if not isinstance(parsed, dict):
            continue

        corrected = parsed.get("corrected")
        changes = parsed.get("changes")

        if isinstance(corrected, str) and isinstance(changes, list):
            return {
                "corrected": corrected,
                "changes": changes,
            }

    raise ValueError(f"Could not find valid correction JSON in response: {text!r}")


def correct_with(model: str, corrupted: str, via: str) -> dict:
    prompt = build_prompt(corrupted)

    response = ask_once(
        prompt,
        model=model,
        via=via,
    )

    parsed = parse_response(response["text"])

    return {
        "corrected": parsed["corrected"],
        "changes": parsed["changes"],
        "input_tokens": response["input_tokens"],
        "output_tokens": response["output_tokens"],
        "model": response["model"],
    }


def score_correction(returned: str, expected: str) -> dict:
    differing_positions = sum(
        1
        for returned_char, expected_char in zip(returned, expected)
        if returned_char != expected_char
    )

    length_difference = abs(len(returned) - len(expected))

    return {
        "exact": returned == expected,
        "char_diff": differing_positions + length_difference,
    }


def run_all() -> list[dict]:
    """Every model against every sentence. One row per (model, sentence)."""
    rows = []
    for via, model in MODELS:
        for s in load_sentences():
            try:
                r = correct_with(model, s["corrupted"], via)
            except Exception as exc:            # a model failing IS a result
                rows.append({"model": model, "id": s["id"],
                             "errors": s["errors"], "failed": repr(exc)})
                continue
            rate_in, rate_out = RATES_PER_MTOK[model]
            rows.append({
                "model": model,
                "id": s["id"],
                "errors": s["errors"],
                "corrected": r["corrected"],
                "changes": r["changes"],
                **score_correction(r["corrected"], s["correct"]),
                "cost": estimate_cost(r["input_tokens"], r["output_tokens"],
                                      rate_in, rate_out),
                "input_tokens": r["input_tokens"],
                "output_tokens": r["output_tokens"],
            })
    return rows


def summarise(rows: list[dict]) -> None:
    """Per-model totals, to paste into SUBMISSION.md."""
    print(f"{'model':38}{'exact':>7}{'failed':>8}{'tokens':>9}{'cost $':>10}")
    print("-" * 72)
    for _, model in MODELS:
        mine = [r for r in rows if r["model"] == model]
        exact = sum(1 for r in mine if r.get("exact"))
        failed = sum(1 for r in mine if r.get("failed"))
        toks = sum(r.get("input_tokens", 0) + r.get("output_tokens", 0) for r in mine)
        cost = sum(r.get("cost", 0.0) for r in mine)
        print(f"{model:38}{exact:>7}{failed:>8}{toks:>9}{cost:>10.5f}")


if __name__ == "__main__":
    out = run_all()
    summarise(out)
    dest = Path(__file__).resolve().parent.parent / "outputs"
    dest.mkdir(exist_ok=True)
    (dest / "corrections.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote outputs/corrections.json ({len(out)} rows)")

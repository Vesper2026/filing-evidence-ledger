"""Organize user-supplied public disclosure evidence; never verify source claims."""
from __future__ import annotations

import argparse
from collections import Counter
import html
import json
from pathlib import Path
from urllib.parse import urlsplit

REQUIRED = ("id", "question", "title", "source_url", "location", "quote")


def text(value):
    return "" if value is None else str(value)


def md(value):
    return html.escape(text(value), quote=False).replace("\\", "\\\\").replace("|", "\\|").replace("[", "\\[").replace("]", "\\]").replace("\n", "<br>")


def review(document):
    rows = document.get("evidence") if isinstance(document, dict) else None
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError('Input must be an object with an "evidence" array of objects.')
    counts = Counter(text(row.get("id")).strip() for row in rows)
    items = []
    for index, row in enumerate(rows, 1):
        issues = [f"missing:{field}" for field in REQUIRED if not text(row.get(field)).strip()]
        identity = text(row.get("id")).strip()
        if identity and counts[identity] > 1:
            issues.append("duplicate:id")
        value = row.get("value")
        if value is not None and text(value).strip():
            if not isinstance(value, str):
                issues.append("value:use_string_to_preserve_original_precision")
            for field in ("unit", "period"):
                if not text(row.get(field)).strip():
                    issues.append(f"missing:{field}")
        source = text(row.get("source_url"))
        if source and (urlsplit(source).scheme not in ("http", "https") or not urlsplit(source).netloc):
            issues.append("source_url:not_absolute_http_url")
        status = row.get("status", "unreviewed")
        if status not in ("unreviewed", "reviewed"):
            issues.append("status:unknown")
        items.append({"row": index, "evidence": dict(row), "review_status": status, "checks": issues})
    return {
        "notice": "User-supplied evidence only. Source links, quotes and facts have NOT been verified.",
        "count": len(items),
        "items_needing_attention": sum(bool(item["checks"]) for item in items),
        "items": items,
    }


def render(report):
    lines = ["# Public-disclosure evidence ledger", "", report["notice"], ""]
    groups = {}
    for item in report["items"]:
        groups.setdefault(text(item["evidence"].get("question")) or "(No research question)", []).append(item)
    for question, items in groups.items():
        lines += [f"## {md(question)}", ""]
        for item in items:
            row = item["evidence"]
            lines += [f"### {md(row.get('id') or '(No ID)')} · row {item['row']}", "",
                      f"**Document:** {md(row.get('title'))}", "",
                      f"**Source URL (unverified):** {md(row.get('source_url'))}", "",
                      f"**Location:** {md(row.get('location'))} · **Disclosure date:** {md(row.get('disclosed_on'))}", "",
                      f"**Original quote:** {md(row.get('quote'))}", ""]
            if row.get("value") is not None:
                lines += [f"**Reported value:** {md(row.get('value'))} · currency={md(row.get('currency'))} · unit={md(row.get('unit'))} · period={md(row.get('period'))}", ""]
            lines += [f"**User review status:** {md(item['review_status'])}", "",
                      "**Field checks:** " + (", ".join(item["checks"]) or "No missing fields detected; not a fact check."), ""]
    lines += ["## Outstanding checklist", ""]
    for item in report["items"]:
        for issue in item["checks"]:
            lines.append(f"- [ ] Row {item['row']} / {md(item['evidence'].get('id'))}: {issue}")
    if not any(item["checks"] for item in report["items"]):
        lines.append("No field-completeness issues. Human source review is still required.")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, default=Path("review"), help="Output directory")
    args = parser.parse_args()
    try:
        report = review(json.loads(args.input.read_text(encoding="utf-8-sig")))
        destinations = [args.output / "ledger.json", args.output / "ledger.md"]
        if args.input.resolve() in [p.resolve() for p in destinations]:
            raise ValueError("Output must not overwrite the input file.")
        args.output.mkdir(parents=True, exist_ok=True)
        destinations[0].write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        destinations[1].write_text(render(report), encoding="utf-8")
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Error: {exc}\n")
    print(f"{report['count']} evidence rows; {report['items_needing_attention']} need field review. Sources not verified.")


if __name__ == "__main__":
    main()

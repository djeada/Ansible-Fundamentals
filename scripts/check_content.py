"""Validate local Markdown references and the course's navigable structure."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {".git", ".venv", ".sandbox", "__pycache__"}


def content_files():
    return [p for p in ROOT.rglob("*.md") if not IGNORED.intersection(p.relative_to(ROOT).parts)]


def headings(text: str) -> set[str]:
    seen: dict[str, int] = {}
    anchors = set()
    for title in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.MULTILINE):
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        suffix = seen.get(slug, 0)
        seen[slug] = suffix + 1
        anchors.add(slug if not suffix else f"{slug}-{suffix}")
    return anchors


def main() -> int:
    errors = []
    documents = content_files()
    for path in documents:
        text = path.read_text()
        # Do not interpret illustrative code as document navigation.
        prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        for target in re.findall(r"!?\[[^\]]*\]\(([^\s)]+)\)", prose):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            dest = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            if not dest.is_relative_to(ROOT) or not dest.exists():
                errors.append(f"{path.relative_to(ROOT)}: missing local target {target}")
            elif parsed.fragment and dest.suffix == ".md":
                if unquote(parsed.fragment) not in headings(dest.read_text()):
                    errors.append(f"{path.relative_to(ROOT)}: missing heading {target}")
    required = ["Before you run", "Predict", "Run", "Observe", "Experiment", "Explain", "Stretch", "Bash alternative", "Next"]
    for number in range(1, 13):
        base = ROOT / "labs" / f"lab{number:02}"
        for name in ["README.md", "playbook.yml", "alternative.sh"]:
            if not (base / name).is_file():
                errors.append(f"Missing {base.relative_to(ROOT) / name}")
        if (base / "README.md").is_file():
            text = (base / "README.md").read_text()
            for section in required:
                if f"## {section}\n" not in text:
                    errors.append(f"{base.relative_to(ROOT)}: missing {section} section")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Content checks passed: {len(documents)} Markdown files, 12 complete lab guides.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

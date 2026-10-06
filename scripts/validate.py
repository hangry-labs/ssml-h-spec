from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
NAMESPACE = "https://hangrylabs.app/ns/ssml-h/1.0"


class LocalLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.values: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in {"a", "img", "link", "script"}:
            return
        values = dict(attrs)
        target = values.get("href") or values.get("src")
        if target:
            self.values.append(target)


def main() -> None:
    specification = (ROOT / "specification.md").read_text(encoding="utf-8")
    page = (ROOT / "index.html").read_text(encoding="utf-8")

    for name, content in {"specification.md": specification, "index.html": page}.items():
        if NAMESPACE not in content:
            raise RuntimeError(f"{name} does not identify the SSML-H 1.0 namespace.")
        if "OmniVoice" in content:
            raise RuntimeError(f"{name} contains processor-specific OmniVoice content.")

    links = LocalLinks()
    links.feed(page)
    for target in links.values:
        parsed = urlparse(target)
        if parsed.scheme or target.startswith("#"):
            continue
        path = ROOT / parsed.path
        if not path.exists():
            raise RuntimeError(f"Missing local page dependency: {target}")

    print("SSML-H specification contract is valid.")


if __name__ == "__main__":
    main()

from dataclasses import dataclass
from pathlib import Path

import pytest


@dataclass(frozen=True)
class Html:
    base_dir: Path

    def read(self, file_name: str) -> str:
        p = self.base_dir / file_name
        return p.read_text()


@pytest.fixture
def html() -> Html:
    base_dir = Path(__file__).parent / "html"
    return Html(base_dir)

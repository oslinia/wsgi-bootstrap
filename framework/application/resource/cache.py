from .mapping import Link

link: Link

path: str

static: str

encoding: str

lang: str

templates: str

patterns: tuple[tuple[str, str], ...]

masks: dict[str, dict[int, tuple[str, ...]] | None]

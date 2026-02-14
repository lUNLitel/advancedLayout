from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import List


@dataclass
class Shot:
    shot_id: int
    name: str
    file_path: str
    trim_in: float = 0.0
    trim_out: float = 10.0
    comment: str = ""

    def duration(self) -> float:
        return max(0.0, self.trim_out - self.trim_in)


class Project:
    def __init__(self) -> None:
        self.shots: List[Shot] = []

    def _next_shot_id(self) -> int:
        if not self.shots:
            return 10
        return max(shot.shot_id for shot in self.shots) + 10

    def add_shot(self, file_path: str, trim_in: float = 0.0, trim_out: float = 10.0) -> Shot:
        shot_id = self._next_shot_id()
        shot = Shot(shot_id=shot_id, name=f"shot_{shot_id:03d}", file_path=file_path, trim_in=trim_in, trim_out=trim_out)
        self.shots.append(shot)
        return shot

    def move_shot(self, index: int, new_index: int) -> None:
        shot = self.shots.pop(index)
        self.shots.insert(new_index, shot)

    def replace_media(self, index: int, file_path: str, media_length: float | None = None) -> None:
        shot = self.shots[index]
        shot.file_path = file_path
        if media_length is not None and shot.trim_out > media_length:
            shot.trim_out = max(shot.trim_in, media_length)

    def to_dict(self) -> dict:
        return {"shots": [asdict(shot) for shot in self.shots]}

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        project = cls()
        for item in data.get("shots", []):
            project.shots.append(Shot(**item))
        return project

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "Project":
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))

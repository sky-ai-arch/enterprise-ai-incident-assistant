from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class GitCommit:
    sha: str
    author: str
    message: str
    timestamp: datetime
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Memory(ABC):

    @abstractmethod
    def get(
        self,
        key: str,
    ) -> Any:
        ...

    @abstractmethod
    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        ...

    @abstractmethod
    def delete(
        self,
        key: str,
    ) -> None:
        ...
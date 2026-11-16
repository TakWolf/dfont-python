from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from dfont.utils.stream import Stream


class Resource(ABC):
    @staticmethod
    @abstractmethod
    def parse(
            stream: Stream,
            data_length: int,
            tag: str,
            id: int,
            name: str | None,
            attributes: int = 0,
    ) -> Resource:
        raise NotImplementedError()

    id: int
    name: str | None
    attributes: int

    def __init__(
            self,
            id: int,
            name: str | None = None,
            attributes: int = 0,
    ) -> None:
        self.id = id
        self.name = name
        self.attributes = attributes

    def __copy__(self) -> Resource:
        return self.copy()

    def __deepcopy__(self, memo: dict[int, Any]) -> Resource:
        return self.deepcopy()

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Resource) or type(self) is not type(other):
            return NotImplemented
        return (self.id == other.id and
                self.name == other.name and
                self.attributes == other.attributes)

    @property
    @abstractmethod
    def tag(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def dump(self, stream: Stream) -> int:
        raise NotImplementedError()

    @abstractmethod
    def copy(self) -> Resource:
        raise NotImplementedError()

    @abstractmethod
    def deepcopy(self) -> Resource:
        raise NotImplementedError()

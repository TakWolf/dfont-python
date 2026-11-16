from __future__ import annotations

from io import BytesIO
from os import PathLike
from typing import Any, BinaryIO

from dfont.resources.resource import Resource
from dfont.utils.stream import Stream


class DFont:
    @staticmethod
    def parse(stream: bytes | bytearray | BinaryIO) -> DFont:
        stream = Stream(stream)
        # TODO
        raise NotImplementedError()

    @staticmethod
    def load(file_path: str | PathLike[str]) -> DFont:
        with open(file_path, 'rb') as file:
            return DFont.parse(file)

    resources: list[Resource]
    attributes: int

    def __init__(
            self,
            resources: list[Resource] | None = None,
            attributes: int = 0,
    ) -> None:
        self.resources = resources if resources is not None else []
        self.attributes = attributes

    def __copy__(self) -> DFont:
        return self.copy()

    def __deepcopy__(self, memo: dict[int, Any]) -> DFont:
        return self.deepcopy()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DFont):
            return NotImplemented
        return (self.resources == other.resources and
                self.attributes == other.attributes)

    def dump(self, stream: BinaryIO) -> None:
        stream = Stream(stream)
        # TODO
        raise NotImplementedError()

    def dump_to_bytes(self) -> bytes:
        stream = BytesIO()
        self.dump(stream)
        return stream.getvalue()

    def save(self, file_path: str | PathLike[str]) -> None:
        with open(file_path, 'wb') as file:
            self.dump(file)

    def copy(self) -> DFont:
        return DFont(
            self.resources,
            self.attributes,
        )

    def deepcopy(self) -> DFont:
        return DFont(
            [resource.deepcopy() for resource in self.resources],
            self.attributes,
        )

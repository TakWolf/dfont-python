from __future__ import annotations

from dfont.resources.resource import Resource
from dfont.utils.stream import Stream


class RawResource(Resource):
    @staticmethod
    def parse(
            stream: Stream,
            data_length: int,
            tag: str,
            id: int,
            name: str | None,
            attributes: int = 0,
    ) -> RawResource:
        data = stream.read(data_length)
        return RawResource(tag, id, data, name, attributes)

    _tag: str
    data: bytes

    def __init__(
            self,
            tag: str,
            id: int,
            data: bytes,
            name: str | None = None,
            attributes: int = 0,
    ) -> None:
        super().__init__(id, name, attributes)
        self._tag = tag
        self.data = data

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RawResource):
            return NotImplemented
        return (super().__eq__(other) and
                self.tag == other.tag and
                self.data == other.data)

    @property
    def tag(self) -> str:
        return self._tag

    def dump(self, stream: Stream) -> int:
        return stream.write(self.data)

    def copy(self) -> RawResource:
        return RawResource(
            self.tag,
            self.id,
            self.data,
            self.name,
            self.attributes,
        )

    def deepcopy(self) -> RawResource:
        return self.copy()

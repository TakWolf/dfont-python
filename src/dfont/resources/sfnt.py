from __future__ import annotations

from dfont.error import DFontParseError
from dfont.resources.resource import Resource
from dfont.utils.stream import Stream

_TAG = 'sfnt'


class SfntResource(Resource):
    """An 'sfnt' resource holding an entire SFNT font as opaque bytes.

    This wrapper preserves the font bytes without parsing the SFNT table directory
    or individual font tables.

    Attributes:
        data:
            Complete embedded SFNT font, excluding the resource-length word.
    """

    @staticmethod
    def parse(
            stream: Stream,
            data_length: int,
            tag: str,
            id: int,
            name: str | None,
            attributes: int = 0,
    ) -> SfntResource:
        if tag != _TAG:
            raise DFontParseError(f'expected resource tag {_TAG!r}, got {tag!r}')

        data = stream.read(data_length)
        return SfntResource(id, data, name, attributes)

    data: bytes

    def __init__(
            self,
            id: int,
            data: bytes,
            name: str | None = None,
            attributes: int = 0,
    ) -> None:
        super().__init__(id, name, attributes)
        self.data = data

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SfntResource):
            return NotImplemented
        return (super().__eq__(other) and
                self.data == other.data)

    @property
    def tag(self) -> str:
        return _TAG

    def dump(self, stream: Stream) -> int:
        return stream.write(self.data)

    def copy(self) -> SfntResource:
        return SfntResource(
            self.id,
            self.data,
            self.name,
            self.attributes,
        )

    def deepcopy(self) -> SfntResource:
        return self.copy()

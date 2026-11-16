from __future__ import annotations

from dfont.error import DFontParseError
from dfont.resources.resource import Resource
from dfont.utils.stream import Stream

_TAG = 'FOND'


class FondResource(Resource):
    @staticmethod
    def parse(
            stream: Stream,
            data_length: int,
            tag: str,
            id: int,
            name: str | None,
            attributes: int = 0,
    ) -> FondResource:
        if tag != _TAG:
            raise DFontParseError(f'expected resource tag {_TAG!r}, got {tag!r}')

        # TODO
        raise NotImplementedError()

    def __init__(
            self,
            id: int,
            name: str | None = None,
            attributes: int = 0,
    ) -> None:
        super().__init__(id, name, attributes)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FondResource):
            return NotImplemented
        return super().__eq__(other)

    @property
    def tag(self) -> str:
        return _TAG

    def dump(self, stream: Stream) -> int:
        # TODO
        raise NotImplementedError()

    def copy(self) -> FondResource:
        return FondResource(
            self.id,
            self.name,
            self.attributes,
        )

    def deepcopy(self) -> FondResource:
        return self.copy()

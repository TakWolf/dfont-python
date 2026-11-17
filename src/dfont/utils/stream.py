import struct
from collections.abc import Sequence
from io import BytesIO, SEEK_SET
from typing import BinaryIO


class Stream:
    source: BinaryIO

    def __init__(self, source: bytes | bytearray | BinaryIO | None = None) -> None:
        if source is None:
            source = BytesIO()
        elif isinstance(source, (bytes, bytearray)):
            source = BytesIO(source)
        self.source = source

    def read(self, size: int, ignore_eof: bool = False) -> bytes:
        if size < 0:
            raise ValueError(f'size must not be negative, got {size}')
        if size == 0:
            return b''

        chunk = self.source.read(size)
        if chunk is None:
            raise BlockingIOError('stream read would block')
        if len(chunk) == size:
            return chunk

        data = bytearray()
        while chunk:
            data.extend(chunk)
            remaining = size - len(data)
            if remaining == 0:
                break

            chunk = self.source.read(remaining)
            if chunk is None:
                raise BlockingIOError('stream read would block')

        if len(data) < size and not ignore_eof:
            raise EOFError()
        return bytes(data)

    def read_uint8(self) -> int:
        return self.read(1)[0]

    def read_uint8_list(self, count: int) -> list[int]:
        return list(self.read(count))

    def read_int8(self) -> int:
        return int.from_bytes(self.read(1), 'big', signed=True)

    def read_int8_list(self, count: int) -> list[int]:
        return list(struct.unpack(f'{count}b', self.read(count)))

    def read_uint16(self) -> int:
        return int.from_bytes(self.read(2), 'big', signed=False)

    def read_uint16_list(self, count: int) -> list[int]:
        return list(struct.unpack(f'>{count}H', self.read(count * 2)))

    def read_int16(self) -> int:
        return int.from_bytes(self.read(2), 'big', signed=True)

    def read_int16_list(self, count: int) -> list[int]:
        return list(struct.unpack(f'>{count}h', self.read(count * 2)))

    def read_uint24(self) -> int:
        return int.from_bytes(self.read(3), 'big', signed=False)

    def read_uint32(self) -> int:
        return int.from_bytes(self.read(4), 'big', signed=False)

    def read_uint32_list(self, count: int) -> list[int]:
        return list(struct.unpack(f'>{count}I', self.read(count * 4)))

    def read_int32(self) -> int:
        return int.from_bytes(self.read(4), 'big', signed=True)

    def read_int32_list(self, count: int) -> list[int]:
        return list(struct.unpack(f'>{count}i', self.read(count * 4)))

    def read_fixed_4_12(self) -> float:
        return self.read_int16() / 4096

    def read_pascal_bytes(self) -> bytes:
        return self.read(self.read_uint8())

    def write(self, data: bytes) -> int:
        view = memoryview(data)
        offset = 0
        while offset < len(view):
            written = self.source.write(view[offset:])
            if written is None:
                raise BlockingIOError('stream write would block')
            if written <= 0 or written > len(view) - offset:
                raise OSError(f'invalid stream write count: {written}')
            offset += written
        return offset

    def write_uint8(self, value: int) -> int:
        return self.write(value.to_bytes(1, 'big', signed=False))

    def write_uint8_list(self, values: Sequence[int]) -> int:
        return self.write(bytes(values))

    def write_int8(self, value: int) -> int:
        return self.write(value.to_bytes(1, 'big', signed=True))

    def write_int8_list(self, values: Sequence[int]) -> int:
        return self.write(struct.pack(f'{len(values)}b', *values))

    def write_uint16(self, value: int) -> int:
        return self.write(value.to_bytes(2, 'big', signed=False))

    def write_uint16_list(self, values: Sequence[int]) -> int:
        return self.write(struct.pack(f'>{len(values)}H', *values))

    def write_int16(self, value: int) -> int:
        return self.write(value.to_bytes(2, 'big', signed=True))

    def write_int16_list(self, values: Sequence[int]) -> int:
        return self.write(struct.pack(f'>{len(values)}h', *values))

    def write_uint24(self, value: int) -> int:
        return self.write(value.to_bytes(3, 'big', signed=False))

    def write_uint32(self, value: int) -> int:
        return self.write(value.to_bytes(4, 'big', signed=False))

    def write_uint32_list(self, values: Sequence[int]) -> int:
        return self.write(struct.pack(f'>{len(values)}I', *values))

    def write_int32(self, value: int) -> int:
        return self.write(value.to_bytes(4, 'big', signed=True))

    def write_int32_list(self, values: Sequence[int]) -> int:
        return self.write(struct.pack(f'>{len(values)}i', *values))

    def write_fixed_4_12(self, value: float) -> int:
        return self.write_int16(round(value * 4096))

    def write_pascal_bytes(self, value: bytes) -> int:
        if len(value) > 255:
            raise ValueError(f'pascal string must not exceed 255 bytes, got {len(value)}')
        return self.write_uint8(len(value)) + self.write(value)

    def write_nulls(self, size: int) -> int:
        if size < 0:
            raise ValueError(f'size must not be negative, got {size}')
        if size > 0:
            self.write(b'\x00' * size)
        return size

    def seek(self, offset: int, whence: int = SEEK_SET) -> None:
        self.source.seek(offset, whence)

    def tell(self) -> int:
        return self.source.tell()

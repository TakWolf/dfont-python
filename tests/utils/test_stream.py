import struct
from io import BytesIO
from typing import BinaryIO

import pytest

from dfont.utils.stream import Stream


@pytest.mark.parametrize(
    'source',
    [
        b'ABC',
        bytearray(b'ABC'),
        BytesIO(b'ABC'),
    ],
)
def test_source(source: bytes | bytearray | BinaryIO) -> None:
    stream = Stream(source)
    assert stream.read(3) == b'ABC'


def test_bytes() -> None:
    stream = Stream()
    assert stream.write(b'Hello World') == 11
    assert stream.tell() == 11
    stream.seek(0)
    assert stream.read(11) == b'Hello World'
    assert stream.tell() == 11


def test_eof() -> None:
    stream = Stream()
    stream.write(b'ABC')
    with pytest.raises(EOFError):
        stream.read(4)
    stream.seek(0)
    assert stream.read(4, ignore_eof=True) == b'ABC'


def test_uint8() -> None:
    stream = Stream()
    assert stream.write_uint8(0x00) == 1
    assert stream.write_uint8(0xFF) == 1
    assert stream.tell() == 2
    stream.seek(0)
    assert stream.read_uint8() == 0x00
    assert stream.read_uint8() == 0xFF
    assert stream.tell() == 2


def test_uint8_list() -> None:
    stream = Stream()
    assert stream.write_uint8_list([0x00, 0xFF]) == 2
    assert stream.tell() == 2
    stream.seek(0)
    assert stream.read_uint8_list(2) == [0x00, 0xFF]
    assert stream.tell() == 2


def test_int8() -> None:
    stream = Stream()
    assert stream.write_int8(-0x80) == 1
    assert stream.write_int8(0x7F) == 1
    assert stream.tell() == 2
    stream.seek(0)
    assert stream.read_int8() == -0x80
    assert stream.read_int8() == 0x7F
    assert stream.tell() == 2


def test_int8_list() -> None:
    stream = Stream()
    assert stream.write_int8_list([-0x80, 0x7F]) == 2
    assert stream.tell() == 2
    stream.seek(0)
    assert stream.read_int8_list(2) == [-0x80, 0x7F]
    assert stream.tell() == 2


def test_uint16() -> None:
    stream = Stream()
    assert stream.write_uint16(0x0000) == 2
    assert stream.write_uint16(0xFFFF) == 2
    assert stream.tell() == 4
    stream.seek(0)
    assert stream.read_uint16() == 0x0000
    assert stream.read_uint16() == 0xFFFF
    assert stream.tell() == 4


def test_uint16_list() -> None:
    stream = Stream()
    assert stream.write_uint16_list([0x0000, 0xFFFF]) == 4
    assert stream.tell() == 4
    stream.seek(0)
    assert stream.read_uint16_list(2) == [0x0000, 0xFFFF]
    assert stream.tell() == 4


def test_int16() -> None:
    stream = Stream()
    assert stream.write_int16(-0x8000) == 2
    assert stream.write_int16(0x7FFF) == 2
    assert stream.tell() == 4
    stream.seek(0)
    assert stream.read_int16() == -0x8000
    assert stream.read_int16() == 0x7FFF
    assert stream.tell() == 4


def test_int16_list() -> None:
    stream = Stream()
    assert stream.write_int16_list([-0x8000, 0x7FFF]) == 4
    assert stream.tell() == 4
    stream.seek(0)
    assert stream.read_int16_list(2) == [-0x8000, 0x7FFF]
    assert stream.tell() == 4


def test_uint24() -> None:
    stream = Stream()
    assert stream.write_uint24(0x000000) == 3
    assert stream.write_uint24(0xFFFFFF) == 3
    assert stream.tell() == 6
    stream.seek(0)
    assert stream.read_uint24() == 0x000000
    assert stream.read_uint24() == 0xFFFFFF
    assert stream.tell() == 6


def test_uint32() -> None:
    stream = Stream()
    assert stream.write_uint32(0x00000000) == 4
    assert stream.write_uint32(0xFFFFFFFF) == 4
    assert stream.tell() == 8
    stream.seek(0)
    assert stream.read_uint32() == 0x00000000
    assert stream.read_uint32() == 0xFFFFFFFF
    assert stream.tell() == 8


def test_uint32_list() -> None:
    stream = Stream()
    assert stream.write_uint32_list([0x00000000, 0xFFFFFFFF]) == 8
    assert stream.tell() == 8
    stream.seek(0)
    assert stream.read_uint32_list(2) == [0x00000000, 0xFFFFFFFF]
    assert stream.tell() == 8


def test_int32() -> None:
    stream = Stream()
    assert stream.write_int32(-0x80000000) == 4
    assert stream.write_int32(0x7FFFFFFF) == 4
    assert stream.tell() == 8
    stream.seek(0)
    assert stream.read_int32() == -0x80000000
    assert stream.read_int32() == 0x7FFFFFFF
    assert stream.tell() == 8


def test_int32_list() -> None:
    stream = Stream()
    assert stream.write_int32_list([-0x80000000, 0x7FFFFFFF]) == 8
    assert stream.tell() == 8
    stream.seek(0)
    assert stream.read_int32_list(2) == [-0x80000000, 0x7FFFFFFF]
    assert stream.tell() == 8


@pytest.mark.parametrize(
    ('value', 'data'),
    [
        (-8.0, b'\x80\x00'),
        (7.999755859375, b'\x7f\xff'),
        (0.0, b'\x00\x00'),
        (1.0, b'\x10\x00'),
        (-1.0, b'\xf0\x00'),
        (0.000244140625, b'\x00\x01'),
    ],
)
def test_fixed_4_12(value: float, data: bytes) -> None:
    stream = Stream(data)
    assert stream.read_fixed_4_12() == value
    assert stream.tell() == 2

    output = Stream()
    assert output.write_fixed_4_12(value) == 2
    output.seek(0)
    assert output.read(2) == data


@pytest.mark.parametrize(
    ('value', 'data'),
    [
        (0.1, b'\x01\x9a'),
        (-0.1, b'\xfe\x66'),
        (0.5 / 4096, b'\x00\x00'),
        (1.5 / 4096, b'\x00\x02'),
        (-1.5 / 4096, b'\xff\xfe'),
    ],
)
def test_fixed_4_12_rounding(value: float, data: bytes) -> None:
    stream = Stream()
    stream.write_fixed_4_12(value)
    stream.seek(0)
    assert stream.read(2) == data


@pytest.mark.parametrize(
    'value',
    [
        -8.000244140625,
        8.0,
    ],
)
def test_fixed_4_12_overflow(value: float) -> None:
    stream = Stream()
    with pytest.raises(OverflowError):
        stream.write_fixed_4_12(value)
    assert stream.tell() == 0


@pytest.mark.parametrize(
    ('values', 'data'),
    [
        ([], b''),
        (
            [
                0.0,
                1 / 256,
                1.0,
                1.5,
                32767 / 256,
                128.0,
                65535 / 256,
            ],
            b'\x00\x00\x00\x01\x01\x00\x01\x80\x7f\xff\x80\x00\xff\xff',
        ),
    ],
)
def test_ufixed_8_8_list(values: list[float], data: bytes) -> None:
    stream = Stream(data)
    assert stream.read_ufixed_8_8_list(len(values)) == values
    assert stream.tell() == len(data)

    output = Stream()
    assert output.write_ufixed_8_8_list(values) == len(data)
    assert output.tell() == len(data)
    output.seek(0)
    assert output.read(len(data)) == data


def test_ufixed_8_8_list_rounding() -> None:
    stream = Stream()
    stream.write_ufixed_8_8_list([0.1, 0.5 / 256, 1.5 / 256, 2.5 / 256])
    stream.seek(0)
    assert stream.read(8) == b'\x00\x1a\x00\x00\x00\x02\x00\x02'


@pytest.mark.parametrize(
    'value',
    [
        -1 / 256,
        256.0,
    ],
)
def test_ufixed_8_8_list_overflow(value: float) -> None:
    stream = Stream()
    with pytest.raises(struct.error):
        stream.write_ufixed_8_8_list([1.0, value])
    assert stream.tell() == 0


def test_ufixed_8_8_list_truncated() -> None:
    stream = Stream(b'\x01\x00\x01')
    with pytest.raises(EOFError):
        stream.read_ufixed_8_8_list(2)


def test_pascal_bytes() -> None:
    stream = Stream()
    assert stream.write_pascal_bytes(b'') == 1
    assert stream.write_pascal_bytes(b'ABC') == 4
    assert stream.tell() == 5
    stream.seek(0)
    assert stream.read_pascal_bytes() == b''
    assert stream.read_pascal_bytes() == b'ABC'
    assert stream.tell() == 5


def test_nulls() -> None:
    stream = Stream()
    assert stream.write_nulls(0) == 0
    assert stream.write_nulls(3) == 3
    assert stream.tell() == 3
    stream.seek(0)
    assert stream.read(3) == b'\x00' * 3
    assert stream.tell() == 3

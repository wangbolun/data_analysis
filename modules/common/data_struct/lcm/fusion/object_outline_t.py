"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

import common.point_2d_t

class object_outline_t(object):
    __slots__ = ["objectOutlinePointCount", "staticObjectPoints"]

    __typenames__ = ["int16_t", "common.point_2d_t"]

    __dimensions__ = [None, ["objectOutlinePointCount"]]

    def __init__(self):
        self.objectOutlinePointCount = 0
        self.staticObjectPoints = []

    def encode(self):
        buf = BytesIO()
        buf.write(object_outline_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">h", self.objectOutlinePointCount))
        for i0 in range(self.objectOutlinePointCount):
            assert self.staticObjectPoints[i0]._get_packed_fingerprint() == common.point_2d_t._get_packed_fingerprint()
            self.staticObjectPoints[i0]._encode_one(buf)

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != object_outline_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return object_outline_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = object_outline_t()
        self.objectOutlinePointCount = struct.unpack(">h", buf.read(2))[0]
        self.staticObjectPoints = []
        for i0 in range(self.objectOutlinePointCount):
            self.staticObjectPoints.append(common.point_2d_t._decode_one(buf))
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if object_outline_t in parents: return 0
        newparents = parents + [object_outline_t]
        tmphash = (0x259ac624e96543e+ common.point_2d_t._get_hash_recursive(newparents)) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if object_outline_t._packed_fingerprint is None:
            object_outline_t._packed_fingerprint = struct.pack(">Q", object_outline_t._get_hash_recursive([]))
        return object_outline_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)


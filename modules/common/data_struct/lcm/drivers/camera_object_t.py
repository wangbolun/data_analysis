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

class camera_object_t(object):
    __slots__ = ["centerPoint", "id", "type", "brake", "turn", "speedLon", "speedLat", "angle", "confidence", "width", "height", "length"]

    __typenames__ = ["common.point_2d_t", "int16_t", "int8_t", "int8_t", "int8_t", "float", "float", "float", "float", "float", "float", "float"]

    __dimensions__ = [None, None, None, None, None, None, None, None, None, None, None, None]

    def __init__(self):
        self.centerPoint = common.point_2d_t()
        self.id = 0
        self.type = 0
        self.brake = 0
        self.turn = 0
        self.speedLon = 0.0
        self.speedLat = 0.0
        self.angle = 0.0
        self.confidence = 0.0
        self.width = 0.0
        self.height = 0.0
        self.length = 0.0

    def encode(self):
        buf = BytesIO()
        buf.write(camera_object_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        assert self.centerPoint._get_packed_fingerprint() == common.point_2d_t._get_packed_fingerprint()
        self.centerPoint._encode_one(buf)
        buf.write(struct.pack(">hbbbfffffff", self.id, self.type, self.brake, self.turn, self.speedLon, self.speedLat, self.angle, self.confidence, self.width, self.height, self.length))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != camera_object_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return camera_object_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = camera_object_t()
        self.centerPoint = common.point_2d_t._decode_one(buf)
        self.id, self.type, self.brake, self.turn, self.speedLon, self.speedLat, self.angle, self.confidence, self.width, self.height, self.length = struct.unpack(">hbbbfffffff", buf.read(33))
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if camera_object_t in parents: return 0
        newparents = parents + [camera_object_t]
        tmphash = (0x3f776a8a93fd07c5+ common.point_2d_t._get_hash_recursive(newparents)) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if camera_object_t._packed_fingerprint is None:
            camera_object_t._packed_fingerprint = struct.pack(">Q", camera_object_t._get_hash_recursive([]))
        return camera_object_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)


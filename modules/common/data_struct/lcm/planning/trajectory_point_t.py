"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class trajectory_point_t(object):
    __slots__ = ["x", "y", "heading_angle", "speed", "acceleration", "curvature", "curvature_rate", "distance", "relative_time"]

    __typenames__ = ["double", "double", "double", "double", "double", "double", "double", "double", "double"]

    __dimensions__ = [None, None, None, None, None, None, None, None, None]

    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.heading_angle = 0.0
        self.speed = 0.0
        self.acceleration = 0.0
        self.curvature = 0.0
        self.curvature_rate = 0.0
        self.distance = 0.0
        self.relative_time = 0.0

    def encode(self):
        buf = BytesIO()
        buf.write(trajectory_point_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">ddddddddd", self.x, self.y, self.heading_angle, self.speed, self.acceleration, self.curvature, self.curvature_rate, self.distance, self.relative_time))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != trajectory_point_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return trajectory_point_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = trajectory_point_t()
        self.x, self.y, self.heading_angle, self.speed, self.acceleration, self.curvature, self.curvature_rate, self.distance, self.relative_time = struct.unpack(">ddddddddd", buf.read(72))
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if trajectory_point_t in parents: return 0
        tmphash = (0x287c72a4c394b50c) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if trajectory_point_t._packed_fingerprint is None:
            trajectory_point_t._packed_fingerprint = struct.pack(">Q", trajectory_point_t._get_hash_recursive([]))
        return trajectory_point_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)


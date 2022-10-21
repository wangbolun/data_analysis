"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

import fusion.moving_object_t

class fusion_objects_t(object):
    __slots__ = ["utime", "leftFrontObject", "frontObject", "rightFrontObject", "leftRearObject", "rearObject", "rightRearObject", "leftObject", "rightObject"]

    __typenames__ = ["int64_t", "fusion.moving_object_t", "fusion.moving_object_t", "fusion.moving_object_t", "fusion.moving_object_t", "fusion.moving_object_t", "fusion.moving_object_t", "fusion.moving_object_t", "fusion.moving_object_t"]

    __dimensions__ = [None, None, None, None, None, None, None, None, None]

    def __init__(self):
        self.utime = 0
        self.leftFrontObject = fusion.moving_object_t()
        self.frontObject = fusion.moving_object_t()
        self.rightFrontObject = fusion.moving_object_t()
        self.leftRearObject = fusion.moving_object_t()
        self.rearObject = fusion.moving_object_t()
        self.rightRearObject = fusion.moving_object_t()
        self.leftObject = fusion.moving_object_t()
        self.rightObject = fusion.moving_object_t()

    def encode(self):
        buf = BytesIO()
        buf.write(fusion_objects_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">q", self.utime))
        assert self.leftFrontObject._get_packed_fingerprint() == fusion.moving_object_t._get_packed_fingerprint()
        self.leftFrontObject._encode_one(buf)
        assert self.frontObject._get_packed_fingerprint() == fusion.moving_object_t._get_packed_fingerprint()
        self.frontObject._encode_one(buf)
        assert self.rightFrontObject._get_packed_fingerprint() == fusion.moving_object_t._get_packed_fingerprint()
        self.rightFrontObject._encode_one(buf)
        assert self.leftRearObject._get_packed_fingerprint() == fusion.moving_object_t._get_packed_fingerprint()
        self.leftRearObject._encode_one(buf)
        assert self.rearObject._get_packed_fingerprint() == fusion.moving_object_t._get_packed_fingerprint()
        self.rearObject._encode_one(buf)
        assert self.rightRearObject._get_packed_fingerprint() == fusion.moving_object_t._get_packed_fingerprint()
        self.rightRearObject._encode_one(buf)
        assert self.leftObject._get_packed_fingerprint() == fusion.moving_object_t._get_packed_fingerprint()
        self.leftObject._encode_one(buf)
        assert self.rightObject._get_packed_fingerprint() == fusion.moving_object_t._get_packed_fingerprint()
        self.rightObject._encode_one(buf)

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != fusion_objects_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return fusion_objects_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = fusion_objects_t()
        self.utime = struct.unpack(">q", buf.read(8))[0]
        self.leftFrontObject = fusion.moving_object_t._decode_one(buf)
        self.frontObject = fusion.moving_object_t._decode_one(buf)
        self.rightFrontObject = fusion.moving_object_t._decode_one(buf)
        self.leftRearObject = fusion.moving_object_t._decode_one(buf)
        self.rearObject = fusion.moving_object_t._decode_one(buf)
        self.rightRearObject = fusion.moving_object_t._decode_one(buf)
        self.leftObject = fusion.moving_object_t._decode_one(buf)
        self.rightObject = fusion.moving_object_t._decode_one(buf)
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if fusion_objects_t in parents: return 0
        newparents = parents + [fusion_objects_t]
        tmphash = (0x560c1f6f864502c7+ fusion.moving_object_t._get_hash_recursive(newparents)+ fusion.moving_object_t._get_hash_recursive(newparents)+ fusion.moving_object_t._get_hash_recursive(newparents)+ fusion.moving_object_t._get_hash_recursive(newparents)+ fusion.moving_object_t._get_hash_recursive(newparents)+ fusion.moving_object_t._get_hash_recursive(newparents)+ fusion.moving_object_t._get_hash_recursive(newparents)+ fusion.moving_object_t._get_hash_recursive(newparents)) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if fusion_objects_t._packed_fingerprint is None:
            fusion_objects_t._packed_fingerprint = struct.pack(">Q", fusion_objects_t._get_hash_recursive([]))
        return fusion_objects_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

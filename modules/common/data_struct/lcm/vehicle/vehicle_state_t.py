"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class vehicle_state_t(object):
    __slots__ = ["utime", "vin", "license_plate", "autodrive_enable", "steering_enable", "throttle_enable", "brake_enable", "acceleration_enable", "gear_enable", "lights_enable", "maximum_user_speed", "vehicle_speed", "wheel_speed_rl", "wheel_speed_rr", "acceleration_longitudinal", "acceleration_lateral", "yaw_rate", "turn_switch", "battery_level", "throttle_status", "brake_status", "steering_angle_status", "steering_speed_status", "gear_status", "turn_light_status", "brake_light_status", "beam_status", "horn_status", "windshield_wiper_status", "throttle_command", "acceleration_command", "brake_command", "steering_angle_command", "steering_speed_command", "gear_command", "turn_light_command", "brake_light_command", "beam_command", "horn_command", "windshield_wiper_command"]

    __typenames__ = ["int64_t", "string", "string", "int8_t", "int8_t", "int8_t", "int8_t", "int8_t", "int8_t", "int8_t", "float", "float", "float", "float", "float", "float", "float", "int8_t", "float", "float", "float", "float", "float", "int8_t", "int8_t", "int8_t", "int8_t", "int8_t", "int8_t", "float", "float", "float", "float", "float", "int8_t", "int8_t", "int8_t", "int8_t", "int8_t", "int8_t"]

    __dimensions__ = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

    def __init__(self):
        self.utime = 0
        self.vin = ""
        self.license_plate = ""
        self.autodrive_enable = 0
        self.steering_enable = 0
        self.throttle_enable = 0
        self.brake_enable = 0
        self.acceleration_enable = 0
        self.gear_enable = 0
        self.lights_enable = 0
        self.maximum_user_speed = 0.0
        self.vehicle_speed = 0.0
        self.wheel_speed_rl = 0.0
        self.wheel_speed_rr = 0.0
        self.acceleration_longitudinal = 0.0
        self.acceleration_lateral = 0.0
        self.yaw_rate = 0.0
        self.turn_switch = 0
        self.battery_level = 0.0
        self.throttle_status = 0.0
        self.brake_status = 0.0
        self.steering_angle_status = 0.0
        self.steering_speed_status = 0.0
        self.gear_status = 0
        self.turn_light_status = 0
        self.brake_light_status = 0
        self.beam_status = 0
        self.horn_status = 0
        self.windshield_wiper_status = 0
        self.throttle_command = 0.0
        self.acceleration_command = 0.0
        self.brake_command = 0.0
        self.steering_angle_command = 0.0
        self.steering_speed_command = 0.0
        self.gear_command = 0
        self.turn_light_command = 0
        self.brake_light_command = 0
        self.beam_command = 0
        self.horn_command = 0
        self.windshield_wiper_command = 0

    def encode(self):
        buf = BytesIO()
        buf.write(vehicle_state_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">q", self.utime))
        __vin_encoded = self.vin.encode('utf-8')
        buf.write(struct.pack('>I', len(__vin_encoded)+1))
        buf.write(__vin_encoded)
        buf.write(b"\0")
        __license_plate_encoded = self.license_plate.encode('utf-8')
        buf.write(struct.pack('>I', len(__license_plate_encoded)+1))
        buf.write(__license_plate_encoded)
        buf.write(b"\0")
        buf.write(struct.pack(">bbbbbbbfffffffbfffffbbbbbbfffffbbbbbb", self.autodrive_enable, self.steering_enable, self.throttle_enable, self.brake_enable, self.acceleration_enable, self.gear_enable, self.lights_enable, self.maximum_user_speed, self.vehicle_speed, self.wheel_speed_rl, self.wheel_speed_rr, self.acceleration_longitudinal, self.acceleration_lateral, self.yaw_rate, self.turn_switch, self.battery_level, self.throttle_status, self.brake_status, self.steering_angle_status, self.steering_speed_status, self.gear_status, self.turn_light_status, self.brake_light_status, self.beam_status, self.horn_status, self.windshield_wiper_status, self.throttle_command, self.acceleration_command, self.brake_command, self.steering_angle_command, self.steering_speed_command, self.gear_command, self.turn_light_command, self.brake_light_command, self.beam_command, self.horn_command, self.windshield_wiper_command))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != vehicle_state_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return vehicle_state_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = vehicle_state_t()
        self.utime = struct.unpack(">q", buf.read(8))[0]
        __vin_len = struct.unpack('>I', buf.read(4))[0]
        self.vin = buf.read(__vin_len)[:-1].decode('utf-8', 'replace')
        __license_plate_len = struct.unpack('>I', buf.read(4))[0]
        self.license_plate = buf.read(__license_plate_len)[:-1].decode('utf-8', 'replace')
        self.autodrive_enable, self.steering_enable, self.throttle_enable, self.brake_enable, self.acceleration_enable, self.gear_enable, self.lights_enable, self.maximum_user_speed, self.vehicle_speed, self.wheel_speed_rl, self.wheel_speed_rr, self.acceleration_longitudinal, self.acceleration_lateral, self.yaw_rate, self.turn_switch, self.battery_level, self.throttle_status, self.brake_status, self.steering_angle_status, self.steering_speed_status, self.gear_status, self.turn_light_status, self.brake_light_status, self.beam_status, self.horn_status, self.windshield_wiper_status, self.throttle_command, self.acceleration_command, self.brake_command, self.steering_angle_command, self.steering_speed_command, self.gear_command, self.turn_light_command, self.brake_light_command, self.beam_command, self.horn_command, self.windshield_wiper_command = struct.unpack(">bbbbbbbfffffffbfffffbbbbbbfffffbbbbbb", buf.read(88))
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if vehicle_state_t in parents: return 0
        tmphash = (0xa1ad5af9bae256ef) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if vehicle_state_t._packed_fingerprint is None:
            vehicle_state_t._packed_fingerprint = struct.pack(">Q", vehicle_state_t._get_hash_recursive([]))
        return vehicle_state_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)


import cantools
import os
import logging
import struct

import modules.common.data_struct.lcm.drivers.buffer_data_t as buffer_data_t

# can message 
#    * 1 byte   : control field
#    * 4 bytes  : frame ID 
#    * 8 bytes  : data
MSG_FORMAT  = '>BI8B'

# can message - control field
#   * 1 bit  : identifier extension           =|
#   * 1 bit  : remote transmission request     | ->  (std) 0b0000 = 0x0  or  (ext) 0b1000 = 0x8
#   * 2 bits : reserved (for future use)      =|
#   * 4 bits : data code length               =| ->  0x8
STD_CONTROL_FIELD  = 0x08  # standard
EXT_CONTROL_FIELD  = 0x88  # extended


class CanContainer(cantools.database.Database):

    def __init__(self, canbus_files=[]):
        super().__init__()

        if not canbus_files:
            return

        self.canbus_files = canbus_files
        for f in self.canbus_files:

            if os.path.isabs(f):
                self.add_dbc_file(str(f), encoding='gb2312')
            else:
                f = str(ab_platoon_root / 'common' / 'dbc'/ f)
                self.add_dbc_file(f, encoding='gb2312')
            self.remove_independent_can_signals()
        
        self.add_internal_can_dictionary()
        self.frame_ids = [msg.frame_id for msg in self.messages]

        self.control_field = STD_CONTROL_FIELD
        for message in self.messages:
            if message.is_extended_frame:
                self.control_field = EXT_CONTROL_FIELD

    def remove_independent_can_signals(self):
        try:
            self.messages.remove(self.get_message_by_name('VECTOR__INDEPENDENT_SIG_MSG'))
        except Exception as e:
            logging.info('delete VECTOR__INDEPENDENT_SIG_MSG error:'+ str(e))

    def add_internal_can_dictionary(self):
        for frame_id in self.messages:
            frame_id.val_dict            = {s.name:0 for s in frame_id.signals}

    def update_can_dict(self, frame_id, data):
        if frame_id not in self.frame_ids:
            return None

        frame_id_obj = self.get_message_by_frame_id(frame_id)
        
        try:
            decoded_data = self.decode_message(frame_id, data, decode_choices=False)
            for s, v in decoded_data.items():
                frame_id_obj.val_dict[s] = v 
        except Exception as e:
            logging.error(f'CAN decode error: {str(e)}')

    def encode_control_message_by_frame_id(self, frame_id):
        message = self.get_message_by_frame_id(frame_id)
        return self.encode_control_message(message)

    def encode_control_message(self, message):
        f_data = self.encode_message(message.frame_id, message.val_dict)
        return encode_lcm_can_message( self.control_field, message.frame_id, f_data )

    
class LcmlogCanContainer(CanContainer):
    
    def __init__(self, dbc_files):
        super().__init__(dbc_files)
        
    def add_internal_can_dictionary(self):
        for frame_id in self.messages:
            frame_id.val_dict = {s.name:[] for s in frame_id.signals}
            
    def reset(self):
        self.add_internal_can_dictionary()

    def update_can_dict(self, frame_id, data, timestamp):
        frame_id_obj = self.get_message_by_frame_id(frame_id)        
        decoded_data = self.decode_message(frame_id, data, decode_choices=False)
        for signal, value in decoded_data.items():
            frame_id_obj.val_dict[signal].append( (timestamp, value) ) 
            
    def parse_lcmlog(self, dataframe, t0):
        for packet, timestamp in dataframe.values:
            msg = buffer_data_t.decode(packet)
            timestamp = timestamp/1e6 - t0

            for st in range(0, msg.data_length, 13):
                _, frame_id = struct.unpack('>BI', msg.data[st:st + 5])
                if frame_id not in self.frame_ids:
                    continue
                self.update_can_dict( frame_id, msg.data[st + 5:st + 13], timestamp)
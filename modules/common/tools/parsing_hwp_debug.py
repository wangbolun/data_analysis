import numpy as np
from collections import namedtuple

import modules.common.data_struct.lcm.planning.hwp_debug_t as hwp_debug_t
from modules.common.tools.lcm_utilities import unpack_packets

HwpDebug = namedtuple(
    typename = "HwpDebug",
    field_names = (
        "timestamp",
        "lane_change_decision",
    ),
    defaults=(0,0)
)

def get_hwp_debug_data(lcmlog_dataframe, channel):
    _, timestamp, packets = unpack_packets(lcmlog_dataframe, channel)
    n_packets = len(packets)

    lane_change_decision = np.zeros(n_packets)

    for i,packet in enumerate(packets):
        msg = hwp_debug_t.decode(packet)
        
        lane_change_decision[i] = msg.turn_light
        
    return HwpDebug(
        timestamp = timestamp,
        lane_change_decision = lane_change_decision,
    )
import numpy as np
from collections import namedtuple

import modules.common.data_struct.proto.hmi.audio_pb2 as audio_pb2
from modules.common.tools.lcm_utilities import unpack_packets

HmiAudio = namedtuple(
    typename = "HmiAudio",
    field_names = (
        "timestamp",
        "audio_file_name", 
    ),
    defaults=(0,"")
)

def get_audio_data(lcmlog_dataframe, channel):
    _, timestamp, packets = unpack_packets(lcmlog_dataframe, channel)
    n_packets = len(packets)

    audio_file_name = [""]*n_packets

    audio_info = audio_pb2.Audio()
    for i,packet in enumerate(packets):
        audio_info.ParseFromString( packet )
        audio_file_name[i] = audio_info.audio_file_name

    return HmiAudio(
        timestamp = timestamp,
        audio_file_name = audio_file_name,
    )
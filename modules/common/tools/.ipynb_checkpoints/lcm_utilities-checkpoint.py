import dataclasses
import time, os

import numpy as np
import pandas as pd
from tqdm.notebook import trange, tqdm
from collections import namedtuple

import lcm

def create_lcm_dataset(lcmlog_file_path):
    lcmlog = lcm.EventLog(lcmlog_file_path, mode="r")
    buffer = [(e.eventnum, e.channel, e.data, e.timestamp) for e in tqdm(lcmlog)]
    lcmlog.close()
    data = pd.DataFrame(
        buffer, columns=["event-number", "channel", "data", "timestamp"]
    )
    data.filename = lcmlog_file_path.split("/")[-1]
    return data


def convert_localtime_to_date_str(localtime):
    return f"{localtime.tm_year:02d}-{localtime.tm_mon:02d}-{localtime.tm_mday:02d}"


def convert_localtime_to_time_str(localtime):
    return f"{localtime.tm_hour:02d}:{localtime.tm_min:02d}:{localtime.tm_sec:02d}"


def get_lcmlog_datetime(lcm_dataframe):
    t0_date = time.localtime(lcm_dataframe["timestamp"].values[0] / 1e6)
    tf_date = time.localtime(lcm_dataframe["timestamp"].values[-1] / 1e6)
    date = convert_localtime_to_date_str(t0_date)
    start = convert_localtime_to_time_str(t0_date)
    end = convert_localtime_to_time_str(tf_date)
    return (date, start, end)


@dataclasses.dataclass
class LcmlogMetaData:
    filename: str = ""
    date: str = ""
    start_time: str = ""
    end_time: str = ""
    summary_message: str = ""


def generate_lcmlog_statistics(lcm_dataframe):
    date, start, end = get_lcmlog_datetime(lcm_dataframe)

    # prepare header
    table_template = (
        "{0:30}|{1:11}|{2:11}|{3:18}|{4:18}|{5:18}|"  # {index: column_width}
    )
    summary_msg = f"Filename: \t {lcm_dataframe.filename} \n"
    summary_msg += f"Date: \t\t {date} \n"
    summary_msg += f"Start: \t\t {start} \n"
    summary_msg += f"Finish: \t {end} \n\n"
    summary_msg += table_template.format(
        "LCM_CHANNEL",
        "MSG COUNT ",
        "RATE [Hz] ",
        "AVG INTERVAL [ms] ",
        "MIN INTERVAL [ms] ",
        "MAX INTERVAL [ms] ",
    )
    summary_msg += "\n"

    for lcm_channel in lcm_dataframe["channel"].unique():
        message_count = lcm_dataframe["channel"].value_counts()[lcm_channel]

        data = lcm_dataframe[lcm_dataframe["channel"].isin([lcm_channel])][
            ["timestamp"]
        ]
        timestamps = data["timestamp"].values / 10 ** 6
        valid_data = len(timestamps) > 1

        time_intervals = np.diff(timestamps) if valid_data else 0
        intv_avg = (
            np.around(1e3 * np.mean(time_intervals), decimals=3) if valid_data else 0
        )
        intv_min = (
            np.around(1e3 * np.min(time_intervals), decimals=3) if valid_data else 0
        )
        intv_max = (
            np.around(1e3 * np.max(time_intervals), decimals=3) if valid_data else 0
        )
        rate = np.around(1.0 / np.mean(time_intervals), decimals=0) if valid_data else 0

        message_count = str(message_count)
        intv_avg = str(intv_avg)
        intv_min = str(intv_min)
        intv_max = str(intv_max)
        rate = str(rate)

        summary_msg += (
            table_template.format(
                lcm_channel, message_count, rate, intv_avg, intv_min, intv_max
            )
            + "\n"
        )

    out = LcmlogMetaData()
    out.filename = lcm_dataframe.filename
    out.date = date
    out.start_time = start
    out.end_time = end
    out.summary_message = summary_msg

    return out


def unpack_packets(lcmlog_dataframe, channel):
    df_lcm_channel = lcmlog_dataframe[ lcmlog_dataframe['channel'].isin([channel]) ][['data','timestamp']]
    packets, packets_timestamp = zip(*df_lcm_channel.values)
    n_packets = len(df_lcm_channel.values)

    log_starting_time = lcmlog_dataframe.timestamp.values[0]
    timestamp = (np.array(packets_timestamp) - log_starting_time)*1e-6
    return log_starting_time, timestamp, packets


from tkinter import Tk
from tkinter import filedialog

def get_lcm_dataset():
    Tk().withdraw()
    filenames = filedialog.askopenfilenames(initialdir='/home/jovyan/data/')
    filename = None if not filenames else filenames[0]

    if filename:
        lcmlog_dataframe = create_lcm_dataset(filename) 
        lcmlog_metadata = generate_lcmlog_statistics(lcmlog_dataframe)
        print(lcmlog_metadata.summary_message)

    return lcmlog_dataframe

def get_lcm_datasets():
    Tk().withdraw()
    lcm_log_dir = filedialog.askdirectory(initialdir='/home/jovyan/data/')
    lcm_log_files = os.listdir(lcm_log_dir)
    lcm_log_path = [lcm_log_dir + "/" + lcm_log_file for lcm_log_file in lcm_log_files]

    lcmlog_dataframes = []

    for filename in lcm_log_path:
        lcmlog_dataframe = create_lcm_dataset(filename) 
        lcmlog_metadata = generate_lcmlog_statistics(lcmlog_dataframe)
        lcmlog_dataframes.append(lcmlog_dataframe)
        print(filename)

    return lcmlog_dataframes


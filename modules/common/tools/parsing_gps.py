import numpy as np
from collections import namedtuple

import modules.common.data_struct.proto.localization.gps_imu_info_pb2 as gps_imu_info_pb2
from modules.common.tools.lcm_utilities import unpack_packets

GpsData = namedtuple(
    typename = "GpsStatus",
    field_names = (
        "timestamp",
        "timestamp_abs",
        "longitude", 
        "latitude", 
        "heading_angle",
        "location_status",
        "satellite_number"
    ),
    defaults=(0,0,0)
)

def get_gps_data(lcmlog_dataframe, channel):
    channel_starting_time, timestamp, packets = unpack_packets(lcmlog_dataframe, channel)
    n_packets = len(packets)

    longitude = np.zeros(n_packets)
    latitude = np.zeros(n_packets)
    heading_angle = np.zeros(n_packets)
    location_status = np.zeros(n_packets)
    satellite_number = np.zeros(n_packets)
    # gpsdata = []

    gps = gps_imu_info_pb2.gpsImu()
    for i,packet in enumerate(packets):
        gps.ParseFromString(packet)
        longitude[i] = gps.longitude
        latitude[i] = gps.latitude
        heading_angle[i] = gps.yaw
        location_status[i] = gps.location_status
        satellite_number[i] = gps.satellite_number
        # gpsdata.append(gps)
    # return gpsdata
    return GpsData(
        timestamp = timestamp,
        timestamp_abs = timestamp + channel_starting_time * 1e-6,
        longitude = longitude,
        latitude = latitude,
        heading_angle = heading_angle,
        location_status = location_status,
        satellite_number = satellite_number,
    )


# GPS utility functions
def rotate(data, angle):
    R = np.array([
        [np.cos(angle), -np.sin(angle) ],
        [np.sin(angle), np.cos(angle) ],
    ])
    
    return (R @ data.T ).T

vehicle_contour_origin = np.array([
    [0, -0.5],
    [0, 0],
    [0, 0.5],
    [2, 0],
    [0, -0.5]
])

def get_ego_contour(ego_x, ego_y, ego_heading):
    ego_contour = rotate(vehicle_contour_origin, ego_heading)
    ego_contour += np.array([ego_x, ego_y])
    return ego_contour

def compute_ellipse_radii_of_curvature(latitude, equatorial_radius=6378137., polar_radius=6356752.):
    a,b = equatorial_radius, polar_radius

    # ns=north-south  ew=east-west
    radius_ns = (a*b)**2 / ( (a*np.cos(latitude))**2 + (b*np.sin(latitude))**2 )**1.5
    radius_ew = (a*a) / np.sqrt( (a*np.cos(latitude))**2 + (b*np.sin(latitude))**2 )
    return radius_ns, radius_ew

class GeodeticModel:
    def __init__(self, location="tianjin"):
        if location == "tianjin":
            self.longitude_origin = np.deg2rad(117.2566420)
            self.latitude_origin  = np.deg2rad(39.135353)
        elif location == "cixi":
            self.longitude_origin = np.deg2rad(121.2014293)
            self.latitude_origin  = np.deg2rad(30.2904962)
        else:
            self.longitude_origin = np.deg2rad(0)
            self.latitude_origin  = np.deg2rad(0)

        self.yaw_offset = 0.0
        self.radius_ns, self.radius_ew = compute_ellipse_radii_of_curvature(self.latitude_origin)

    def transform_spherical_to_euclidean_coordinates(self, latitude, longitude, heading):
        dlat = np.deg2rad( latitude ) - self.latitude_origin
        dlon = np.deg2rad( longitude ) - self.longitude_origin
        yaw = -heading + np.pi/2 + self.yaw_offset
        yaw = np.arctan2(np.sin(yaw),np.cos(yaw))

        X = np.sin(dlon) * self.radius_ew * np.cos(self.latitude_origin)
        Y = np.sin(dlat) * self.radius_ns

        return X, Y, yaw


# Down sample GPS trajectory
def down_sample_gps_trajectory(x, y, distance = 0.5):
    if len(x) != len(y):
        return [], []

    chosen_indice = [False] * len(x)
    chosen_indice[0] = True
    x_left = x[0]
    y_left = y[0]
    for i in range(len(x)):
        if np.hypot(x_left - x[i], y_left - y[i]) >= distance:
            x_left = x[i]
            y_left = y[i]
            chosen_indice[i] = True

    return x[chosen_indice], y[chosen_indice], chosen_indice


def get_gps_trajectory_curvature(x, y):
    # ---------- get trajectory s ----------------- #
    s = np.cumsum( np.hypot(np.diff(x), np.diff(y)) )
    s = np.hstack([0, s])

    # ---------- get trajectory curvature --------- #
    curvature = []
    num = 3
    deg = 2
    for i in range(num, len(s)-num):
        zx = np.poly1d(
            np.polyfit(
                s[i-num : i+num], x[i-num : i+num], deg
            )
        )
        zxd = np.polyder(zx)
        zxdd = np.polyder(zxd)
        zy = np.poly1d(
            np.polyfit(
                s[i-num : i+num], y[i-num : i+num], deg
            )
        )
        zyd = np.polyder(zy)
        zydd = np.polyder(zyd)
        curvature.append(
            1
            / (1 + (zyd(s[i]) / zxd(s[i])) ** 2)
            * (zydd(s[i]) * zxd(s[i]) - zyd(s[i]) * zxdd(s[i]))
            / zxd(s[i]) ** 2
        )
    curvature = np.array(curvature)
    curvature = np.hstack(
        [curvature[0] * np.ones(num), curvature, curvature[-1] * np.ones(num)]
    )

    return curvature
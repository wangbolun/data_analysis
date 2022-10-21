import numpy as np

def nearest_point_index(x_vec, y_vec, x_point, y_point):
    min_distance = np.inf
    current_index = 0
    min_index = -1
    for (x, y) in zip(x_vec, y_vec):
        current_distance = np.hypot(x_point-x, y_point-y)
        if current_distance < min_distance:
            min_index = current_index
            min_distance = current_distance
        current_index += 1
    return min_index

def aligned_point(x_vec_1, y_vec_1, x_vec_2, y_vec_2):
    index_bgn = nearest_point_index(x_vec_1, y_vec_1, x_vec_2[0], y_vec_2[0])
    index_bgn = max(index_bgn-1,0)
    index_end = nearest_point_index(x_vec_1, y_vec_1, x_vec_2[-1], y_vec_2[-1])
    index_end = min(index_end+1,len(x_vec_1)-1)
    return x_vec_1[index_bgn:index_end], y_vec_1[index_bgn:index_end]

def compute_discrete_point_distance(x,y):
    distance = np.hstack([np.array([0]),
                          np.cumsum(np.hypot(np.diff(x),
                                             np.diff(y)
                                            )
                                    )
                        ])
    return distance

def compute_discrete_point_heading(x,y):
    heading = np.arctan2(np.diff(y),np.diff(x))
    return heading

def compute_discrete_point_curvature(x,y):
    heading = compute_discrete_point_heading(x,y)
    ds = np.hypot(np.diff(x), np.diff(y))
    ds = np.array([(ds[i] + ds[i+1])/2 for i in range(len(ds)-1)])
    dtheta = np.diff(heading)
    dtheta = np.array([np.arctan2(np.sin(dtheta_i),np.cos(dtheta_i)) for dtheta_i in dtheta])
    curvature = np.diff(heading)/ds
    return curvature
    